#%%
from LESO import System
from LESO.components import PhotoVoltaic
from pathlib import Path

FOLDER = Path(__file__).parent
date_from = "2019-01-01"
date_to = "2019-12-31"

#%%
system = System.read_pickle("cablepooling_paper.pkl")

pv2 = PhotoVoltaic(
    "PV South (lower ratio)",
    azimuth=180,
    use_ninja=True,
    dof=True,
    date_from=date_from,
    date_to=date_to,
    lifetime=40,
    opex_ratio=0.026,
    dcac_ratio=1/0.7,
    capex={"DC": 0.2},
)

system.add_components([pv2])
filename = system.name.lower() + "_both.pkl"
system.to_pickle(FOLDER / filename)
