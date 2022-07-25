#%% cablepool_definitions.py
from pathlib import Path
import LESO
from google.cloud.exceptions import Conflict
from functools import partial
from LESO.experiments.analysis import move_log_from_active_to_cold


#%%
# cost_range = (lower, upper)
PV_COST_RANGE = (170e-3, 420e-3)
BATTERY_ENERGY_COST_RANGE = (46e-3, 299e-3)
BATTERY_POWER_COST_RANGE = (40e-3, 510e-3)

COLLECTION = "cablepooling_paper"
OUTPUT_PREFIX = f"{COLLECTION}_exp_"


MODEL_FOLDER = Path(__file__).parent.parent / "model"
RESULTS_FOLDER = Path(__file__).parent.parent / "results"
RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

ACTIVE_FOLDER = Path(__file__).parent

move_log_from_active_to_cold = partial(
    move_log_from_active_to_cold,
    active_folder=ACTIVE_FOLDER,
    cold_folder=RESULTS_FOLDER,
)


# create bucket if not already exist
if False:
    try:
        LESO.dataservice.google.cloud_create_bucket(COLLECTION)
    except Conflict as c:
        print(c)

MODEL = MODEL_FOLDER / "cablepooling_paper.pkl"

METRICS = [
    # components
    "PV South installed capacity",
    "Nordex N100 2500 installed capacity",
    "1h battery installed capacity",
    "2h battery installed capacity",
    "4h battery installed capacity",
    "6h battery installed capacity",
    "8h battery installed capacity",
    "12h battery installed capacity",
    "Grid connection installed capacity",
    # others
    "objective_result",
    "total_renewable_energy",
    "total_investment_cost",
    "curtailment",
    "return_on_add_investment",
    "net_profit_add_investment",
]


# this is needed due to the dependent but double variant uncertainty ranges given by ATB
def lithium_linear_map(value):
    min, max = BATTERY_ENERGY_COST_RANGE
    map_min, map_max = BATTERY_POWER_COST_RANGE

    frac = (value - min) / (max - min)
    m_value = frac * (map_max - map_min) + map_min

    return m_value


# for the linear map in 2050, we return the same value
def linear_map_2050(value):
    return value


if __name__ == "__main__":
    # use this to easily generate the metrics for installed capacity
    if False:
        ref_system = LESO.System.read_pickle(MODEL)
        m = []
        for c in ref_system.components:
            if not isinstance(c, (LESO.FinalBalance, LESO.ETMdemand)):
                out = c.name + " installed capacity"
                m.append(out)
        print(m)
