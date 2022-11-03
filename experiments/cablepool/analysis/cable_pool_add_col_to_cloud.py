#%%
from LESO.experiments.analysis import gdatastore_results_to_df
from LESO.dataservice.google import datastore_query, datastore_put_entry, DSCLIENT
import pandas as pd

COLLECTION = "cablepooling_paper"
RUN_IDS = [
    "220806_cablepooling_bothdcs",
    "220725_cablepooling_1024",
]

#%%


gdf = pd.DataFrame(
    columns=[
        "run_id",
        "shape",
        "PV South (lower ratio) installed capacity",
        "PV South installed capacity",
        "PV high DC ratio installed capacity",
        "PV low DC ratio installed capacity",
    ]
)

for idx, run_id in enumerate(RUN_IDS):
    df = gdatastore_results_to_df(
        collection=COLLECTION, filters=[("run_id", "=", run_id)]
    )

    dicto = {
        "run_id": run_id,
        "shape": df.shape,
    }
    for key, value in (
        df[[col for col in df.columns if "PV" in col]].sum().to_dict().items()
    ):
        dicto.update({key: value})

    gdf.at[idx, :] = dicto

#%%
run_id = "220725_cablepooling_1024"
q = datastore_query(kind=COLLECTION, filters=[("run_id", "=", run_id)])

# high_dc
# low_dc
# both_dc

entities = []
for entity in q:
    entity["experiment"] = "high_dc"
    entities.append(entity)

# gcloud maxes put_multi to 500 entities in a single call
while len(entities) > 500:
    entities_to_put, entities = entities[:500], entities[500:]
    print(len(entities_to_put), len(entities))

    DSCLIENT.put_multi(entities_to_put)
# push last set after chopped down
DSCLIENT.put_multi(entities)

#%% Get the both dc data set
run_id = "220806_cablepooling_bothdcs"
q = datastore_query(kind=COLLECTION, filters=[("run_id", "=", run_id)])
df = pd.DataFrame(q)


#%%

df2 = df.sort_values(
    [
        "pv_cost",
        "battery_cost",
        "PV low DC ratio installed capacity",
        "PV high DC ratio installed capacity",
    ],
)
df2["experiment"] = [*["both_dc", "low_dc"] * 1024]
df2[
    [
        "pv_cost",
        "battery_cost",
        "PV low DC ratio installed capacity",
        "PV high DC ratio installed capacity",
        "experiment",
    ]
].to_excel("inspect2.xlsx")


#%%
entities = []

for index, (experiment, logfile) in df2[["experiment", "logfile"]].iterrows():

    q = datastore_query(
        kind=COLLECTION,
        filters=[
            ("run_id", "=", run_id),
            ("logfile", "=", logfile),
        ],
    )

    entity = next(q)
    entity["experiment"] = experiment
    entities.append(entity)


#%%
# gcloud maxes put_multi to 500 entities in a single call
while len(entities) > 500:
    entities_to_put, entities = entities[:500], entities[500:]
    print(len(entities_to_put), len(entities))

    DSCLIENT.put_multi(entities_to_put)
# push last set after chopped down
DSCLIENT.put_multi(entities)