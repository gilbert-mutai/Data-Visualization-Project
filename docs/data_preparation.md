# Data Preparation

From the Eurostat file to the dashboard. Columns are described in [data_contract.md](data_contract.md).

```
data/raw/eurostat/nrg_ind_ren$defaultview_linear_2_0.csv      Eurostat download
  │  src/data/clean_eurostat_renewables.py
data/processed/renewable_energy_shares.parquet                368 rows
  │  dashboard: derived metrics per country and year
```

If the processed file is missing (e.g. on Streamlit Cloud), the dashboard cleans the raw file the same way. It never falls back to generated data.

## Cleaning

| Step | What | Why |
|---|---|---|
| Columns | Keep country, code, year, value, flag; rename | Raw file has 19 mostly technical columns |
| Missing values | Drop rows without a value (none in the current file) | Only measured values are shown |
| Types | Year as integer, share rounded to 3 decimals | Consistent sorting and display |
| Flags | `p` → provisional, empty → final | Eurostat marks 2025 as provisional (30 countries) |
| Aggregates | EU-27 and euro area marked `is_aggregate` | Kept as a benchmark, not ranked as a country |
| Names | Footnote markers (`*`) removed | Clean labels in charts |

## Derived Metrics

Computed in the dashboard for every country and year:

| Metric | Definition |
|---|---|
| Year-on-year change | Share minus previous year's share (percentage points) |
| Change since base | Share minus the share in 2016 |
| Rank | Position among all countries in that year |
| Gap to EU-27 | Share minus the EU-27 average |

## Validation

Values checked against the Eurostat source, e.g. Hungary 2024 = 18.3%, EU-27 2024 = 25.2%.

## Earlier Phase: Hourly Electricity Data

The repository also contains a pipeline for hourly electricity data from the Energy-Charts API (`src/data/clean_energy_charts.py`, `src/features/build_features.py`) with 14 tests in `tests/`. It is not used by the current dashboard.
