from cablepool_postprocess_data import costblocks, Costblock
from matplotlib.axes import Axes
import matplotlib.patheffects as pe


def plot_cost_boxes(
    ax: Axes, annotate=False, annotate_color="black", annotate_linestyle="--"
):
    """Plot the cost boxes on the given axis."""

    # draw a box for each cost block
    for costblock in costblocks:
        costblock: Costblock = costblock
        ymin, ymax = costblock.bat
        xmin, xmax = costblock.pv

        data_xmin, data_xmax = ax.get_xlim()
        data_range = data_xmax - data_xmin
        xmin_canvas = (xmin - data_xmin) / data_range
        xmax_canvas = (xmax - data_xmin) / data_range

        ax.axhspan(
            ymin=ymin,
            ymax=ymax,
            xmin=xmin_canvas,
            xmax=xmax_canvas,
            edgecolor="white",
            facecolor="none",
            linewidth=1.5,
            alpha=0.8,
        )
        ax.axhspan(
            ymin=ymin,
            ymax=ymax,
            xmin=xmin_canvas,
            xmax=xmax_canvas,
            edgecolor=annotate_color,
            facecolor="none",
            linestyle=annotate_linestyle,
            linewidth=1,
        )

        if annotate:
            year = costblock.year
            loc = ((xmax - xmin) / 2 + xmin, ymax + 0.1)
            ax.annotate(
                f"{year} range",
                xy=loc,
                ha="center",
                xytext=(0, 2),
                textcoords="offset points",
                color=annotate_color,
                fontsize=8,
                path_effects=[
                    pe.withStroke(linewidth=2, foreground="white", alpha=0.8)
                ],
            )
