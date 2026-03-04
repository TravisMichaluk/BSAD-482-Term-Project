The data cleaning process for this project followed a systematic workflow to transform disparate raw datasets into a unified framework capable of supporting high-stakes strategic decisions. The process focused on ensuring naming consistency, financial categorization, and statistical accuracy across four primary data sources.


1. Structural Normalization and Joining

The initial challenge involved reconciling the "Player Name" fields across the Salaries and Single-Game datasets. One source formatted names as "Last, First" (e.g., Stolarz, Anthony) while others used "First Last" (e.g., Anthony Stolarz). Using a relationship calculation, the names were programmatically split, trimmed, and re-named to ensure that Tableau could correctly associate financial data with on-ice performance metrics. This step was vital for building the relationship that powers the cross-file visualizations.


2. Variable Definition and Cutoff Logic

To facilitate a comparative analysis between high-investment and value-based assets, a new categorical variable, Ranking, was established. A hard threshold of $7,000,000 was applied to the Cap Hit data. Any goaltender exceeding this amount was classified as "E" (Elite), representing a franchise-level investment, while those below were classified as "T" (Tandem). This categorization allowed the analysis to move beyond individual players and evaluate the broader success of different financial models.


3. Data Type Correction and Financial Cleaning

Raw data often imports with "dirty" formatting that prevents mathematical analysis. The $/W (Cost per Win) column, originally formatted as strings containing symbols (e.g., "$119k"), was cleaned using string replacement functions to remove the currency signs and suffixes, then converted into float values. Similarly, the gameDate field, which arrived as an integer (e.g., 20250312), was transformed into a standardized Date object to enable accurate time-series analysis and fatigue-trend mapping.


4. Situational Filtering and Integrity Checks

The single-game statistics contained multiple rows per game to account for different game situations (All, 5-on-5, 4-on-5, etc.). To prevent the statistical "double-counting" that would lead to impossible results—such as cumulative save percentages exceeding 80.0—a global filter was applied to isolate the "all" situation. Additionally, a sample-size filter was implemented to exclude goaltenders with fewer than 20 games played, ensuring that the final decision is based on established performance rather than statistical noise from minor-league call-ups.


5. Aggregation and Ratio Logic

The final step involved correcting how Tableau calculates performance over time. Standard "Averages of Averages" can be misleading if one game has significantly more shots than another. The cleaning process involved shifting from simple averages to Ratio-of-Totals calculations. By summing the total saves and total shots across a rolling 5-game window before performing the division, the resulting trend lines provide a mathematically accurate representation of a goaltender's performance trajectory and the impact of their workload.


