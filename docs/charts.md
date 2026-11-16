# Chart Guide

How to use the chart functions in `src/viz/` in the Panel dashboard.

## Quick Start

```python
import sys
from pathlib import Path

import holoviews as hv
import pandas as pd
import panel as pn

ROOT = Path(__file__).resolve().parents[1]      # repo root, from dashboard/app.py
sys.path.insert(0, str(ROOT))
from src.viz import countries, demand, prices, renewables, style

pn.extension(theme="dark")
hv.extension("bokeh")
style.apply()

df = pd.read_parquet(ROOT / "data/processed/electricity_hourly.parquet")

country = pn.widgets.MultiChoice(name="Countries", options=style.COUNTRY_ORDER, value=["HU"])
years = pn.widgets.IntRangeSlider(name="Years", start=2022, end=2025, value=(2022, 2025))

def selection(codes, yrs):
    return df[df["country"].isin(codes) & df["year"].between(*yrs)]

heatmap = pn.bind(lambda c, y: demand.hour_weekday_heatmap(selection(c, y)), country, years)
pn.Column(pn.Row(country, years), heatmap).servable()
```

Run with `panel serve dashboard/app.py --show`. To view one chart alone: `python src/viz/preview.py` lists the names, `python src/viz/preview.py country_map` opens one.

## Conventions

- Every function takes the **already filtered** hourly DataFrame and returns a HoloViews object with hover, zoom and pan.
- `title=` overrides the default title.
- `relative=` (load charts): GW for one country, % of each country's average for several.
- `*_data` functions return the table behind a chart, e.g. for KPI cards.
- Charts showing different selections on one page need `.opts(shared_axes=False)`.

## Functions

| Module | Function | Shows |
|---|---|---|
| `demand` | `hour_weekday_heatmap` | Mean load per weekday × hour |
| | `calendar_heatmap` | One cell per day, one row per year |
| | `seasonal_profile` | Average day per season |
| `countries` | `country_map` | Choropleth of a metric |
| | `country_ranking` | Ranked dots; `compare_years=True` for a dumbbell |
| | `country_mix` | Generation mix per country (100% bars) |
| | `country_metrics` | Table per country, for KPI cards |
| `renewables` | `generation_mix` | Stacked generation with load; `as_share=True` for % |
| | `renewable_share_heatmap` | Country × month renewable share |
| | `daily_coverage` | Duck curve (best with a season filter) |
| | `coverage_duration` | How often renewables cover X% of demand |
| `prices` | `price_distribution` | Violins per country, or `by="year"` |
| | `price_duration_curve` | Prices sorted high to low |
| | `share_price` | Hexbin + median price; `x="residual_load"` for merit order |
| | `negative_price_heatmap` | Negative-price share, `by="hour"` or `by="month"` |

Metrics for `country_map` and `country_ranking`: `consumption_twh`, `mean_load_gw`, `peak_load_gw`, `renewable_share`, `mean_price`, `negative_pct`, and `per_capita_mwh` (needs `population=`).

## Linked Selection

The charts aggregate the data, so brushing needs a sampled hourly scatter that filters the others:

```python
sample = df.sample(20_000, random_state=0)
scatter = hv.Points(sample, ["renewable_share_load_pct", "price_eur_mwh"]).opts(
    size=3, alpha=0.3, tools=["box_select", "lasso_select"])
ls = hv.link_selections.instance()
linked = ls(scatter)
mix = pn.bind(lambda _: renewables.generation_mix(ls.filter(df)), ls.param.selection_expr)
```
