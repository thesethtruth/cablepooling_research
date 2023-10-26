# %%
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import lines
import numpy as np


from cablepool_postprocess_data import (
    total_bat_col,
    pv_dc_col,
)
from cablepool_postprocess_data import pv_col1 as high_dc_pv_col
from cablepool_postprocess_data import pv_col2 as low_dc_pv_col
from util import plot_cost_boxes

from LESO.plotting import default_matplotlib_save, default_matplotlib_style
from LESO.plotting import crop_transparency_top_bottom


# %% constants
FOLDER = Path(__file__).parent
RESULT_FOLDER = FOLDER.parent / "results"
RESOURCE_FOLDER = FOLDER / "resources"
PV_COST_RANGE = (170, 420)
BATTERY_ENERGY_COST_RANGE = (46, 299)
BATTERY_POWER_COST_RANGE = (40, 510)


# %% helper functions
def energy_cost_to_power_cost(value):
    min, max = BATTERY_ENERGY_COST_RANGE
    map_min, map_max = BATTERY_POWER_COST_RANGE

    frac = (value - min) / (max - min)
    m_value = frac * (map_max - map_min) + map_min

    return m_value


def determine_cost_for_battery_config(
    energy_cost: float, storage_duration: int
) -> float:
    power_cost = energy_cost_to_power_cost(energy_cost)
    cost_per_kwh = (storage_duration * energy_cost + power_cost) / storage_duration

    return np.round(cost_per_kwh)


from functools import partial

twiny_energy_cost_for_2h_battery = partial(
    determine_cost_for_battery_config, storage_duration=2
)

twiny_energy_cost_for_6h_battery = partial(
    determine_cost_for_battery_config, storage_duration=6
)

# %% open loop for all PV_ts

from cablepool_postprocess_data import experiments, PV_COST_DICT, BAT_COST_DICT

# experiments
for experiment in experiments:
    dataset_filename = f"{experiment}_additional.pkl"
    IMAGE_FOLDER = FOLDER / "images" / experiment
    IMAGE_FOLDER.mkdir(exist_ok=True, parents=True)

    # read in data
    df = pd.read_pickle(RESOURCE_FOLDER / dataset_filename)
    df["pv_cost"] = df["pv_cost"] * 1000
    df["battery_cost"] = df["battery_cost"] * 1000

    ##  fig (3) [a] PV deployment vs PV cost with battery Z-index -----------------------------------------------------

    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)
    fig.set_size_inches(6, 4)
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

    ax.legend(
        bbox_to_anchor=(0.5, -0.2),
        loc=9,
        borderaxespad=0.0,
        frameon=True,
        title="deployed battery capacity (MWh)",
        ncol=6,
    )

    # ### ADD COST
    _cost_dict = PV_COST_DICT[experiment]
    for year, mean in _cost_dict.items():
        ax.axvline(
            x=mean,
            color="gray",
            linestyle="--",
        )
        y = ax.get_ylim()[-1]
        ax.annotate(
            f"{year}",
            xy=(mean, y),
            ha="center",
            xytext=(0, 5),
            textcoords="offset points",
        )

    default_matplotlib_save(fig, IMAGE_FOLDER / "pv_deployment_vs_cost_z_battery.png")

    ##  fig (3) [b] battery deployment vs battery cost with PV Z-index  ------------------------------------------------------

    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)
    ax2 = ax.twiny()

    fig.set_size_inches(6, 4)
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

    bottom_xticks = ax.get_xticks()[1:-1]
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(bottom_xticks)
    ax2.set_xticklabels(twiny_energy_cost_for_6h_battery(bottom_xticks))
    ax2.set_xlabel("2h battery capacity cost (€/kWh)")

    ax.legend(
        bbox_to_anchor=(0.5, -0.2),
        loc=9,
        borderaxespad=0.0,
        frameon=True,
        title="deployed PV capacity (MWp)",
        ncol=6,
    )

    ### ADD COST
    for year, mean in BAT_COST_DICT.items():
        ax.axvline(
            x=mean,
            color="gray",
            linestyle="--",
        )
        y = ax.get_ylim()[-1]
        ax.annotate(
            f"{year}",
            xy=(mean, y),
            ha="center",
            xytext=(0, 1),
            textcoords="offset points",
        )
    default_matplotlib_save(fig, IMAGE_FOLDER / "battery_deployment_vs_cost_z_pv.png")

    # ##  fig (4) [a] battery cost vs PV cost with PV Z-index  ------------------------------------------------------

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

    ax.set_ylabel("battery energy\ncapacity cost (€/kWh)")
    ax.set_xlabel("PV capacity cost (€/kWp)")
    ax.legend(
        bbox_to_anchor=(0.5, -0.4),
        loc=9,
        borderaxespad=0.0,
        frameon=True,
        title="deployed PV capacity (MWp)",
        ncol=6,
    )
    ### ADD COST
    plot_cost_boxes(ax=ax)

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

    ax.set_ylabel("battery energy\ncapacity cost (€/kWh)")
    ax.set_xlabel("PV capacity cost (€/kWp)")
    ax.legend(
        bbox_to_anchor=(0.5, -0.4),
        loc=9,
        borderaxespad=0.0,
        frameon=True,
        title="deployed battery capacity (MWh)",
        ncol=6,
    )

    ## ADD COST
    plot_cost_boxes(ax=ax)

    default_matplotlib_save(fig, IMAGE_FOLDER / "bat_cost_vs_pv_cost_z_battery.png")

    # ##  fig (5) [a] relative curtailment vs additional PV Z index battery ------------------------------------------------------
    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)
    fig.set_size_inches(4, 3)

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
    ax.set_ylabel("relative\ncurtailment (%)")

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
    fig.set_size_inches(4, 3)

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

    ## Fig X1  - additional figure add_fig_battery_cost_vs_storage_duration_z_battery
    # %%
    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)

    fig.set_size_inches(6, 4)
    sns.scatterplot(
        x="battery_cost",
        y="average_storage_duration",
        size=total_bat_col,
        hue=total_bat_col,
        data=df,
        palette="Greens",
        ax=ax,
        edgecolor="black",
    )

    ax.set_ylabel("storage duration (h)")
    ax.set_xlabel("battery energy capacity cost (€/kWh)")

    ax.legend(
        bbox_to_anchor=(0.5, -0.2),
        loc=9,
        borderaxespad=0.0,
        frameon=True,
        title="deployed battery capacity (MWh)",
        ncol=6,
    )

    ## ADD COST
    for year, mean in BAT_COST_DICT.items():
        ax.axvline(
            x=mean,
            color="gray",
            linestyle="--",
        )
        y = ax.get_ylim()[-1]
        ax.annotate(
            f"{year}",
            xy=(mean, y),
            ha="center",
            xytext=(0, 5),
            textcoords="offset points",
        )

    default_matplotlib_save(
        fig, IMAGE_FOLDER / "add_fig_battery_cost_vs_storage_duration_z_battery.png"
    )

    ## Fig X1  - additional figure add_fig_deployed_battery_vs_storage_duration_z_PV
    # %%
    fig, ax = plt.subplots()
    fig, ax = default_matplotlib_style(fig, ax)

    fig.set_size_inches(6, 4)
    sns.scatterplot(
        x=total_bat_col,
        y="average_storage_duration",
        size=pv_dc_col,
        hue=pv_dc_col,
        data=df,
        palette="YlOrBr",
        ax=ax,
        edgecolor="black",
    )

    ax.set_ylabel("storage duration (h)")
    ax.set_xlabel("deployed battery capacity (MWh)")

    ax.legend(
        bbox_to_anchor=(0.5, -0.2),
        loc=9,
        borderaxespad=0.0,
        frameon=True,
        title="deployed PV capacity (MWp)",
        ncol=6,
    )

    default_matplotlib_save(
        fig, IMAGE_FOLDER / "add_fig_deployed_battery_vs_storage_duration_z_PV.png"
    )

    # DC ratio plots for only both ratio experiments
    if experiment == "both_ratios":

        vmin, vmax = 1.4, 2
        cmap = sns.color_palette(palette="YlOrBr", as_cmap=True)
        norm = plt.Normalize(vmin=vmin, vmax=vmax)
        lp = lambda i: plt.plot([], color=cmap(norm(i)), marker="o", ls="", ms=10)[0]
        labels = [round(i, 1) for i in np.arange(vmin, vmax, 0.2)]
        h = [lp(i) for i in labels]

        fig, ax = plt.subplots()
        fig, ax = default_matplotlib_style(fig, ax)

        fig.set_size_inches(6, 4)
        df["effective_dc_ratio"] = (
            df[high_dc_pv_col] * 2 + df[low_dc_pv_col] * 1.4
        ) / (df[high_dc_pv_col] + df[low_dc_pv_col])
        sns.scatterplot(
            x="pv_cost",
            y="battery_cost",
            size="effective_dc_ratio",
            hue="effective_dc_ratio",
            data=df,
            palette="YlOrBr",
            ax=ax,
            edgecolor="black",
            vmin=vmin,
            vmax=vmax,
        )

        ax.set_ylabel("battery energy\ncapacity cost (€/kWh)")
        ax.set_xlabel("PV capacity cost (€/kWp)")

        ax.legend(
            bbox_to_anchor=(0.5, -0.2),
            loc=9,
            borderaxespad=0.0,
            frameon=True,
            title="effective DC/AC ratio (MWp/MW)",
            ncol=6,
            labels=labels,
            handles=h,
        )
        plot_cost_boxes(ax=ax, header_height=0.6)
        default_matplotlib_save(
            fig, IMAGE_FOLDER / "bat_cost_vs_pv_cost_vs_z_dc_ratio.png"
        )

    if True:
        crop_transparency_top_bottom(
            folder_to_crop=IMAGE_FOLDER, file_ext_to_crop="png", override_original=True
        )
