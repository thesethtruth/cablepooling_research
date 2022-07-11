import uuid
import pyomo.environ as pyo
import numpy as np
from copy import deepcopy as copy
from LESO.experiments.analysis import (
    gdatastore_put_entry,
    gcloud_upload_experiment_dict,
)

import LESO
from LESO.experiments import ema_pyomo_interface

from cablepool_definitions import (
    lithium_linear_map,
    RESULTS_FOLDER,
    MODEL,
    METRICS,
    COLLECTION,
    OUTPUT_PREFIX,
)
from LESO.finance import (
    determine_total_investment_cost,
    determine_roi,
    determine_total_net_profit,
)
from LESO.leso_logging import get_module_logger

logger = get_module_logger(__name__)


def Handshake(
    pv_cost=None,
    battery_cost=None,
    model=MODEL,
):

    # initiate System component
    system = LESO.System.read_pickle(model)

    # process ema inputs to components
    for component in system.components:
        if isinstance(component, LESO.PhotoVoltaic):
            component.capex = pv_cost
        if isinstance(component, LESO.Lithium):
            component.capex_storage = component.capex_storage * battery_cost
            component.capex_power = lithium_linear_map(battery_cost)

    # generate file name and filepath for storing
    filename_export = OUTPUT_PREFIX + str(uuid.uuid4().fields[-1]) + ".json"
    filepath = RESULTS_FOLDER / filename_export
    logfile = filename_export.replace(".json", ".log")

    ## initiate the solver kwargs
    solver_kwrgs = {
        "BarConvTol": 1e-8,
        "LogToConsole": 0,
        "LogFile": logfile,
        "Method": 2,
        "Crossover": -1,
    }

    ## SOLVE
    system.optimize(
        objective="osc",  # overnight system cost
        time=None,  # resorts to default; year 8760h
        store=True,  # write-out to json
        filepath=filepath,  # resorts to default: modelname+timestamp
        solver="gurobi",  # default solver
        nonconvex=False,  # solver option (warning will show if needed)
        solve=True,  # solve or just create model
        solver_kwrgs=solver_kwrgs,
    )

    return system, filename_export, logfile


@ema_pyomo_interface
def CablePooling(
    pv_cost=1,
    battery_cost=1,
    run_ID=None,
):

    # hand ema_inputs over to the LESO handshake
    system, filename_export = Handshake(
        pv_cost=pv_cost,
        battery_cost=battery_cost,
    )

    # check for optimalitiy before trying to access all information
    if pyo.check_optimal_termination(system.model.results):

        # extract capacities from system components
        capacities = {
            component.name + " installed capacity": component.installed
            for component in system.components
            if not isinstance(component, LESO.FinalBalance)
        }

        # calculate total renewable energy
        total_renewable_energy = sum(
            sum(
                component.state.power
                for component in system.components
                if any(
                    [
                        isinstance(component, LESO.PhotoVoltaic),
                        isinstance(component, LESO.Wind),
                    ]
                )
            )
        )

        # calculate curtailment
        curtailment = sum(
            sum(
                component.state.power
                for component in system.components
                if isinstance(component, LESO.FinalBalance)
            )
        )

        # calculate additional investment cost
        total_investment_cost = determine_total_investment_cost(system)
        roi = determine_roi(system)
        net_profit = determine_total_net_profit(system)

        # combine performance indicators to one dictionary
        pi = {
            "objective_result": system.model.results["Problem"][0]["Lower bound"],
            "total_renewable_energy": total_renewable_energy,
            "total_investment_cost": total_investment_cost,
            "curtailment": curtailment,
            "return_on_add_investment": roi,
            "net_profit_add_investment": net_profit,
        }

        # create and update results dictionary
        results = dict()
        results.update(capacities)
        results.update(pi)
        meta_data = {"filename_export": filename_export}

    ## Non optimal exit, no results
    else:
        meta_data = {"filename_export": "N/a"}
        results = {metric: np.nan for metric in METRICS}

    ## In any case
    meta_data.update(
        {
            "solving_time": system.model.results["solver"][0]["Time"],
            "solver_status": system.model.results["solver"][0]["status"].__str__(),
            "solver_status_code": system.model.results["solver"][0]["Return code"],
        }
    )

    # create db entry with results, ema_inputs and meta_data
    db_entry = copy(results)  # results
    db_entry.update(
        {  # ema_inputs
            "battery_cost": battery_cost,
            "pv_cost": pv_cost,
        }
    )
    db_entry.update(meta_data)  # metadata
    db_entry.update({"run_id": run_ID})

    # put db_entry to google datastore, keeps retrying when internet is down.
    succesful = False
    while not succesful:
        try:
            gdatastore_put_entry(COLLECTION, db_entry)
            succesful = True
        except:
            pass

    # put system.results to google cloud, keeps retrying when internet is down.
    succesful = False
    while not succesful:
        try:
            gcloud_upload_experiment_dict(system.results, COLLECTION, filename_export)
            succesful = True
        except:
            pass

    return results
