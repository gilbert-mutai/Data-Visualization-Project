# Chart Guide

The charts are Plotly modules in `src/viz/`. Each takes the Eurostat table (see [data_contract.md](data_contract.md)) and returns a Plotly figure; `dashboard/app.py` places them in the views.

| Module | Function | Chart | Dashboard view |
|---|---|---|---|
| `choropleth_map.py` | `create_choropleth_map(df)` | Map of Europe with a year slider; `enrich_country_metrics(df)` adds the derived metrics | Overview |
| `multitrend list chart.py` | `create_multitrend(df)` | One line per country with a ranked legend; click to hide, double-click to isolate | Trends |
| `Outlier box plot.py` | `create_outlier_box(df)` | Box per year; outliers (1.5 × IQR rule) labelled by country | Spread & Outliers |
| `Heatmap matrix.py` | `create_heatmap(df)` | Countries × years; share, year-on-year change or change since 2016 | Matrix |

The ranking bars (Overview) and the dumbbell chart (Movers) are built directly in `dashboard/app.py`.

## Viewing a Single Chart

Each module also runs on its own and opens the chart in the browser:

```bash
python src/viz/choropleth_map.py
python "src/viz/Heatmap matrix.py"
```

## Interaction

- **Country selection** in the sidebar applies to every view.
- **Year slider** and **metric selector** (share, year-on-year change, change since 2016, gap to EU-27) drive the map and ranking.
- **Policy target** slider adds a target line to the ranking and trend charts and counts the countries above it.
- **Hover** on any chart for exact values; **zoom and pan** via the Plotly toolbar.
- **Export CSV** in the Data view downloads the filtered table.
