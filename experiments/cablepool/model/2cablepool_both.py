#%%
from LESO import System
from LESO.components import PhotoVoltaic
from pathlib import Path

FOLDER = Path(__file__).parent
date_from = "2019-01-01"
date_to = "2019-12-31"

#%%
system = System.read_pickle("cablepooling_paper.pkl")

for c in system.components:
    if isinstance(c, PhotoVoltaic):

        if "low" in c.name:
            c.dof = True  # True == DOF
            c.installed = 1  # 1 == DOF

            print(f"Enabled {c.name} as optimization variable")

        if "high" in c.name:
            c.dof = True  # True == DOF
            c.installed = 1  # 1 == DOF

            print(f"Enabled {c.name} as optimization variable")

filename = system.name.lower() + "_both.pkl"
system.to_pickle(FOLDER / filename)
