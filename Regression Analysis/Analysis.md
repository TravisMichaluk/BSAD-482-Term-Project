# Regression Analysis: What Predicts Team Success?


## Model Overview


To understand which goaltender performance metrics are most associated with team success, a multiple linear regression was estimated using team points percentage (Pts%) as the dependent variable across 56 NHL goalies who played a minimum of 20 games in the 2024-25 regular season. The three independent variables were Games Played (GP), High-Danger Save Percentage (HDSV%), and Goals Saved Above Expected (GSAX).
The model was statistically significant overall (F(3,52) = 11.04, p < 0.001), meaning the three predictors together explain a non-trivial portion of variation in team winning. The R² of 0.389 indicates the model accounts for approximately 39% of the variance in team Pts%. The Adjusted R², which penalizes for the number of predictors included, was 0.354 — confirming the model retains meaningful explanatory power even after accounting for model complexity.

## Coefficients and Their Meaning
GSAX (β = 0.00444, p < 0.001)
GSAX is the only statistically significant predictor in the model and by far the most important variable. Holding GP and HDSV% constant, each additional goal saved above expected is associated with approximately a 0.44 percentage point increase in team Pts%. In practical terms, this is a meaningful result for a General Manager: a goaltender who saves 20 goals above expected — a strong but attainable performance — is associated with a team Pts% roughly 8.9 points higher than a replacement-level goalie. Over an 82-game season, that difference can be the margin between a playoff berth and an early offseason. Critically, this relationship holds regardless of cap hit, reinforcing the core argument of this analysis: teams are better served by targeting high-GSAX goalies efficiently rather than simply paying for a marquee name.

Games Played (β = 0.00127, p = 0.186)
GP carries a positive coefficient but is not statistically significant once GSAX is in the model. This makes intuitive sense — a goalie who plays more games likely does so because the team is winning and trusts their starter, but the causal driver of that winning is performance quality (captured by GSAX), not workload itself. The variable adds minimal independent explanatory value here.

HDSV% (β = 0.153, p = 0.625)
High-Danger Save Percentage is positive in direction — better performance in high-danger situations is associated with higher Pts% — but is not statistically significant. This does not necessarily mean HDSV% is unimportant as a concept; it may simply be that GSAX already absorbs much of its explanatory signal, since GSAX is a cumulative metric that reflects high-danger performance among other factors. A GM should not dismiss HDSV% as irrelevant — it may be more valuable as a scouting and evaluation tool than as a standalone regression predictor.


# Limitations
## Correlation vs. causation. 

This model identifies associations, not causal relationships. A goalie posting a high GSAX does not cause their team to win — there are complex feedback loops at play. Better teams may allow fewer high-danger chances, making their goalie's job easier and inflating their GSAX. Conversely, elite goalies can mask defensive deficiencies. The direction of influence is difficult to isolate with observational data alone.
## Omitted variable bias. 

The model explains 39% of variation in Pts%, meaning roughly 61% is driven by factors not included here. Defensive structure, offensive firepower, power play and penalty kill efficiency, coaching, and opponent quality all influence team points percentage and are absent from this model. Their omission means the coefficients on GP, HDSV%, and GSAX may absorb some of their effects, potentially inflating or distorting the estimates.
## Data constraints. 

The sample is limited to 56 goalies who met the 20-game minimum threshold in a single season. This is a relatively small dataset for regression purposes, which reduces statistical power and makes it harder to detect significant effects for variables like HDSV%. A multi-season dataset would substantially improve reliability. Additionally, goalies who played fewer than 20 games — including tandem partners who split starts unevenly — are excluded, which may introduce selection bias toward established starters and underrepresent the tandem model this project aims to evaluate.
## Unit of analysis mismatch. 

Each observation represents an individual goalie, but the dependent variable (Pts%) is a team-level outcome. Teams with two goalies who both met the 20-game threshold appear twice in the dataset under the same Pts% value, which slightly inflates the apparent sample size and may underestimate standard errors. Ideally, the analysis would aggregate goalie metrics to the team level for a cleaner unit of observation.

