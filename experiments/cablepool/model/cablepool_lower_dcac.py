#%%
from LESO import System
from LESO.components import PhotoVoltaic
from pathlib import Path

FOLDER = Path(__file__).parent

#%%
system = System.read_pickle("cablepooling_paper.pkl")

for c in system.components:
    if isinstance(c, PhotoVoltaic):

        c.opex_ratio = 2.6 / 100
        c.name = "PV South (lower ratio)"

filename = system.name.lower() + "_lower_dcac.pkl"
system.to_pickle(FOLDER / filename)
