# EU Electricity Dashboard

Interactive dashboard on electricity demand, generation, renewables and prices in seven EU countries, 2022 to 2025.

Project for **Data Visualization Methods (INMAA0105L-01/26f)**, MSc Data Science, University of Debrecen.
Team: Gilbert Mutai, Aviral Birthare, Venkatachalamoorthy Jagadish.

## Analytical Questions
1. **Demand:** How does demand vary by hour, weekday and season, and when are the peaks?
2. **Countries:** How do the countries differ in consumption and generation mix?
3. **Renewables:** How has the renewable share evolved, and how well does it cover demand?
4. **Prices:** Do hours with high renewable generation have lower (or negative) prices?

Countries: Hungary, Germany, Austria, France, Spain, Poland, Denmark. Findings: [docs/insights.md](docs/insights.md).

## Data Sources
| Data | Source | Licence |
|---|---|---|
| Hourly generation by source and load | [Energy-Charts API](https://api.energy-charts.info), Fraunhofer ISE | Energy-Charts terms of use |
| Day-ahead prices (all zones except ES) | Energy-Charts API, Bundesnetzagentur / SMARD.de | CC BY 4.0 |
| Day-ahead prices, Spain | Energy-Charts API, EPEX SPOT SE | Private use only, so not shown in published charts |
| Renewable energy share, annual | [Eurostat `nrg_ind_ren`](https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table) | Free reuse with attribution |
| Country borders | [Eurostat GISCO](https://gisco-services.ec.europa.eu/distribution/v2/countries/) | © EuroGeographics |

Accessed October to November 2026. Raw data is not stored in Git; scripts in `src/data/` download it.

## Data Preparation
Mixed 15-minute and hourly data resampled to hourly means, all timestamps in UTC, short gaps interpolated, the Iberian blackout (28 April 2025) left missing and flagged, negative prices kept, derived variables added (renewable share, residual load, peak flag, season). Checked by automated tests.

Details: [docs/data_preparation.md](docs/data_preparation.md) · Columns: [docs/data_contract.md](docs/data_contract.md)

## Charts
Built with **Panel, HoloViews and Bokeh** (PyViz).

| Question | Charts |
|---|---|
| Demand | hour × weekday heatmap, calendar heatmap, seasonal profile |
| Countries | choropleth map, ranking, dumbbell, generation mix |
| Renewables | stacked generation mix, monthly heatmap, duck curve, coverage duration curve |
| Prices | violin plots, price duration curve, renewables vs price hexbin, negative-price heatmap |

## Run
```bash
python -m venv venv
venv\Scripts\activate                  # macOS / Linux: source venv/bin/activate
pip install -r requirements.txt

python src/data/download_energy_charts.py
python src/data/download_gisco.py
python src/data/clean_energy_charts.py
python src/features/build_features.py

python src/viz/gallery.py              # all charts: reports/figures/chart_gallery.html
python src/viz/preview.py country_map  # one chart
panel serve dashboard/app.py --show    # dashboard
pytest tests/                          # checks
```

## Structure
```
src/data/      download and cleaning     docs/       documentation
src/features/  derived variables         dashboard/  Panel app
src/viz/       chart functions           tests/      data and chart tests
```
