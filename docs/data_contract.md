# Data Contract

Columns of the processed datasets. Chart and dashboard code relies only on these; change this file together with any column change.

## `electricity_hourly.parquet`

One row per country and hour: 7 countries × 35,064 hours (2022 to 2025). Source: Energy-Charts API, Fraunhofer ISE.

| Column | Unit | Description |
|---|---|---|
| `timestamp_utc` | UTC | Start of the hour; use for time series and joins |
| `timestamp_local` | local time | Use for hour-of-day and weekday patterns |
| `country`, `country_name` | | `HU`, `DE`, `AT`, `FR`, `ES`, `PL`, `DK` and full name |
| `year`, `month`, `season`, `weekday`, `hour` | | Local calendar fields |
| `is_weekend`, `is_peak` | bool | Peak = weekdays 08:00 to 20:00 local |
| `load_mw` | MW | Demand |
| `solar_mw`, `wind_onshore_mw`, `wind_offshore_mw`, `wind_mw` | MW | Wind = onshore + offshore |
| `hydro_mw`, `biomass_mw`, `other_renewables_mw` | MW | Hydro excludes pumped storage |
| `nuclear_mw`, `gas_mw`, `coal_mw`, `oil_mw`, `other_mw` | MW | Coal = lignite + hard coal; other = waste + others |
| `storage_mw` | MW | Pumped storage + batteries (not renewable) |
| `renewable_mw`, `fossil_mw`, `total_generation_mw` | MW | Subtotals |
| `renewable_share_load_pct` | % | Renewables / load; can exceed 100 when exporting |
| `renewable_share_generation_pct` | % | Renewables / total generation |
| `residual_load_mw` | MW | Load − solar − wind |
| `price_eur_mwh` | EUR/MWh | Day-ahead price; negative values are real |
| `is_negative_price` | bool | Price below zero |
| `load_missing` | bool | No load data (54 hours) |
| `n_interpolated`, `n_zero_filled`, `price_interpolated` | | Data quality flags |

**Usage:** each row is one hour, so summing `_mw` columns gives MWh and their mean gives average power. Exclude `load_missing` rows when aggregating load.

## `renewable_energy_shares.parquet`

Eurostat `nrg_ind_ren`, one row per country and year (2016 to 2025): `country`, `geo_code`, `year`, `renewable_share_pct` (share of all energy use), `data_flag` (final / provisional), `is_aggregate` (EU totals).
