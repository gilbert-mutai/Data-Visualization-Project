"""EU Electricity Dashboard.

Run from the repo root:
    panel serve dashboard/app.py --show
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import holoviews as hv  # noqa: E402
import pandas as pd  # noqa: E402
import panel as pn  # noqa: E402

from src.viz import countries, demand, prices, renewables, style  # noqa: E402

pn.extension(theme="dark", raw_css=[f"body {{ background: {style.PAGE}; }}"])
hv.extension("bokeh")
style.apply()

# Spain's price data is licensed for private and internal use only
RESTRICTED_PRICE_COUNTRIES = ["ES"]
LINKED_SAMPLE_SIZE = 15_000


@pn.cache
def load_data():
    return pd.read_parquet(ROOT / "data" / "processed" / "electricity_hourly.parquet")


df = load_data()

# -- filters ---------------------------------------------------------------------

country_select = pn.widgets.MultiChoice(
    name="Countries",
    options={style.COUNTRY_NAMES[c]: c for c in style.COUNTRY_ORDER},
    value=list(style.COUNTRY_ORDER),
)
year_select = pn.widgets.IntRangeSlider(name="Years", start=2022, end=2025, value=(2022, 2025), step=1)
season_select = pn.widgets.CheckButtonGroup(
    name="Seasons", options=style.SEASON_ORDER, value=list(style.SEASON_ORDER),
    button_type="primary", button_style="outline", orientation="vertical",
)
FILTERS = (country_select, year_select, season_select)


def select(codes, years, seasons):
    return df[df["country"].isin(codes) & df["year"].between(*years) & df["season"].isin(seasons)]


def price_data(data):
    return data[~data["country"].isin(RESTRICTED_PRICE_COUNTRIES)]


def message(text):
    return pn.pane.Alert(text, alert_type="secondary")


def chart(make, prices_only=False):
    """Bind a chart function to the filters; it receives the filtered data."""
    def render(codes, years, seasons):
        data = select(codes, years, seasons)
        if prices_only:
            data = price_data(data)
        if data.empty:
            return message("No data for this selection.")
        return make(data).opts(shared_axes=False)
    # lazy: charts in hidden tabs are only recomputed when their tab is opened
    return pn.param.ParamFunction(pn.bind(render, *FILTERS), lazy=True, sizing_mode="stretch_width")


# -- KPI cards -------------------------------------------------------------------

def card(label, value, note=""):
    return pn.pane.HTML(
        f"""<div style="background:{style.SURFACE}; border:1px solid {style.BORDER};
                        border-radius:8px; padding:14px 18px;">
              <div style="color:{style.TEXT_MUTED}; font-size:13px;">{label}</div>
              <div style="color:{style.TEXT}; font-size:26px; font-weight:600; margin-top:4px;">{value}</div>
              <div style="color:{style.TEXT_MUTED}; font-size:12px; margin-top:2px;">{note}</div>
            </div>""",
        sizing_mode="stretch_width",
    )


def kpis(codes, years, seasons):
    data = select(codes, years, seasons)
    if data.empty:
        return message("Select at least one country and season.")
    with_load = data[~data["load_missing"]]
    consumption = with_load["load_mw"].sum()
    share = 100 * with_load["renewable_mw"].sum() / consumption
    price = price_data(data)["price_eur_mwh"]
    # Peak hour on a relative scale, so large countries do not dominate
    relative = with_load["load_mw"] / with_load.groupby("country", observed=True)["load_mw"].transform("mean")
    peak = relative.groupby(with_load["hour"]).mean().idxmax()
    return pn.Row(
        card("Electricity consumption", style.fmt_energy(consumption), "total for the selection"),
        card("Average day-ahead price", style.fmt_price(price.mean()) if len(price) else "n/a",
             "excluding Spain (licence)"),
        card("Renewable share", style.fmt_pct(share), "renewable generation / load"),
        card("Peak demand hour", f"{peak:02d}:00", "local time, average day"),
        sizing_mode="stretch_width",
    )


# -- linked selection (Q4) -------------------------------------------------------

def linked_view(codes, years, seasons):
    data = price_data(select(codes, years, seasons))
    cols = ["renewable_share_load_pct", "price_eur_mwh", "hour"]
    data = data[cols].dropna()
    if data.empty:
        return message("No price data for this selection.")
    sample = data.sample(min(LINKED_SAMPLE_SIZE, len(data)), random_state=0).astype(float)
    low, high = sample["price_eur_mwh"].quantile([0.005, 0.995])

    points = hv.Points(sample, ["renewable_share_load_pct", "price_eur_mwh"], ["hour"]).opts(
        title="Select hours (box or lasso)", color=style.SOURCE_COLORS["wind"], size=3, alpha=0.4,
        tools=["box_select", "lasso_select"], active_tools=["box_select"], ylim=(low, high),
        xlabel="Renewable share of load (%)", ylabel="Day-ahead price (EUR/MWh)",
    )
    hours = hv.operation.histogram(points, dimension="hour", num_bins=24, bin_range=(0, 24)).opts(
        title="Selected hours by time of day", xlabel="Hour of day (local time)", ylabel="Hours",
        color=style.SOURCE_COLORS["solar"],
    )
    return hv.link_selections.instance()(points + hours).opts(shared_axes=False)


# -- tabs ------------------------------------------------------------------------

def section(text):
    return pn.pane.Markdown(text, styles={"color": style.TEXT_SECONDARY}, margin=(10, 10, 0, 10))


demand_tab = pn.Column(
    section("**How does demand vary by hour, weekday and season, and when are the peaks?** "
            "One country is shown in GW, several as % of each country's average."),
    pn.Row(chart(demand.hour_weekday_heatmap), chart(demand.seasonal_profile)),
    chart(demand.calendar_heatmap),
)

countries_tab = pn.Column(
    section("**How do the countries differ in consumption and generation mix?** Averages over the selection."),
    pn.Row(chart(countries.country_map), chart(lambda d: countries.country_ranking(d, "consumption_twh"))),
    pn.Row(chart(lambda d: countries.country_ranking(d, compare_years=True)), chart(countries.country_mix)),
)

renewables_tab = pn.Column(
    section("**How has the renewable share evolved, and how well does it cover demand?** "
            "Tip: select Summer only to see the duck curve clearly."),
    chart(lambda d: renewables.generation_mix(d, as_share=True)),
    chart(renewables.renewable_share_heatmap),
    pn.Row(chart(renewables.daily_coverage), chart(renewables.coverage_duration)),
)

prices_tab = pn.Column(
    section("**Do hours with high renewable generation have lower (or negative) prices?** "
            "Spain is not shown: its price data is licensed for private use only."),
    pn.Row(chart(prices.price_distribution, prices_only=True),
           chart(prices.price_duration_curve, prices_only=True)),
    chart(prices.share_price, prices_only=True),
    section("**Linked views:** select hours in the left chart; the right chart shows when in the day "
            "they occur. Hours with high renewables and low prices cluster around midday."),
    pn.param.ParamFunction(pn.bind(linked_view, *FILTERS), lazy=True, sizing_mode="stretch_width"),
    chart(lambda d: prices.negative_price_heatmap(d, by="month"), prices_only=True),
)

about_tab = pn.pane.Markdown(
    """
### Data sources
| Data | Source | Licence |
|---|---|---|
| Hourly generation by source and load | Energy-Charts API, Fraunhofer ISE (api.energy-charts.info) | Energy-Charts terms of use |
| Day-ahead prices (all zones except Spain) | Energy-Charts API, Bundesnetzagentur / SMARD.de | CC BY 4.0 |
| Day-ahead prices, Spain | Energy-Charts API, EPEX SPOT SE | Private use only, not shown |
| Country borders | Eurostat GISCO | © EuroGeographics |

Accessed October to November 2026.

### Data preparation
Mixed 15-minute and hourly data resampled to hourly means, timestamps in UTC, short gaps (≤ 3 h)
interpolated, the Iberian blackout of 28 April 2025 left missing, negative prices kept.
Germany uses the DE-LU price zone; Denmark's price is the mean of DK1 and DK2.

### Countries and period
Hungary, Germany, Austria, France, Spain, Poland and Denmark, 2022 to 2025 (energy crisis, recovery, solar growth).
""",
    styles={"color": style.TEXT_SECONDARY}, sizing_mode="stretch_width", margin=(10, 20),
)

tabs = pn.Tabs(
    ("Demand", demand_tab),
    ("Countries", countries_tab),
    ("Renewables", renewables_tab),
    ("Prices", prices_tab),
    ("About the data", about_tab),
    dynamic=True,  # only the open tab is rendered, which keeps filtering fast
    sizing_mode="stretch_width",
)

template = pn.template.FastListTemplate(
    title="EU Electricity Dashboard",
    theme="dark",
    sidebar=[pn.pane.Markdown("### Filters"), country_select, year_select,
             pn.pane.Markdown("Seasons", margin=(10, 10, 0, 10)), season_select],
    main=[pn.panel(pn.bind(kpis, *FILTERS), sizing_mode="stretch_width"), tabs],
    accent=style.SOURCE_COLORS["wind"],
    header_background=style.SURFACE,
    background_color=style.PAGE,
    sidebar_width=300,
)
template.servable()
