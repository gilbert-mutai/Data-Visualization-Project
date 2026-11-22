# Data Contract

Columns the dashboard relies on. Change this file together with any column change.

## `renewable_energy_shares.parquet`

Eurostat `nrg_ind_ren`: one row per country and year, 2016 to 2025. 37 countries plus EU-27 and euro area totals.

| Column | Type | Description |
|---|---|---|
| `country` | text | Country name |
| `geo_code` | text | Eurostat code (Greece is `EL`, EU-27 is `EU27_2020`) |
| `year` | integer | Year |
| `renewable_share_pct` | % | Share of renewable energy in gross final energy consumption (all energy uses) |
| `data_flag` | text | `final` or `provisional` |
| `is_aggregate` | bool | True for EU-27 and euro area totals |

## Derived in the Dashboard

| Column | Unit | Description |
|---|---|---|
| `yoy_change` | pp | Change from the previous year |
| `change_since_base` | pp | Change since 2016 |
| `year_rank` | | Rank among countries in that year (1 = highest) |
| `eu_avg_pct` | % | EU-27 value in that year |
| `vs_eu_avg` | pp | Gap to EU-27 (positive = above average) |
