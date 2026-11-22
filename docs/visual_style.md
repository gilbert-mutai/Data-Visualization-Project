# Visual Style

## Theme

Dark interface: black page (`#000000`), dark cards (`#1C1C1E`), light text (`#F5F5F7`), muted labels (`#8E8E93`). One accent colour (blue `#0A84FF`); green marks the policy target, amber highlights selected countries.

## Colour Scales

| Data | Scale | Why |
|---|---|---|
| Renewable share (map, matrix) | Viridis | Sequential, perceptually even, readable with colour-vision deficiencies |
| Changes (year-on-year, since 2016, gap to EU-27) | Red-blue diverging, symmetric around 0 | Gains and losses read in opposite colours, zero is neutral |
| Countries (trend lines) | Fixed categorical palette | A country keeps its colour when others are hidden |

## Decisions

- **Map + ranking side by side:** the map shows geography, the ranking makes exact comparison easy.
- **Policy target as a line**, adjustable, so users can test any benchmark and see how many countries pass.
- **Indexed trend mode** (2016 = 100) compares growth independent of starting level.
- **Box plot with all countries as dots** shows both the distribution and individual outliers.
- **EU-27 average** kept as a reference line instead of a ranked country.
