<!-- 220627 aantekeningen met emiel.md -->

# Takenlijst
1. Kosten invullen (bandbreedtes)
2. Technische specs aanpassen
3. PV clipping losses in programmeren (als standaard uitgaan van ratio van 50%)
4. Prijzen op basis van https://pro.energytransitionmodel.com/saved_scenarios/12161

## Technische specs:

**Lithium**
| Eenheid              | Oorspronkelijk | LESO waarde         |
| -------------------- | -------------- | ------------------- |
| Roundtrip efficiency | 92%            | 0.92                |
| Discharge per dag    | 0.1%           | 0.999958 per hour   |
| Lifetime             | 20-30          | 25                  |
| O&M                  | 450€/MW/a      | aanpassen met _opex |
| Variable cost        | 1.8€/MWh       | 1.8e-6 eu/MWH       |

**PV**
| Eenheid       | Oorspronkelijk | LESO waarde |
| ------------- | -------------- | ----------- |
| O&M           | 2.5-3.2%       | 0.3         |
| Lifetime      | 35-40          | 40          |
| DC - AC ratio | 2              | 2           |
| DC - AC ratio | 340-840        | 0.34-0.84   |