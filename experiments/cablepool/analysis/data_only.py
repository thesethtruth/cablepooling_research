# %%
import pandas as pd
from pathlib import Path

# %% constants
FOLDER = Path(__file__).parent
RESULT_FOLDER = FOLDER.parent / "results"
RESOURCE_FOLDER = FOLDER / "resources"
PV_COST_RANGE = (170, 420)
BATTERY_ENERGY_COST_RANGE = (46, 299)
BATTERY_POWER_COST_RANGE = (40, 510)


# %% open loop for all PV_ts

from cablepool_postprocess_data import experiments

dfs = []
# experiments
for experiment in experiments:
    dataset_filename = f"{experiment}_additional.pkl"

    # read in data
    df = pd.read_pickle(RESOURCE_FOLDER / dataset_filename)
    df["pv_cost"] = df["pv_cost"] * 1000
    df["battery_cost"] = df["battery_cost"] * 1000
    dfs.append(df)

# %%

mid_prices = {
    "pv": {
        "2020": 398,
        "2030": 266,
        "2050": 199,
    },
    "battery": {
        "2020": 367,
        "2030": 222,
        "2050": 105,
    },
}

YEARS = ["2020", "2030", "2050"]
TECHS = ["pv", "battery"]


def get_closest_id(df, pv_cost, battery_cost):
    distance = abs(df["pv_cost"] - pv_cost) + abs(df["battery_cost"] - battery_cost)
    return df.loc[distance.idxmin(), "filename_export"]


for df in dfs:
    selected_ids = {
        experiment: {
            year: get_closest_id(
                df,
                mid_prices["pv"][year],
                mid_prices["battery"][year],
            )
            for year in YEARS
        }
        for experiment in experiments
    }

import json

with open(RESOURCE_FOLDER / "selected_ids.json", "w") as f:
    json.dump(selected_ids, f, indent=2)
