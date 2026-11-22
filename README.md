# EU Renewable Energy Observatory

Interactive dashboard on the renewable share of energy consumption in 37 European countries, 2016 to 2025, and their progress towards EU policy targets.

Project for **Data Visualization Methods (INMAA0105L-01/26f)**, MSc Data Science, University of Debrecen.
Team: Gilbert Mutai, Aviral Birthare, Venkatachalamoorthy Jagadish.

Online: https://eu-energyproject-mebwy7ytsuxk4jjtia9rca.streamlit.app/

## Analytical Questions
1. **Leaders and laggards:** Which countries have the highest and lowest renewable share, and how many meet a policy target?
2. **Trends:** How has the renewable share developed since 2016, compared with the EU-27 average?
3. **Movers:** Which countries changed the most, and in which years?
4. **Spread:** How far apart are the countries, and which are outliers?

Findings: [docs/insights.md](docs/insights.md).

## Dashboard
Built with **Streamlit** and **Plotly**. All views follow one country selection.

| View | Chart | Question |
|---|---|---|
| Overview | Choropleth map with year slider + ranking against an adjustable policy target | 1 |
| Trends | Multi-line trend with EU-27 average and target line; absolute, indexed or year-on-year | 2 |
| Movers | Dumbbell chart, start vs end of the period | 3 |
| Spread & Outliers | Box plot per year with all countries as dots | 4 |
| Matrix | Country × year heatmap: share, year-on-year change, change since 2016, gap to EU-27 | 2, 3 |
| Data | Filterable table with CSV export | all |

## Data
| Data | Source | Licence |
|---|---|---|
| Share of renewable energy in gross final energy consumption, annual | [Eurostat `nrg_ind_ren`](https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table) | Free reuse with attribution |

Covers all energy uses (electricity, heating, transport), not only electricity. 2025 values are provisional. Accessed October 2026.

Preparation: [docs/data_preparation.md](docs/data_preparation.md) · Columns: [docs/data_contract.md](docs/data_contract.md)

## Run
```bash
python -m venv venv
venv\Scripts\activate                   # macOS / Linux: source venv/bin/activate
pip install -r requirements.txt

streamlit run dashboard/app.py          # dashboard
panel serve dashboard/Panel.py --show   # Panel version of the dashboard
pytest tests/                           # data checks
```

## Structure
```
dashboard/     Streamlit app (app.py) and Panel version (Panel.py)
src/viz/       Plotly chart modules (map, trends, box plot, heatmap)
src/data/      data cleaning scripts
data/raw/      original Eurostat file
docs/          documentation
tests/         data checks
```
