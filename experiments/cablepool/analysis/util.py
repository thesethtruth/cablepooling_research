from cablepool_postprocess_data import costblocks, Costblock
from matplotlib.axes import Axes
import matplotlib.patheffects as pe


def plot_cost_boxes(
    ax: Axes,
    annotate=True,
    annotate_color="black",
    annotate_linestyle="--",
    header_height=1.1,
):
    """Plot the cost boxes on the given axis."""
    data_ymin, data_ymax = ax.get_ylim()
    data_xmin, data_xmax = ax.get_xlim()
    data_yrange = data_ymax - data_ymin
    data_xrange = data_xmax - data_xmin

    # draw a box for each cost block
    for costblock in costblocks:
        costblock: Costblock = costblock
        ymin, ymax = costblock.bat
        xmin, xmax = costblock.pv

        xmin_canvas = (xmin - data_xmin) / data_xrange
        xmax_canvas = (xmax - data_xmin) / data_xrange

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

            ax.axhspan(
                ymin=ymax,
                ymax=ymax + data_yrange / 12 * header_height,
                xmin=xmin_canvas,
                xmax=xmax_canvas,
                edgecolor="none",
                facecolor=annotate_color,
                alpha=0.7,
            )

            ax.annotate(
                f"{year}",
                xy=loc,
                ha="center",
                xytext=(0, 1),
                textcoords="offset points",
                fontsize=7,
                color="white"
                # path_effects=[
                #     pe.withStroke(linewidth=2, foreground="white", alpha=0.8)
                # ],
            )
