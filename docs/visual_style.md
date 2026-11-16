# Visual Style

All charts use `src/viz/style.py`, so they share one theme and a colour always means the same thing.

## Theme

Dark, following the SaaS reference design: near-black page, dark chart surface, faint gridlines, muted labels. `style.apply()` sets it once for all charts.

## Colour Roles

| Role | Used for | Scale |
|---|---|---|
| Identity | energy source, country | fixed colour per entity |
| Magnitude | heatmaps, map | one hue (blue), dark = low |
| Above / below zero | price vs average, residual load | blue / gray / red |
| Status | KPI alerts only | with icon or label |

## Energy Sources

Stack order bottom to top, so renewables sit on the baseline and their total reads directly:

| Source | Colour |
|---|---|
| Solar | yellow |
| Hydro | aqua |
| Wind | blue |
| Biomass & other renewables | green |
| Coal | red |
| Nuclear | violet |
| Gas | orange |
| Oil, storage & other | gray |

Conventional hues where they exist (solar yellow, wind blue). **Colour-blind safety was measured**, not eyeballed: `src/viz/palette_check.py` simulates protanopia and deuteranopia and checks the contrast of every pair of touching colours. The gray "other" group and nuclear between coal and gas were needed to pass.

## Other Decisions

- Countries are compared by position (axes, rankings) rather than colour, since colour already means energy source.
- One y-axis per chart; never two units on one chart.
- Shares over a period are energy-weighted (total renewable MWh / total load MWh), not averages of hourly percentages.
- Price axes show the middle 99% of hours so the 2022 spikes (up to about 3,000 EUR/MWh) don't flatten everything else; tooltips show exact values.
- 245,000 hours are too many for a scatter, so prices vs renewables use hexbin density with a median line.
