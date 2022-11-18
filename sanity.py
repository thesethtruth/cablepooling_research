#%%
import pandas as pd
from typing import Tuple, List
import os
import json
from google.cloud import datastore
from google.cloud import storage
from pathlib import Path
import numpy as np

path = str(
    (Path(__file__).parent / "LESO" / "LESO" / "dataservice" / "gkey.json").absolute()
)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path
DSCLIENT = datastore.Client()
CSCLIENT = storage.Client()


def cloud_fetch_blob_as_dict(
    bucket_name: str,
    blob_name: str,
):
    """download a blob (as dict) from google cloud store"""
    bucket = CSCLIENT.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    return json.loads(blob.download_as_string())


def gcloud_read_experiment(
    collection: str,
    experiment_id: str,
) -> dict:
    """read an experiment id (previously the json filename) from gcloud as AttrDict
    collection == bucket_name
    experiment_id == blob_name
    """
    return cloud_fetch_blob_as_dict(bucket_name=collection, blob_name=experiment_id)


COLLECTION = "cablepooling_paper"

experiment = gcloud_read_experiment(
    collection=COLLECTION, experiment_id="cablepooling_paper_exp_204818674930076.json"
)

#%%
from LESO import AttrDict

experiment = AttrDict(experiment)

for c_name, values in experiment.components.items():

    if "4h" in c_name:

        df = pd.DataFrame.from_dict(values.state, orient="columns")
        print(c_name)

df.rename(
    {
        "energy": "energy",
        "losses": "losses",
        "power [+]": "power_pos",
        "power [-]": "power_neg",
    },
    axis=1,
    inplace=True,
)

df["net_charging"] = df.apply(
    lambda row: row.power_neg + row.losses
    if row.power_neg < 0
    else row.power_pos - row.losses,
    axis=1,
)
import matplotlib.pyplot as plt

df["relative_losses"] = df.losses / (df.power_pos - df.power_neg)
df["relative_losses"] = df["relative_losses"].mask(df.relative_losses == np.inf, 0)
df["relative_losses"] = df["relative_losses"].mask(pd.isna(df.relative_losses), 0)

#%%
fig, ax = plt.subplots(figsize=(8, 10))
df.loc[:120].plot(ax=ax)
fig.savefig("output.jpg")
