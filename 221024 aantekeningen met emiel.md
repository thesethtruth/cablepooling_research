# Takenlijst figuurtjes

Er zijn 3 experimenten, met 2 `run_id`s

| Experiment beschrijving | `run_id`                                    | `pv_cols`                                                                    | `dc_ratio` |
| ----------------------- | ------------------------------------------- | ---------------------------------------------------------------------------- | ---------- |
| Alleen hoge DCAC ratio  | `220725_cablepooling_1024`                  | `PV South installed capacity`                                                | 2          |
| Alleen lage DCAC ratio  | `220805_cablepooling_current_both_dcratios` | `PV low DC ratio installed capacity`                                         | 1/0.7      |
| Beide DCAC ratios       | `220805_cablepooling_current_both_dcratios` | `PV low DC ratio installed capacity` + `PV high DC ratio installed capacity` | 2 & 1/0.7  |

## Daarvan wilt Emiel de volgende plotjes
### Fig. 3. Technology deployment plotted against a single technology capacity cost

    (a) Deployment of solar PV on the y-axis and batteries indicated by colored dots against solar PV capacity cost on the x-axis
![](imgs\report_cablepool_cheapbat_pv_deployment_vs_cost.png)

 - [ ] Palette to green

    (b) Deployment of batteries on the y-axis and solar PV indicated by colored dots against battery capacity cost on the x-axis
![](imgs/report_cablepool_cheapbat_bat_deployment_vs_cost.png)

 - [ ] Palette to yellow
 - [ ] Change the x-axis to battery capacity cost regardless of the hour configuration (NOT 6h but €/kWh)
 - [ ] Add top x-axis for the 2h battery capacity cost in €/kWh


### Fig. 4. Technology deployment indicated by colored dots plotted against both solar PV and battery capacity cost

    (a) Deployment of solar PV indicated by colored dots against both solar PV and battery capacity cost

![](imgs\report_cablepool_cheapbat_bivariate_deployment.png)

    (b) Deployment of batteries indicated by colored dots against both solar PV and battery capacity cost

![](imgs\report_cablepool_cheapbat_bivariate_deployment2.png)


- [ ] Heatmap plot with contourlines

### Fig. 5. Relative curtailment against total deployed generation capacity of wind + solar and colored dots indicating battery deployment

![](imgs\report_cablepool_cheapbat_rel_curtailment_vs_deployment.png)

- [ ] Palette to green
- [ ] Relative curtailment (inclusief wind)
- [ ] Total added PV capacity die begint vanaf 0 en dus zonder wind

## Nieuwe figuurtjes die we misschien willen hebben
1. Batterij samenstelling tussen verschillende hour configs als functie van batterij opslagkosten
2. Renewable production capacity factor (productie - curtailment) / grid capacity y-as. X-as PV capacity, Z-index battery capacity.
3. Gedrags curves van representaties