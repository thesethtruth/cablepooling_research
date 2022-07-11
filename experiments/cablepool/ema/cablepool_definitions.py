#%% cablepool_definitions.py
from pathlib import Path
import LESO
from google.cloud.exceptions import Conflict

#%%

COLLECTION = "cablepooling_paper"
OUTPUT_PREFIX = f"{COLLECTION}_exp_"


MODEL_FOLDER = Path(__file__).parent.parent / "model"
RESULTS_FOLDER = Path(__file__).parent.parent / "results"
RESULTS_FOLDER.mkdir(parents=True, exist_ok=True)

# create bucket if not already exist
if True:
    try:
        LESO.dataservice.google.cloud_create_bucket(COLLECTION)
    except Conflict as c:
        print(c)

MODEL = MODEL_FOLDER / "model.pkl"

METRICS = [
    # components
    "PV South installed capacity",
    "PV West installed capacity",
    "PV East installed capacity",
    "Nordex N100 2500 installed capacity",
    "2h battery installed capacity",
    "6h battery installed capacity",
    "10h battery installed capacity",
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
def linear_map_2030(value):
    min, max = 0.41, 0.70  # @@
    map_min, map_max = 0.42, 0.81  # @@

    frac = (value - min) / (max - min)
    m_value = frac * (map_max - map_min) + map_min

    return m_value


# for the linear map in 2050, we return the same value
def linear_map_2050(value):
    return value


if __name__ == "__main__":
    # use this to easily generate the metrics for installed capacity
    if True:
        ref_system = LESO.System.read_pickle(MODEL)
        m = []
        for c in ref_system.components:
            if not isinstance(c, (LESO.FinalBalance, LESO.ETMdemand)):
                out = c.name + " installed capacity"
                m.append(out)
                print(m)
