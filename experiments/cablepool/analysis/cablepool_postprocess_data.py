#%% evhub_postprocess_tools.py
from pathlib import Path

import pandas as pd

from LESO.experiments.analysis import gcloud_read_experiment, gdatastore_results_to_df

FOLDER = Path(__file__).parent
RESOURCE_FOLDER = FOLDER / "resources"
RESOURCE_FOLDER.mkdir(exist_ok=True)
COLLECTION = "cablepooling_paper_v2"

## pointers
# PV
pv_col1 = pv_col3 = "PV high DC ratio installed capacity"
pv_col2 = "PV low DC ratio installed capacity"
# Wind
wind_col = "Nordex N100 2500 installed capacity"
# Battery
bat1_col = "1h battery installed capacity"
bat2_col = "2h battery installed capacity"
bat4_col = "4h battery installed capacity"
bat6_col = "6h battery installed capacity"
bat8_col = "8h battery installed capacity"
bat12_col = "12h battery installed capacity"
# collectors
batcols = [bat1_col, bat2_col, bat4_col, bat6_col, bat8_col, bat12_col]
# pv_dict
pv_dict = {
    pv_col1: {"dc_ratio": 2, "specific_yield": None},
    pv_col2: {"dc_ratio": 1 / 0.7, "specific_yield": None},
    pv_col3: {"dc_ratio": 2, "specific_yield": None},
}

# alts
total_bat_col = "total_storage_energy"
pv_ac_col = "total_pv_ac"
pv_dc_col = "total_pv_dc"

bivar_tech_dict = {
    "PV AC": pv_ac_col,
    "PV DC": pv_dc_col,
    "wind": wind_col,
    "battery": total_bat_col,
}

experiments = ["high_ratio", "low_ratio", "both_ratios"]

#%% load in results
def get_data_from_db(experiment, force_refresh=False):

    filename = f"{experiment}.pkl"
    pickled_db = RESOURCE_FOLDER / filename

    # buffer all the calculations/db, only refresh if forced to refresh
    if pickled_db.exists() and not force_refresh:

        print("opened pickle -- not refreshed")
        db = pd.read_pickle(pickled_db)

    else:
        filters = [("dc_ratio", "=", experiment)]
        db = gdatastore_results_to_df(collection=COLLECTION, filters=filters)
        db.to_pickle(RESOURCE_FOLDER / filename)

    return db


def update_pv_dict_with_specific_yield(pv_dict):

    mapping = {pv_col1: "high_ratio", pv_col2: "low_ratio"}

    for pv_col in pv_dict.keys():

        db = get_data_from_db(mapping[pv_col])

        experiment_name = db[db[pv_col] > 1].filename_export.iat[0]

        exp = gcloud_read_experiment(
            collection=COLLECTION, experiment_id=experiment_name
        )

        for key in exp.components.keys():
            if "pv" in key:
                component = exp.components[key]
                if component.name in pv_col:
                    spec_yield_pv = (
                        sum(component.state["power [+]"]) / component.settings.installed
                    )

                    pv_dict[pv_col].update({"specific_yield": spec_yield_pv})

    for key in exp.components.keys():
        if "wind" in key:
            global tot_yield_wind
            tot_yield_wind = sum(exp.components[key].state["power [+]"])

    return None


def add_additional_data(experiment: str, force_refresh: bool = False):

    db = get_data_from_db(experiment=experiment, force_refresh=force_refresh)

    mapping = {
        "high_ratio": [pv_col1],
        "low_ratio": [pv_col2],
        "both_ratios": [pv_col2, pv_col3],
    }

    # curtailment
    db["curtailment"] = db["curtailment"].abs()

    # total generation uses the specific yield
    db["total_generation"] = 0
    for pv_col in mapping[experiment]:
        db["total_generation"] += db[pv_col] * pv_dict[pv_col]["specific_yield"]
    db["total_generation"] += tot_yield_wind

    db["relative_curtailment"] = db["curtailment"] / db["total_generation"] * 100

    # total installed capacity including 10 MW wind
    db["total_installed_capacity"] = 10
    for pv_col in mapping[experiment]:
        db["total_installed_capacity"] += db[pv_col]

    # AC PV power is a direct mapping
    db[pv_ac_col] = 0
    for pv_col in mapping[experiment]:
        db[pv_ac_col] += db[pv_col]

    # DC PV power is based on the DC ratio that increases the total deployed capacity
    db[pv_dc_col] = 0
    for pv_col in mapping[experiment]:
        db[pv_dc_col] += db[pv_col] * pv_dict[pv_col]["dc_ratio"]

    # battery storage power and energy capacity
    db["total_storage_energy"] = db[batcols].sum(axis=1)
    db["total_storage_power"] = (
        db[bat1_col]
        + db[bat2_col] / 2
        + db[bat4_col] / 4
        + db[bat6_col] / 6
        + db[bat8_col] / 8
        + db[bat12_col] / 12
    )
    db["pv_cost_ac"] = db["pv_cost"] * pv_dict[mapping[experiment][0]]["dc_ratio"]

    # switch that determines the ratio between PV and wind
    switch = lambda x: "<1" if x < 1 else ">1"
    db["ratio"] = [switch(x) for x in db[pv_col] / 10]

    db.to_pickle(RESOURCE_FOLDER / f"{experiment}_additional.pkl")


#%%
if __name__ == "__main__":
    update_pv_dict_with_specific_yield(pv_dict=pv_dict)

    for experiment in experiments:
        add_additional_data(experiment=experiment)
