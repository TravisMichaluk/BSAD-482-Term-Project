"""
Multiple Regression: Goalie Stats -> Team Points Percentage
2024-25 NHL Season  |  BSAD-482 Term Project

Dependent Variable:   Pts%  (team points percentage)
Independent Variables: GP, HDSV%, GSAX
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

# ── 1. LOAD DATA ─────────────────────────────────────────────────────────────

stats_df = pd.read_excel("Goalie_Stats_24-25_Min_20_games.xlsx", sheet_name="Summary")
salaries = pd.read_excel("Goalie_Salaries_2024-25.xlsx",          sheet_name="Sheet2").dropna(subset=['Player'])
puck     = pd.read_excel("goalies_puckpedia_24-25.xlsx",          sheet_name="Sheet 1 - goalies", header=1)

# ── 2. ENGINEER HDSV% ────────────────────────────────────────────────────────

puck_all = puck[puck['situation'] == 'all'].copy()
puck_all['HDSV%'] = 1 - (puck_all['highDangerGoals'] / puck_all['highDangerShots'])
puck_all = puck_all[['name', 'HDSV%']].rename(columns={'name': 'Player'})

# ── 3. FIX SALARY NAMES & PULL GSAX ──────────────────────────────────────────

def fix_name(n):
    if ',' in str(n):
        parts = str(n).split(',')
        return parts[1].strip() + ' ' + parts[0].strip()
    return str(n)

salaries['Player'] = salaries['Player'].apply(fix_name)
sal_clean   = salaries[['Player', 'GSAX']].dropna()
stats_clean = stats_df[['Player', 'GP', 'Pts%']].dropna()

# ── 4. MERGE ──────────────────────────────────────────────────────────────────

df = stats_clean.merge(sal_clean, on='Player', how='inner')
df = df.merge(puck_all,           on='Player', how='inner')
print(f"Final dataset: {len(df)} goalies\n")

# ── 5. OLS REGRESSION ────────────────────────────────────────────────────────

X_raw = df[['GP', 'HDSV%', 'GSAX']].values
y     = df['Pts%'].values
n, p  = X_raw.shape
X     = np.column_stack([np.ones(n), X_raw])

beta   = np.linalg.lstsq(X, y, rcond=None)[0]
y_hat  = X @ beta
resid  = y - y_hat

SSE    = np.sum(resid**2)
SST    = np.sum((y - y.mean())**2)
SSR    = SST - SSE
R2     = 1 - SSE / SST
R2_adj = 1 - (SSE / (n - p - 1)) / (SST / (n - 1))
MSE    = SSE / (n - p - 1)

cov_beta = MSE * np.linalg.inv(X.T @ X)
se       = np.sqrt(np.diag(cov_beta))
t_vals   = beta / se
p_vals   = 2 * (1 - stats.t.cdf(np.abs(t_vals), df=n - p - 1))

F   = (SSR / p) / MSE
F_p = 1 - stats.f.cdf(F, p, n - p - 1)

VIF           = np.diag(np.linalg.inv(np.corrcoef(X_raw.T)))
sw_stat, sw_p = stats.shapiro(resid)

# ── 6. PRINT RESULTS ─────────────────────────────────────────────────────────

feature_names = ['Intercept', 'GP', 'HDSV%', 'GSAX']
print("=" * 62)
print("  REGRESSION RESULTS:  Pts% ~ GP + HDSV% + GSAX")
print(f"  N={n}  |  R²={R2:.4f}  |  Adj R²={R2_adj:.4f}")
print(f"  F({p},{n-p-1})={F:.4f}  |  p={F_p:.6f}")
print("=" * 62)
print(f"{'Variable':<12} {'Coef':>12} {'SE':>12} {'t':>8} {'p':>10}")
print("-" * 62)
for i, name in enumerate(feature_names):
    sig = " ***" if p_vals[i] < 0.001 else (" **" if p_vals[i] < 0.01 else (" *" if p_vals[i] < 0.05 else ""))
    print(f"{name:<12} {beta[i]:>12.6f} {se[i]:>12.6f} {t_vals[i]:>8.3f} {p_vals[i]:>10.4f}{sig}")
print("=" * 62)
print("\nVariance Inflation Factors (VIF < 5 = no multicollinearity):")
for i, name in enumerate(['GP', 'HDSV%', 'GSAX']):
    print(f"  {name}: {VIF[i]:.4f}")
print(f"\nResidual normality — Shapiro-Wilk: W={sw_stat:.4f}, p={sw_p:.4f}")

# ── 7. PLOTS ──────────────────────────────────────────────────────────────────

fig = plt.figure(figsize=(14, 10))
fig.suptitle("Goalie Regression: Pts% ~ GP + HDSV% + GSAX  (2024-25 NHL)",
             fontsize=14, fontweight='bold')
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.42, wspace=0.36)

# Fitted vs Actual
ax1 = fig.add_subplot(gs[0, 0])
ax1.scatter(y_hat, y, alpha=0.75, edgecolors='steelblue', facecolors='lightblue', s=65)
lims = [min(y.min(), y_hat.min()) - 0.02, max(y.max(), y_hat.max()) + 0.02]
ax1.plot(lims, lims, 'r--', lw=1.5, label='Perfect fit')
ax1.set_xlabel("Fitted Pts%"); ax1.set_ylabel("Actual Pts%")
ax1.set_title(f"Fitted vs Actual\nR²={R2:.3f}, Adj R²={R2_adj:.3f}")
ax1.legend(fontsize=8)

# Residuals vs Fitted
ax2 = fig.add_subplot(gs[0, 1])
ax2.scatter(y_hat, resid, alpha=0.75, edgecolors='steelblue', facecolors='lightblue', s=65)
ax2.axhline(0, color='red', linestyle='--', lw=1.5)
ax2.set_xlabel("Fitted Pts%"); ax2.set_ylabel("Residuals")
ax2.set_title(f"Residuals vs Fitted\nF={F:.2f}, p={F_p:.5f}")

# Q-Q Plot
ax3 = fig.add_subplot(gs[0, 2])
(osm, osr), (slope, intercept, _) = stats.probplot(resid, dist='norm')
ax3.scatter(osm, osr, alpha=0.75, edgecolors='steelblue', facecolors='lightblue', s=65)
line_x = np.array([osm[0], osm[-1]])
ax3.plot(line_x, slope * line_x + intercept, 'r--', lw=1.5)
ax3.set_xlabel("Theoretical Quantiles"); ax3.set_ylabel("Sample Quantiles")
ax3.set_title(f"Q-Q Plot\nShapiro-Wilk p={sw_p:.3f}")

# Partial regression plots
predictors = [('GP', 0), ('HDSV%', 1), ('GSAX', 2)]
for idx, (name, col) in enumerate(predictors):
    ax = fig.add_subplot(gs[1, idx])
    others = [i for i in range(p) if i != col]
    X_other = np.column_stack([np.ones(n), X_raw[:, others]])
    def pr(Z, t): b = np.linalg.lstsq(Z, t, rcond=None)[0]; return t - Z @ b
    e_x = pr(X_other, X_raw[:, col])
    e_y = pr(X_other, y)
    ax.scatter(e_x, e_y, alpha=0.75, edgecolors='steelblue', facecolors='lightblue', s=55)
    m, b2 = np.polyfit(e_x, e_y, 1)
    xl = np.linspace(e_x.min(), e_x.max(), 100)
    ax.plot(xl, m * xl + b2, 'r-', lw=1.5)
    ax.set_xlabel(f"e({name} | others)"); ax.set_ylabel("e(Pts% | others)")
    ax.set_title(f"Partial: {name}\np={p_vals[col+1]:.4f}")

plt.savefig("goalie_regression_v2_plots.png", dpi=150, bbox_inches='tight')
print("\nPlots saved to goalie_regression_v2_plots.png")
plt.show()
