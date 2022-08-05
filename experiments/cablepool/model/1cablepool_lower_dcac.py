#%%
from LESO import System
from LESO.components import PhotoVoltaic
from pathlib import Path

FOLDER = Path(__file__).parent

#%%
system = System.read_pickle("cablepooling_paper.pkl")

for c in system.components:
    if isinstance(c, PhotoVoltaic):

        if "low" in c.name:
            c.dof = True  # True == DOF
            c.installed = 1  # 1 == DOF

            print(f"Enabled {c.name} as optimization variable")

        if "high" in c.name:
            c.dof = False  # False  ---!
            c.installed = 0  # also zero  ---! --> disabled

            print(f"Disabled {c.name} as optimization variable")


filename = system.name.lower() + "_lower_dcac.pkl"
system.to_pickle(FOLDER / filename)
