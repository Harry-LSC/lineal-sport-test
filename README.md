# Lineal Sport Championship

Independent reconstruction of lineal championships in sport.

## Current publication

Cricket is the first published sport, covering seven lineages across Test cricket, ODIs, T20Is and the Indian Premier League.

## Updating championship data

Current holders, defences, transfers and scheduled next defences are maintained in `LSC_Update_System.xlsx`. The GitHub Actions workflow runs `build_data.py` and publishes the resulting state to `data/sports-data.json`, which is read by the Cricket Hub and championship pages.

Historical lineage data remains embedded in the individual championship pages and is changed only after verification.

Unofficial independent fan project.
