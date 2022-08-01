# %%
import pandas as pd
import numpy as np
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

from cablepool_postprocess_tools import (
    get_data_from_db,
    gcloud_read_experiment,
    pv_col,
    wind_col,
    bat1_col,
    bat2_col,
    bat4_col,
    bat6_col,
    bat8_col,
    bat12_col,
    total_bat_col,
    batcols,
)
from LESO.plotting import default_matplotlib_save, default_matplotlib_style

#%% constants
FOLDER = Path(__file__).parent
RESULT_FOLDER = FOLDER.parent / "results"
IMAGE_FOLDER = FOLDER / "images"
RESOURCE_FOLDER = FOLDER / "resources"

COLLECTION = "cablepooling_paper"
RUN_ID = "220725_cablepooling_1024"


#%% read in data
df = get_data_from_db(
    collection=COLLECTION,
    run_id=RUN_ID,
    force_refresh=False,
    # filter=filter,
)

exp = gcloud_read_experiment(
    collection=COLLECTION, experiment_id=df.filename_export.iat[23]
)

## solar deployment
subset = df[df[pv_col] != 0]
idx = subset[pv_col].argmin()
max_solar_price = subset.loc[subset.index[idx], "pv_cost"]
print(f"Solar deployment starts at: {round(max_solar_price,0)} €/kWp")

#%% Deployment vs absolut cost scatter

fig, ax = plt.subplots()
fig, ax = default_matplotlib_style(fig, ax)
fig.set_size_inches(6, 2.2)
sns.scatterplot(
    x="pv_cost",
    y=pv_col,
    size="curtailment",
    hue="curtailment",
    data=df,
    palette="Reds",
    ax=ax,
    edgecolor="black",
)

ax.set_ylabel("deployed PV\ncapacity (MW)")
ax.set_xlabel("PV capacity cost (€/kWp)")

ax.legend(frameon=False, title="Curtailment (MWh)")

default_matplotlib_save(
    fig, IMAGE_FOLDER / "paper_cablepool_init_pv_deployment_vs_cost.png"
)

#%% relative curtailment
fig, ax = plt.subplots()
fig, ax = default_matplotlib_style(fig, ax)
fig.set_size_inches(3, 3)

sns.scatterplot(
    x="total_installed_capacity",
    y="relative_curtailment",
    hue=total_bat_col,
    data=df,
    palette="Reds",
    ax=ax,
    edgecolor="black",
)

ax.set_xlabel("total deployed capacity (MW)")

ax.set_ylabel("relative curtailment (%)")

ax.legend(
    bbox_to_anchor=(0.5, -0.35),
    loc=9,
    borderaxespad=0.0,
    frameon=True,
    title="deployed battery capacity (MWh)",
    ncol=3,
)

default_matplotlib_save(
    fig, IMAGE_FOLDER / "paper_cablepool_rel_curtailment_vs_deployment.png"
)

relplot_ticks = ax.get_xticks()
relplot_labels = ax.get_xticklabels()

#%% absolute curtailment
fig, ax = plt.subplots()
fig, ax = default_matplotlib_style(fig, ax)
fig.set_size_inches(3, 3)

sns.scatterplot(
    x="total_installed_capacity",
    y="curtailment",
    hue=total_bat_col,
    data=df,
    palette="Reds",
    ax=ax,
    edgecolor="black",
)


ax.set_xlabel("total deployed capacity (MW)")
ax.set_xticks(relplot_ticks)
ax.set_xticklabels(relplot_labels)
ax.set_ylabel("curtailment (MWh)")

ax.legend(
    bbox_to_anchor=(0.5, -0.35),
    loc=9,
    borderaxespad=0.0,
    frameon=True,
    title="deployed battery capacity (MWh)",
    ncol=3,
)

default_matplotlib_save(
    fig, IMAGE_FOLDER / "paper_cablepool_abs_curtailment_vs_deployment.png"
)
#%% bi-variate scatterplot

fig, ax = plt.subplots()
fig, ax = default_matplotlib_style(fig, ax)
fig.set_size_inches(5, 3)

sns.scatterplot(
    x="pv_cost",
    y="battery_cost",
    size=pv_col,
    hue=pv_col,
    data=df,
    palette="Reds",
    sizes=(10, 40),
    ax=ax,
    edgecolor="black",
)

ax.set_ylabel("battery power\ncapacity cost (€/kW)")
ax.set_xlabel("PV capacity cost (€/kWp)")
ax.legend(
    bbox_to_anchor=(0.5, -0.4),
    loc=9,
    borderaxespad=0.0,
    frameon=True,
    title="Deployed PV capacity (MW)",
    ncol=6,
)

default_matplotlib_save(
    fig, IMAGE_FOLDER / "paper_cablepool_init_bivariate_deployment.png"
)
# %%
timeseries = exp.components.pv2.state["power [+]"]
timeseries = [i / max(timeseries) for i in timeseries]

fig, ax = plt.subplots()
fig, ax = default_matplotlib_style(fig, ax)
fig.set_size_inches(4, 2)
ax.hist(
    timeseries,
    color="firebrick",
    alpha=0.5,
    bins=30,
)
ax.legend(frameon=False)
ax.set_ylabel("frequency (h/y)")
ax.set_ylim([0, 500])
ax.set_xlabel("capacity factor [-]")
ax.set_xlim([0, 1])
default_matplotlib_save(fig, IMAGE_FOLDER / "paper_cablepool_PV_histogram.png")

#%%
if input("Crop the images in this folder? [y/n]") == "y":
    from LESO.plotting import crop_transparency_top_bottom

    crop_transparency_top_bottom(
        folder_to_crop=IMAGE_FOLDER, file_ext_to_crop="png", override_original=True
    )
