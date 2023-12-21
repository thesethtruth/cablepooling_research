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
POINTS_HIGHLIGHT = {
    2020: {
        "color": "deepskyblue",
        "exp": "cablepooling_paper_v2_exp_168548892478198.json",
    },
    2030: {
        "color": "blue",
        "exp": "cablepooling_paper_v2_exp_110088832558956.json",
    },
    2050: {
        "color": "darkblue",
        "exp": "cablepooling_paper_v2_exp_215620213215519.json",
    },
}
HIGHLIGHT_MARKER_SIZE = 8
HIGHLIGHT_MARKER_EW = 2


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

    return [int(cost) for cost in cost_per_kwh]


from functools import partial

twiny_energy_cost_for_2h_battery = partial(
    determine_cost_for_battery_config, storage_duration=2
)

twiny_energy_cost_for_6h_battery = partial(
    determine_cost_for_battery_config, storage_duration=6
)


def add_highlight_points(ax, x_col, y_col, z_col, annotation=False, y_divider=1):
    dicto = POINTS_HIGHLIGHT
    for year, dicto in dicto.items():
        x = dicto["row"][x_col]
        y = dicto["row"][y_col] / y_divider

        ax.plot(
            x,
            y,
            markeredgecolor=dicto["color"],
            markerfacecolor="none",
            markeredgewidth=HIGHLIGHT_MARKER_EW,
            marker="o",
            markersize=HIGHLIGHT_MARKER_SIZE,
            zorder=10,
        )
        if annotation:
            ax.annotate(
                f"{year}",
                xy=(x, y),
                ha="center",
                xytext=(0, 5),
                textcoords="offset points",
                color=dicto["color"],
            )
    return ax


# %% open loop for all PV_ts

from cablepool_postprocess_data import experiments, PV_COST_DICT, BAT_COST_DICT

# experiments
for experiment in ["both_ratios"]:
    dataset_filename = f"{experiment}_additional.pkl"
    IMAGE_FOLDER = FOLDER / "images" / experiment
    IMAGE_FOLDER.mkdir(exist_ok=True, parents=True)

    # read in data
    df = pd.read_pickle(RESOURCE_FOLDER / dataset_filename)
    df["pv_cost"] = df["pv_cost"] * 1000
    df["battery_cost"] = df["battery_cost"] * 1000

    if experiment == "both_ratios":
        for year, dicto in POINTS_HIGHLIGHT.items():
            POINTS_HIGHLIGHT[year].update(
                {"row": df.query(f"filename_export == '{dicto['exp']}'")}
            )

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

    ax = add_highlight_points(
        ax=ax,
        x_col="pv_cost",
        y_col=pv_dc_col,
        z_col=total_bat_col,
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
            color="gray",
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

    ax = add_highlight_points(
        ax=ax,
        x_col="battery_cost",
        y_col=total_bat_col,
        z_col=pv_dc_col,
    )

    ax.set_ylabel("deployed battery capacity (MWh)")
    ax.set_xlabel("battery energy capacity cost (€/kWh)")

    bottom_xticks = ax.get_xticks()[1:-1]
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(bottom_xticks)
    ax2.set_xticklabels(twiny_energy_cost_for_6h_battery(bottom_xticks))
    ax2.set_xlabel("6h battery capacity cost (€/kWh)")

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
            ha="right",
            va="top",
            xytext=(-1, -1),
            textcoords="offset points",
            color="gray",
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
    ax = add_highlight_points(
        ax=ax,
        x_col="pv_cost",
        y_col="battery_cost",
        z_col=pv_dc_col,
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
    ax = add_highlight_points(
        ax=ax,
        x_col="pv_cost",
        y_col="battery_cost",
        z_col=total_bat_col,
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
    ax = add_highlight_points(
        ax=ax,
        x_col=pv_dc_col,
        y_col="relative_curtailment",
        z_col=total_bat_col,
    )

    ax.set_xlabel("deployed PV capacity (MWp)")
    ax.set_ylabel("relative\ncurtailment (%)")
    ax.ylim = (0, 21)
    ax.set_yticks([0, 5, 10, 15, 20])

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

    df["curtailment"] = df["curtailment"] / 1000

    sns.scatterplot(
        x=pv_dc_col,
        y="curtailment",
        hue=total_bat_col,
        data=df,
        palette="Greens",
        ax=ax,
        edgecolor="black",
    )
    ax = add_highlight_points(
        ax=ax,
        x_col=pv_dc_col,
        y_col="curtailment",
        z_col=total_bat_col,
        y_divider=1000,
    )

    ax.set_xlabel("deployed PV capacity (MWp)")
    ax.set_ylabel("absolute\ncurtailment (GWh)")

    ## set y ticks
    ax.ylim = (0, 16)
    ax.set_yticks([0, 5, 10, 15])

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
    ax = add_highlight_points(
        ax=ax,
        x_col="battery_cost",
        y_col="average_storage_duration",
        z_col=total_bat_col,
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
            color="gray",
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
    ax = add_highlight_points(
        ax=ax,
        x_col=total_bat_col,
        y_col="average_storage_duration",
        z_col=pv_dc_col,
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

        for year, dicto in POINTS_HIGHLIGHT.items():
            POINTS_HIGHLIGHT[year].update(
                {"row": df.query(f"filename_export == '{dicto['exp']}'")}
            )

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
        ax = add_highlight_points(
            ax=ax,
            x_col="pv_cost",
            y_col="battery_cost",
            z_col="effective_dc_ratio",
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

        ## FIG investment vs net profit vs ROI
        fig, ax = plt.subplots()
        fig, ax = default_matplotlib_style(fig, ax)
        fig.set_size_inches(6, 4)
        df["return_on_add_investment"] = df["return_on_add_investment"] * 100

        vmin, vmax = 8, 15
        cmap = sns.color_palette(palette="summer_r", as_cmap=True)
        norm = plt.Normalize(vmin=vmin, vmax=vmax)
        lp = lambda i: plt.plot([], color=cmap(norm(i)), marker="o", ls="", ms=10)[0]
        labels = [round(i, 1) for i in np.arange(vmin, vmax, 2)]
        h = [lp(i) for i in labels]

        vmin, vmax = 0, 14
        sns.scatterplot(
            x="total_investment_cost",
            y="net_profit_add_investment",
            hue="return_on_add_investment",
            data=df,
            palette="summer_r",
            ax=ax,
            edgecolor="black",
            vmin=vmin,
            vmax=vmax,
        )

        ax = add_highlight_points(
            ax=ax,
            x_col="total_investment_cost",
            y_col="net_profit_add_investment",
            z_col="return_on_add_investment",
        )

        ax.set_xlabel("total investment cost (M€)")
        ax.set_xticks(np.arange(22, 40, 2))
        ax.set_ylabel("net profit (M€)")

        ax.legend(
            bbox_to_anchor=(0.5, -0.2),
            loc=9,
            borderaxespad=0.0,
            frameon=True,
            title="ROI (%)",
            ncol=4,
            labels=labels,
            handles=h,
        )

        default_matplotlib_save(
            fig, IMAGE_FOLDER / "invest_cost_vs_net_profit_z_ROI.png"
        )

    if True:
        crop_transparency_top_bottom(
            folder_to_crop=IMAGE_FOLDER, file_ext_to_crop="png", override_original=True
        )
