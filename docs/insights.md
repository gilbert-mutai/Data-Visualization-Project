# Key Insights

Computed from `data/processed/electricity_hourly.parquet`, 2022 to 2025. Chart in italics.

## Q1: Demand

- **Weekends are about 13% lower than weekdays** (90% vs 104% of average load). *Hour × weekday heatmap*
- **Demand peaks around 18:00 in every season:** 124% of average in winter, 102% in summer; lowest at 03:00 to 04:00. *Seasonal profile*
- **France is the most seasonal:** winter load is 1.46× summer load (Germany 1.17, Hungary 1.20). *Seasonal profile*
- **The quietest days are spring Sundays and holidays** (e.g. Easter), not Christmas. *Calendar heatmap*

## Q2: Countries

- **Size:** Germany 468 TWh a year, France 434, Austria 59, Hungary 43, Denmark 36. *Ranking*
- **Renewable share of load, 2022 → 2025:** Hungary 12% → 21%, Poland 18% → 29%, France 23% → 31%, Germany 48% → 55%, Spain 49% → 60%, Denmark 73% → 76%. Austria peaked at 91% in 2024. *Dumbbell chart*
- **Different systems:** Denmark wind, Austria hydro, France nuclear, Poland coal, Hungary nuclear and gas. *Generation mix*
- **Imports matter:** Hungary generates only 75% of what it uses, France 114%, so shares "of load" and "of generation" can rank countries differently.

## Q3: Renewables

- **Renewables grew from 37% to 44% of generation; solar from 8% to 13%.** *Generation mix as share*
- **Hours fully covered by renewables, 2022 → 2025:** Austria 8% → 22%, Germany 0.2% → 6%, Denmark about 25% throughout; France and Poland 0%. *Coverage duration curve*
- **Duck curve:** on summer days solar brings renewables close to load at midday; the gap reopens in the evening peak. *Duck curve*
- **Seasons depend on the system:** wind-based Denmark peaks in winter, hydro-based Austria in summer, Hungary (solar) doubles from winter to summer; Germany stays flat as winter wind and summer solar offset. *Monthly heatmap*

## Q4: Prices

Six countries: Spain's price data may not be published (licence).

- **More renewables, lower prices, in every country** (2025 correlation from −0.82 in Germany to −0.47 in Denmark).
- **Germany 2025:** median price falls from about 165 EUR/MWh at 12% renewables to about zero above 100%. *Renewables vs price*
- **France** reaches low prices at much lower renewable shares, since nuclear covers most of the rest; **Denmark** reacts least, likely due to strong links with neighbouring markets.
- **Residual load explains prices even better** (correlation +0.58 to +0.87): the merit order effect.
- **Negative prices are growing fast,** e.g. Germany 0.8% → 6.6% of hours, France 0% → 5.9%. They cluster at midday and in late spring. *Negative-price heatmaps*
- **Price level:** median 207 EUR/MWh in 2022 (crisis), 100 in 2023, 80 in 2024, 95 in 2025. *Violins by year*
