#%%
from pathlib import Path

import pandas as pd

from LESO import FinalBalance, Grid, Lithium, PhotoVoltaic, System, Wind
from LESO.leso_logging import log_to_stderr

log_to_stderr()

#%%
FOLDER = Path(__file__).parent

#%% Define system and components
modelname = "cablepooling_paper"
lat, lon = 51.89, 5.85  # Nijmegen
date_from = "2019-01-01"
date_to = "2019-12-31"

price_filename = "etm_pricecurve.csv"
retail_prices = pd.read_csv(FOLDER / price_filename, index_col=0)
retail_prices = list(
    (retail_prices / 1e6).T.values[0]
)  # convert from eu/MWh to M eu/MWh

# initiate System component
system = System(lat=lat, lon=lon, model_name=modelname)

#%%
grid = Grid(
    "Grid connection",
    installed=10,
    variable_cost=retail_prices,
    variable_income=retail_prices,
)
wind = Wind(
    "Nordex N100 2500",
    dof=False,
    installed=10,
    turbine_type="Nordex N100 2500",  # actually Lagerwey L100 2.5 MW, best match
    hub_height=100,
    use_ninja=True,
    date_from=date_from,
    date_to=date_to,
)
pv_high = PhotoVoltaic(
    "PV high DC ratio",
    azimuth=180,
    use_ninja=True,
    dof=True,
    date_from=date_from,
    date_to=date_to,
    lifetime=40,
    opex_ratio=0.023,
    dcac_ratio=2,
    capex={"DC": 0.2},
)
pv_low = PhotoVoltaic(
    "PV low DC ratio",
    azimuth=180,
    use_ninja=True,
    dof=False,  # False  ---!
    installed=0,  # also zero  ---! --> disabled
    date_from=date_from,
    date_to=date_to,
    lifetime=40,
    opex_ratio=2.6 / 100,  # unique for this value
    dcac_ratio=1 / 0.7,  # ACDC ratio 0.7
    capex={"DC": 0.2},
)
bat_1h = Lithium("1h battery", dof=True, EP_ratio=1)
bat_2h = Lithium("2h battery", dof=True, EP_ratio=2)
bat_4h = Lithium("4h battery", dof=True, EP_ratio=4)
bat_6h = Lithium("6h battery", dof=True, EP_ratio=6)
bat_8h = Lithium("8h battery", dof=True, EP_ratio=8)
bat_12h = Lithium("12h battery", dof=True, EP_ratio=12)
final = FinalBalance(name="curtailment_underload")

component_list = [
    pv_high,
    pv_low,
    wind,
    bat_1h,
    bat_2h,
    bat_4h,
    bat_6h,
    bat_8h,
    bat_12h,
    final,
    grid,
]

#%%
# update the values to new values from DEA
for c in component_list:

    if isinstance(c, Lithium):
        c.capex_storage = 0.046
        c.capex_power = 40e-3
        c.cycle_efficieny = 0.92
        c.discharge_rate = 0.999958
        c.lifetime = 25
        c._opex = 0.54e-3 / c.EP_ratio
        c.variable_cost = 1.8e-6

#%% add the components to the system
system.add_components(component_list)
#%% Pickle the model

if __name__ == "__main__":
    ## Solve
    if False:
        system.optimize(
            objective="osc",  # overnight system cost
            time=None,  # resorts to default; year 8760h
            store=True,  # write-out to json
            solver="gurobi",  # default solver
            filepath="here.json",
            nonconvex=False,  # solver option (warning will show if needed)
            solve=True,  # solve or just create model
        )
    ## Or write to pickle
    else:
        filename = modelname.lower() + ".pkl"
        system.to_pickle(FOLDER / filename)
