# %%
import pandas as pd
import numpy as np
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

from cablepool_postprocess_data import (
    total_bat_col,
    pv_dc_col,
)
from LESO.plotting import default_matplotlib_save, default_matplotlib_style
from LESO.plotting import crop_transparency_top_bottom


#%% constants
FOLDER = Path(__file__).parent
RESULT_FOLDER = FOLDER.parent / "results"
RESOURCE_FOLDER = FOLDER / "resources"


#%% open loop for all experiments

from cablepool_postprocess_data import experiments

for experiment in experiments:

    dataset_filename = f"{experiment}_additional.pkl"
    IMAGE_FOLDER = FOLDER / "images" / experiment
    IMAGE_FOLDER.mkdir(exist_ok=True, parents=True)

    # read in data
    df = pd.read_pickle(RESOURCE_FOLDER / dataset_filename)

    ##  fig (3) [a] PV deployment vs PV cost with battery Z-index -----------------------------------------------------

    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)
    fig.set_size_inches(6, 2.2)
    sns.scatterplot(
        x="pv_cost",
        y=pv_dc_col,
        size=total_bat_col,
        hue=total_bat_col,
        data=df,
        palette="Greens",
        ax=ax,
        edgecolor="black",
    )

    ax.set_ylabel("deployed PV\ncapacity (MWp)")
    ax.set_xlabel("PV capacity cost (€/kWp)")

    ax.legend(frameon=False, title="deployed battery capacity (MWh)")

    default_matplotlib_save(fig, IMAGE_FOLDER / "pv_deployment_vs_cost_z_battery.png")

    ##  fig (3) [b] PV deployment vs PV cost with battery Z-index  ------------------------------------------------------

    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)
    fig.set_size_inches(6, 2.2)
    sns.scatterplot(
        x="battery_cost",
        y=total_bat_col,
        size=pv_dc_col,
        hue=pv_dc_col,
        data=df,
        palette="YlOrBr",
        ax=ax,
        edgecolor="black",
    )

    ax.set_ylabel("deployed battery capacity (MWh)")
    ax.set_xlabel("battery energy capacity cost (€/kWh)")

    ax.legend(frameon=False, title="deployed PV\ncapacity (MWp)")

    default_matplotlib_save(fig, IMAGE_FOLDER / "battery_deployment_vs_cost_z_pv.png")

    ##  fig (4) [a] battery cost vs PV cost with PV Z-index  ------------------------------------------------------

    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)
    fig.set_size_inches(5, 3)

    sns.scatterplot(
        x="pv_cost",
        y="battery_cost",
        size=pv_dc_col,
        hue=pv_dc_col,
        data=df,
        palette="YlOrBr",
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
        title="Deployed PV capacity (MWp)",
        ncol=6,
    )
    default_matplotlib_save(fig, IMAGE_FOLDER / "bat_cost_vs_pv_cost_z_pv.png")

    ##  fig (4) [b] battery cost vs PV cost with battery Z-index  ------------------------------------------------------

    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)
    fig.set_size_inches(5, 3)

    sns.scatterplot(
        x="pv_cost",
        y="battery_cost",
        size=total_bat_col,
        hue=total_bat_col,
        data=df,
        palette="Greens",
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
        title="deployed battery capacity (MWh)",
        ncol=6,
    )
    default_matplotlib_save(fig, IMAGE_FOLDER / "bat_cost_vs_pv_cost_z_battery.png")

    ##  fig (5) [a] relative curtailment vs additional PV Z index battery ------------------------------------------------------
    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)
    fig.set_size_inches(3, 3)

    sns.scatterplot(
        x=pv_dc_col,
        y="relative_curtailment",
        hue=total_bat_col,
        data=df,
        palette="Greens",
        ax=ax,
        edgecolor="black",
    )

    ax.set_xlabel("additional PV capacity (MWp)")
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
        fig, IMAGE_FOLDER / "rel_curtailment_vs_PV_deployment_z_battery.png"
    )

    relplot_ticks = ax.get_xticks()
    relplot_labels = ax.get_xticklabels()

    ##  fig (5) [b] absolute curtailment vs additional PV Z index battery ------------------------------------------------------

    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)
    fig.set_size_inches(3, 3)

    sns.scatterplot(
        x=pv_dc_col,
        y="curtailment",
        hue=total_bat_col,
        data=df,
        palette="Greens",
        ax=ax,
        edgecolor="black",
    )

    ax.set_xlabel("additional PV capacity (MWp)")
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

    default_matplotlib_save(fig, IMAGE_FOLDER / "abs_curtailment_vs_deployment.png")

    if False:
        crop_transparency_top_bottom(
            folder_to_crop=IMAGE_FOLDER, file_ext_to_crop="png", override_original=True
        )
