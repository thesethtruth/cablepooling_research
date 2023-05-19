# %%
import pandas as pd
import numpy as np
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import lines


from cablepool_postprocess_data import (
    total_bat_col,
    pv_dc_col,
)
from cablepool_postprocess_data import pv_col1 as high_dc_pv_col
from cablepool_postprocess_data import pv_col2 as low_dc_pv_col

from LESO.plotting import default_matplotlib_save, default_matplotlib_style
from LESO.plotting import crop_transparency_top_bottom


#%% constants
FOLDER = Path(__file__).parent
RESULT_FOLDER = FOLDER.parent / "results"
RESOURCE_FOLDER = FOLDER / "resources"
PV_COST_RANGE = (170, 420)
BATTERY_ENERGY_COST_RANGE = (46, 299)
BATTERY_POWER_COST_RANGE = (40, 510)

#%% helper functions
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

    return np.round(cost_per_kwh, 2)


from functools import partial

twiny_energy_cost_for_2h_battery = partial(
    determine_cost_for_battery_config, storage_duration=2
)

twiny_energy_cost_for_6h_battery = partial(
    determine_cost_for_battery_config, storage_duration=6
)

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

    ### ADD COST
    ax.axvline(y=0, color='black', linestyle='--')
    # Create line object for legend
    line = lines.Line2D([], [], color='black', linestyle='--', label='Zero line')

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
    ax.axvline(y=0, color='black', linestyle='--')
    # Create line object for legend
    line = lines.Line2D([], [], color='black', linestyle='--', label='Zero line')
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



    default_matplotlib_save(fig, IMAGE_FOLDER / "bat_cost_vs_pv_cost_z_battery.png")

    ##  fig (5) [a] relative curtailment vs additional PV Z index battery ------------------------------------------------------
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
    #%%
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

    ### ADD COST
    ax.axvline(y=0, color='black', linestyle='--')
    # Create line object for legend
    line = lines.Line2D([], [], color='black', linestyle='--', label='Zero line')

    default_matplotlib_save(
        fig, IMAGE_FOLDER / "add_fig_battery_cost_vs_storage_duration_z_battery.png"
    )

    ## Fig X1  - additional figure add_fig_deployed_battery_vs_storage_duration_z_PV
    #%%
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

        fig, ax = plt.subplots()
        fig, ax = default_matplotlib_style(fig, ax)

        fig.set_size_inches(6, 4)
        sns.scatterplot(
            x="pv_cost",
            y="battery_cost",
            size=high_dc_pv_col,
            hue=high_dc_pv_col,
            data=df,
            palette="YlOrBr",
            ax=ax,
            edgecolor="black",
        )

        ax.set_ylabel("battery energy\ncapacity cost (€/kWh)")
        ax.set_xlabel("PV capacity cost (€/kWp)")

        ax.legend(
            bbox_to_anchor=(0.5, -0.2),
            loc=9,
            borderaxespad=0.0,
            frameon=True,
            title="deployed PV capacity (MWp)\n(high DC ratio)",
            ncol=6,
        )

        default_matplotlib_save(
            fig, IMAGE_FOLDER / "pv_cost_vs_bat_cost_z_high_dc_capacity.png"
        )
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        fig, ax = plt.subplots()
        fig, ax = default_matplotlib_style(fig, ax)

        fig.set_size_inches(6, 4)
        sns.scatterplot(
            x="pv_cost",
            y="battery_cost",
            size=low_dc_pv_col,
            hue=low_dc_pv_col,
            data=df,
            palette="YlOrBr",
            ax=ax,
            edgecolor="black",
        )

        ax.set_ylabel("battery energy\ncapacity cost (€/kWh)")
        ax.set_xlabel("PV capacity cost (€/kWp)")

        ax.legend(
            bbox_to_anchor=(0.5, -0.2),
            loc=9,
            borderaxespad=0.0,
            frameon=True,
            title="deployed PV capacity (MWp)\n(low DC ratio)",
            ncol=6,
        )

        default_matplotlib_save(
            fig, IMAGE_FOLDER / "pv_cost_vs_bat_cost_z_low_dc_capacity.png"
        )

    if True:
        crop_transparency_top_bottom(
            folder_to_crop=IMAGE_FOLDER, file_ext_to_crop="png", override_original=True
        )
