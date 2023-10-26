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

## ADD COST
## ### PV - X - vline
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

## ### Battery - Y - hline
for year, mean in BAT_COST_DICT.items():
    ax.axhline(
        y=mean,
        color="gray",
        linestyle="--",
    )
    x = ax.get_xlim()[-1]
    ax.annotate(
        f"{year}",
        xy=(x, mean),
        ha="center",
        xytext=(0, 5),
        textcoords="offset points",
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

default_matplotlib_save(fig, IMAGE_FOLDER / "pv_cost_vs_bat_cost_z_low_dc_capacity.png")
## ADD COST
## ### PV - X - vline
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

## ### Battery - Y - hline
for year, mean in BAT_COST_DICT.items():
    ax.axhline(
        y=mean,
        color="gray",
        linestyle="--",
    )
    x = ax.get_xlim()[-1]
    ax.annotate(
        f"{year}",
        xy=(x, mean),
        ha="center",
        xytext=(0, 5),
        textcoords="offset points",
    )
