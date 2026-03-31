# The "Blue Paint" Dilemma


# Decision Maker: 
NHL General Managers


# Decision: 
Should an NHL General Manager commit a high-value, long-term contract to a single "Elite Starter" or allocate that same budget to a "1A/1B Tandem" for the 2025-26 season?


# Executive Summary

The National Hockey League operates under a rigorous hard salary cap, transforming roster construction into a high-stakes exercise in resource optimization. Historically, the prevailing wisdom favored the "workhorse" model, where a single elite goaltender commanded a significant percentage of the team’s budget and handled the vast majority of starts. However, the 2024-25 season underscored a shifting paradigm toward the "1A/1B" tandem model. As the speed and physical toll of the modern game increase, the decision of how to distribute capital within the "blue paint" has emerged as a primary determinant of a franchise’s long-term competitive ceiling.

This analysis focuses on the pivotal choice facing a General Manager during the Summer 2025 Free Agency period: committing a premium contract of $7.0 million or more to a single elite starter or allocating that same budget to pair two capable tandem goaltenders. This is not a simple talent evaluation but a complex risk-management problem. While elite stars offer a high degree of reliability and "star power," data from the most recent season suggests that lower-cost tandem players can often produce comparable efficiency on a per-dollar basis. Choosing the tandem route potentially allows a GM to reallocate millions in "cap savings" to bolster the defensive corps or top-six scoring depth, creating a more balanced and resilient roster.

The stakes of this decision are illustrated by the inherent volatility of the goaltending position. A single injury or a statistical regression from a high-priced starter can effectively close a championship window and leave a team with "dead cap" space that is difficult to move. Conversely, an improperly constructed tandem may lack the high-end capability required to steal a series during the Stanley Cup Playoffs. By evaluating the relationship between salary and advanced metrics like Goals Saved Above Expected (GSAx), this project establishes a decision-intelligence framework to help a General Manager minimize financial risk while maximizing the probability of post-season success.

[Read more](background.md)

## CLD Diagram

<img width="1440" height="1186" alt="image" src="https://github.com/user-attachments/assets/54658482-f095-43ef-b2bd-e1079d6fc8e8" />


<img width="1440" height="1356" alt="image" src="https://github.com/user-attachments/assets/4dfc0572-b26d-405a-9be4-9deea1af1322" />



### Key Feedback Loop Explanation

# Loop R1 — The Elite Fatigue Trap (Reinforcing)
This loop sits at the heart of the conventional GM mindset. A large investment in an elite starter creates institutional pressure to justify that spend through a high goaltender workload — the franchise goalie plays 60+ games because the team paid for 60+ games. Sustained workload produces fatigue, which degrades on-ice performance (GSAX declines). Lower GSAX reduces team Pts%, and poor standings create urgency for the GM to "solve" the goaltending problem — which, in a reinforcing loop, leads back to seeking another elite signing. Each cycle can leave the team with dead cap space and a regressing starter, amplifying rather than resolving the original problem.


# Loop B1 — Roster Depth from Tandem Investment (Balancing)
B1 is the corrective loop that the tandem model activates. By reducing investment in a single elite starter, the team increases available salary cap. That flexibility funds roster depth — specifically defensive personnel — which reduces the volume of high-danger shots against. Fewer high-danger opportunities lower the performance burden on the goalie, producing more stable and efficient GSAX outcomes even from lower-cost netminders. B1 counteracts R1 by attacking the source of goalie fatigue rather than the goalie himself.


# Loop B2 — The GSAX-Value Correction (Balancing)
B2 is the analytical corrective loop that data surfaces. GSAX feeds directly into a GSAX-per-dollar efficiency metric. When cap hit is high, efficiency is low, which — for an analytically driven organization — should reduce willingness to commit further elite spending. Meanwhile, strong HDSV% contributes positively to GSAX, but is itself suppressed by a high volume of high-danger shots. B2 connects the regression findings back to the decision structure: if GMs track GSAX/$ rather than raw salary, the loop redirects capital toward high-efficiency, lower-cost options.


# Leverage Point and Intervention
The primary leverage point is on-ice performance (GSAX) — it sits at the intersection of all three loops. Intervening at GSAX rather than at salary is the key insight for the GM decision-maker. Targeting goalies with strong GSAX trajectories regardless of contract tier — and pairing them with a deep defensive roster — activates B1 and B2 simultaneously while disrupting the R1 cycle. This is precisely the case our regression confirms: GSAX is the only statistically significant predictor of Pts% (p < 0.001), and salary is not.

## Recomendations


**Recommendation:** Allocate your goaltender budget toward a high-performing 1A/1B tandem rather than committing $7 million or more to a single elite starter. The evidence from the 2024-25 season is clear: what wins games is how many goals a goalie prevents beyond what is expected of them — not how much they are paid. Distributing your goaltending budget across two capable netminders produces comparable on-ice results at meaningfully lower cost, while freeing cap space to strengthen the parts of your roster that also drive winning.

**The evidence.** A statistical analysis of 56 goalies who played at least 20 games in 2024-25 found that Goals Saved Above Expected (GSAX) — a measure of how much better a goalie performs relative to what an average goalie would have done in the same situations — is the only factor that significantly predicts team points percentage. Salary had no statistically meaningful relationship with winning whatsoever. Just as important, value and mid-tier goalies (those earning under $5 million) delivered more GSAX per cap dollar than elite starters on average. Paying more does not reliably buy better goaltending; it buys a name. The regression model explaining this relationship accounted for roughly 39% of the variation in team winning — a meaningful result for a single position on a roster of 23 players.

**Uncertainties and conditions.** This analysis covers one season and 56 players, which limits how confidently findings can be generalized. The relationship between goaltending and winning also runs in both directions: strong teams allow fewer dangerous shots, which inflates their goalie's GSAX regardless of individual skill. If your defensive infrastructure is weak, even a high-GSAX tandem may struggle. The recommendation to pursue a tandem also depends on identifying two goalies with genuinely positive and consistent GSAX trajectories — a poorly constructed tandem built from two mediocre options is not a solution. If a generational goaltending talent becomes available at a reasonable term and structure, the calculus shifts.

**Suggested next steps.** Begin by screening free agent and trade targets using multi-year GSAX data rather than traditional statistics like save percentage or goals-against average, which are more susceptible to team effects. Model your specific cap situation: identify the two-goalie combinations available within your budget and estimate the cap savings that could be redirected toward defensive personnel or top-six forward depth. Engage your analytics staff to run this comparison against your current roster projections before free agency opens.

**What would strengthen this analysis.** Incorporating two or three seasons of data would substantially improve reliability. Adding team-level defensive metrics — such as high-danger chances against per game — would help isolate individual goalie quality from team context. A playoff-specific GSAX analysis would also be valuable, since postseason performance is ultimately what defines a championship window and may weight the elite starter argument more heavily than regular season data alone can capture.

# Data Citations (APA 7th Edition):

Hockey-Reference. (2025). 2024-25 NHL summary: League-wide averages and team statistics. https://www.hockey-reference.com/leagues/stats.html

MoneyPuck. (2025). NHL goaltender advanced stats: 2024-2025 regular season [Data set]. https://moneypuck.com/data.htm

National Hockey League. (2025). Goaltender statistics: 2024-2025 regular season [Data set]. https://www.nhl.com/stats/goalies

PuckPedia. (2025). Goaltender salary cap hits and contract details [Data set]. https://puckpedia.com/players/search

