# Takenlijst figuurtjes

Er zijn 3 experimenten, met 2 `run_id`s

| Experiment beschrijving | `run_id`                                    | `pv_cols`                                                                    | `dc_ratio` |
| ----------------------- | ------------------------------------------- | ---------------------------------------------------------------------------- | ---------- |
| Alleen hoge DCAC ratio  | `220725_cablepooling_1024`                  | `PV South installed capacity`                                                | 2          |
| Alleen lage DCAC ratio  | `220805_cablepooling_current_both_dcratios` | `PV low DC ratio installed capacity`                                         | 1/0.7      |
| Beide DCAC ratios       | `220805_cablepooling_current_both_dcratios` | `PV low DC ratio installed capacity` + `PV high DC ratio installed capacity` | 2 & 1/0.7  |
## Alle figuurtjes fixen
- [ ] Eraf vallen van teksten 

## Daarvan wilt Emiel de volgende plotjes
### Fig. 3. Technology deployment plotted against a single technology capacity cost

    (a) Deployment of solar PV on the y-axis and batteries indicated by colored dots against solar PV capacity cost on the x-axis


    (b) Deployment of batteries on the y-axis and solar PV indicated by colored dots against battery capacity cost on the x-axis

 - [ ] Add top x-axis for the 2h battery capacity cost in €/kWh

```python
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

X = np.linspace(0,1,1000)
Y = np.cos(X*20)

ax1.plot(X,Y)
ax1.set_xlabel(r"Original x-axis: $X$")

new_tick_locations = np.array([.2, .5, .9])

def tick_function(X):
    V = 1/(1+X)
    return ["%.3f" % z for z in V]

ax2.set_xlim(ax1.get_xlim())
ax2.set_xticks(new_tick_locations)
ax2.set_xticklabels(tick_function(new_tick_locations))
ax2.set_xlabel(r"Modified x-axis: $1/(1+X)$")
plt.show()
```

### Fig. 4. Technology deployment indicated by colored dots plotted against both solar PV and battery capacity cost
    (a) Deployment of solar PV indicated by colored dots against both solar PV and battery capacity cost
    (b) Deployment of batteries indicated by colored dots against both solar PV and battery capacity cost



- [ ] Heatmap plot with contourlines

### Fig. 5. Relative curtailment against total deployed generation capacity of wind + solar and colored dots indicating battery deployment


- [ ] Total added PV capacity die begint vanaf 0 en dus zonder wind

## Nieuwe figuurtjes die we misschien willen hebben
1. Batterij samenstelling tussen verschillende hour configs als functie van batterij opslagkosten
2. Renewable production capacity factor (productie - curtailment) / grid capacity y-as. X-as PV capacity, Z-index battery capacity.
3. Gedragscurves met LESO thesis viewer opstarten