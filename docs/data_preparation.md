# Data Preparation

From raw downloads to the dashboard dataset. Columns are described in [data_contract.md](data_contract.md).

```
data/raw/energy_charts/   60 JSON files (7 countries + 8 price zones × 4 years)
  │  src/data/clean_energy_charts.py
data/interim/             hourly generation and prices
  │  src/features/build_features.py
data/processed/electricity_hourly.parquet   245,448 rows (7 countries × 35,064 hours)
```

## Cleaning

| Step | What | Why |
|---|---|---|
| Timestamps | Unix seconds → UTC | No daylight-saving gaps or duplicates |
| Resolution | 15-minute and hourly data → hourly means | Sources mix both; prices switched to 15 min in Oct 2025. For MW, the hourly mean equals MWh |
| Calendar | Every country reindexed to all 35,064 hours | Missing hours become explicit |
| Short gaps (≤ 3 h) | Linear interpolation (206 values) | Power changes smoothly |
| Long gaps in a source | Set to 0 | Empty means no production, e.g. German nuclear after the 15 April 2023 shutdown |
| Long gaps in load | Left missing, flagged (54 hours) | Mostly the Iberian blackout, 28 April 2025; filling would invent demand |
| Price zones | DE-LU for Germany; mean of DK1 and DK2 for Denmark | Prices are set per bidding zone |
| Negative prices | Kept | Real market outcomes, central to question 4 |

Known limitation: French offshore wind is empty until May 2023 and set to 0, a slight undercount (under 1% of French generation).

## Derived Variables

- **Generation categories:** 21 source series grouped into 12 (e.g. lignite + hard coal = coal). Pumped storage and batteries are storage, not renewable.
- **Renewable share** = renewables / load. Within 0.2 to 1.7 points of Energy-Charts' own figure; we count all waste as non-renewable.
- **Residual load** = load − solar − wind, the basis of the duck curve.
- **Calendar fields** in local time: hour, weekday, month, season, peak (weekdays 08:00 to 20:00).

## Validation

14 automated checks (`pytest tests/`): complete hourly calendar, no duplicates, no missing or negative generation, missing load only where flagged, and annual consumption within the range of national statistics:

| TWh | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Germany | 482 | 458 | 466 | 466 |
| France | 444 | 426 | 430 | 435 |
| Spain | 236 | 229 | 232 | 238 |
| Poland | 172 | 166 | 164 | 158 |
| Austria | 62 | 58 | 59 | 59 |
| Hungary | 43 | 42 | 43 | 43 |
| Denmark | 34 | 35 | 37 | 38 |

## Eurostat Renewables

`src/data/clean_eurostat_renewables.py`: annual renewable share of all energy (not only electricity), used as context. Columns renamed, flags labelled (`p` = provisional), EU aggregates marked, saved as Parquet.
