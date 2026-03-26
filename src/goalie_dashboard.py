"""
The Blue Paint Dilemma — GM Decision Support Dashboard
BSAD-482 Term Project  |  2024-25 NHL Season
Run with:  streamlit run goalie_dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from pathlib import Path
BASE = Path(__file__).parent

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Blue Paint Dilemma",
    page_icon="🥅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Dark rink-inspired theme */
  .stApp { background-color: #0d1117; color: #e6edf3; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #21262d;
  }
  section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

  /* Hero header */
  .hero {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1a2332 100%);
    border: 1px solid #21262d;
    border-left: 4px solid #58a6ff;
    border-radius: 8px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
  }
  .hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    letter-spacing: 0.05em;
    color: #58a6ff;
    margin: 0 0 0.25rem 0;
    line-height: 1;
  }
  .hero p { color: #8b949e; font-size: 0.95rem; margin: 0; line-height: 1.6; }

  /* Metric cards */
  .metric-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 8px;
    padding: 1.2rem 1.5rem;
    text-align: center;
  }
  .metric-label { color: #8b949e; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; }
  .metric-value { color: #58a6ff; font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; line-height: 1.2; }
  .metric-sub { color: #6e7681; font-size: 0.78rem; margin-top: 0.2rem; }

  /* Section headers */
  .section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.06em;
    color: #e6edf3;
    border-bottom: 2px solid #21262d;
    padding-bottom: 0.4rem;
    margin: 1.5rem 0 0.75rem 0;
  }

  /* Insight boxes */
  .insight-box {
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 3px solid #3fb950;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    font-size: 0.88rem;
    color: #8b949e;
    line-height: 1.65;
    margin-top: 0.75rem;
  }
  .insight-box strong { color: #e6edf3; }

  /* Decision verdict */
  .verdict-elite {
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 4px solid #f85149;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
  }
  .verdict-tandem {
    background: #161b22;
    border: 1px solid #21262d;
    border-left: 4px solid #3fb950;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
  }
  .verdict-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
  }
  .verdict-elite .verdict-title { color: #f85149; }
  .verdict-tandem .verdict-title { color: #3fb950; }
  .verdict-body { color: #8b949e; font-size: 0.87rem; line-height: 1.65; }

  /* Divider */
  hr { border: none; border-top: 1px solid #21262d; margin: 1.5rem 0; }

  /* Tab styling override */
  .stTabs [data-baseweb="tab-list"] { background: #161b22; border-radius: 8px; gap: 4px; }
  .stTabs [data-baseweb="tab"] { color: #8b949e; border-radius: 6px; }
  .stTabs [aria-selected="true"] { background: #21262d !important; color: #58a6ff !important; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0d1117; }
  ::-webkit-scrollbar-thumb { background: #21262d; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ── DATA LOADING ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    stats_df = pd.read_excel(BASE = Path(__file__).parent / "Goalie_Stats_24-25_Min_20_games.xlsx", sheet_name="Summary")
    salaries = pd.read_excel(BASE = Path(__file__).parent / "Goalie_Salaries_2024-25.xlsx", sheet_name="Sheet2").dropna(subset=['Player'])
    puck     = pd.read_excel(BASE = Path(__file__).parent / "goalies_puckpedia_24-25.xlsx", sheet_name="Sheet 1 - goalies", header=1)

    puck_all = puck[puck['situation'] == 'all'].copy()
    puck_all['HDSV%'] = 1 - (puck_all['highDangerGoals'] / puck_all['highDangerShots'])
    puck_all = puck_all[['name', 'HDSV%']].rename(columns={'name': 'Player'})

    def fix_name(n):
        if ',' in str(n):
            p = str(n).split(',')
            return p[1].strip() + ' ' + p[0].strip()
        return str(n)

    salaries['Player'] = salaries['Player'].apply(fix_name)
    sal_clean   = salaries[['Player', 'Cap Hit', 'GSAX']].dropna()
    stats_clean = stats_df[['Player', 'Team', 'GP', 'Pts%', 'Sv%', 'GAA', 'W']].dropna()

    df = stats_clean.merge(sal_clean, on='Player', how='inner').merge(puck_all, on='Player', how='inner')
    df['Cap Hit M'] = df['Cap Hit'] / 1_000_000
    df['GSAX/M']    = df['GSAX'] / df['Cap Hit M']                 # efficiency metric
    df['Contract Type'] = df['Cap Hit M'].apply(
        lambda x: 'Elite ($7M+)' if x >= 7 else ('Mid-Tier ($3–7M)' if x >= 3 else 'Value (<$3M)')
    )
    return df

df = load_data()

# ── REGRESSION (cached) ───────────────────────────────────────────────────────
@st.cache_data
def run_regression(data):
    X_raw = data[['GP', 'HDSV%', 'GSAX']].values
    y     = data['Pts%'].values
    n, p  = X_raw.shape
    X     = np.column_stack([np.ones(n), X_raw])
    beta  = np.linalg.lstsq(X, y, rcond=None)[0]
    y_hat = X @ beta
    resid = y - y_hat
    SSE = np.sum(resid**2); SST = np.sum((y - y.mean())**2)
    R2  = 1 - SSE/SST
    R2a = 1 - (SSE/(n-p-1)) / (SST/(n-1))
    MSE = SSE/(n-p-1)
    se  = np.sqrt(np.diag(MSE * np.linalg.inv(X.T @ X)))
    t   = beta/se
    pv  = 2*(1 - stats.t.cdf(np.abs(t), df=n-p-1))
    F   = ((SST-SSE)/p)/MSE
    Fp  = 1 - stats.f.cdf(F, p, n-p-1)
    return dict(beta=beta, se=se, t=t, pv=pv, R2=R2, R2a=R2a,
                F=F, Fp=Fp, y_hat=y_hat, resid=resid, n=n)

reg = run_regression(df)

# ── PLOTLY THEME DEFAULTS ─────────────────────────────────────────────────────
PLOT_BG   = "#0d1117"
PAPER_BG  = "#0d1117"
GRID_CLR  = "#21262d"
FONT_CLR  = "#8b949e"
BLUE      = "#58a6ff"
GREEN     = "#3fb950"
ORANGE    = "#d29922"
RED       = "#f85149"
PURPLE    = "#bc8cff"

def base_layout(**kwargs):
    return dict(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=FONT_CLR, family="Inter"),
        xaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
        yaxis=dict(gridcolor=GRID_CLR, zerolinecolor=GRID_CLR),
        legend=dict(bgcolor="#161b22", bordercolor=GRID_CLR, borderwidth=1),
        margin=dict(l=50, r=30, t=50, b=50),
        **kwargs
    )


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🥅 Filters & Controls")
    st.markdown("---")

    st.markdown("**Cap Hit Range (\\$M)**")
    cap_min, cap_max = st.slider(
        "Cap Hit", 0.0, 10.5,
        (float(df['Cap Hit M'].min()), float(df['Cap Hit M'].max())),
        step=0.25, label_visibility="collapsed"
    )

    st.markdown("**Min Games Played**")
    min_gp = st.slider("Min GP", 20, 63, 20, label_visibility="collapsed")

    st.markdown("**Contract Type**")
    contract_filter = st.multiselect(
        "Contract Type", options=['Elite ($7M+)', 'Mid-Tier ($3–7M)', 'Value (<$3M)'],
        default=['Elite ($7M+)', 'Mid-Tier ($3–7M)', 'Value (<$3M)'],
        label_visibility="collapsed"
    )

    st.markdown("**Highlight Goalie**")
    highlight = st.selectbox(
        "Highlight", options=["None"] + sorted(df['Player'].tolist()),
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**GM Budget Simulator**")
    st.caption("Allocate your goalie budget to compare strategies.")
    budget = st.slider("Total Cap Space (\\$M)", 5.0, 20.0, 12.0, step=0.5)
    strategy = st.radio("Strategy", ["Elite Starter", "1A/1B Tandem"], horizontal=True)

    if strategy == "Elite Starter":
        elite_pct = st.slider("Elite goalie share (%)", 50, 90, 70)
        starter_cap = budget * elite_pct / 100
        backup_cap  = budget - starter_cap
        st.markdown(f"**Starter:** ${starter_cap:.1f}M  |  **Backup:** ${backup_cap:.1f}M")
    else:
        split = st.slider("1A share (%)", 40, 65, 55)
        g1_cap = budget * split / 100
        g2_cap = budget - g1_cap
        st.markdown(f"**Goalie 1:** ${g1_cap:.1f}M  |  **Goalie 2:** ${g2_cap:.1f}M")

    st.markdown("---")
    st.caption("BSAD-482 Term Project · 2024-25 NHL Season")


# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
mask = (
    df['Cap Hit M'].between(cap_min, cap_max) &
    (df['GP'] >= min_gp) &
    df['Contract Type'].isin(contract_filter)
)
dff = df[mask].copy()

CONTRACT_COLORS = {
    'Elite ($7M+)':     RED,
    'Mid-Tier ($3–7M)': ORANGE,
    'Value (<$3M)':     GREEN,
}


# ══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
  <h1>🥅 The Blue Paint Dilemma</h1>
  <p>
    Decision support tool for NHL General Managers · 2024-25 Regular Season ·
    Should you commit $7M+ to an elite starter, or build a high-efficiency tandem?
    Explore the data and find out.
  </p>
</div>
""", unsafe_allow_html=True)


# ── KPI ROW ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
elite_gsax  = df[df['Contract Type']=='Elite ($7M+)']['GSAX'].mean()
value_gsax  = df[df['Contract Type']=='Value (<$3M)']['GSAX'].mean()
elite_eff   = df[df['Contract Type']=='Elite ($7M+)']['GSAX/M'].mean()
value_eff   = df[df['Contract Type']=='Value (<$3M)']['GSAX/M'].mean()

for col, label, val, sub in [
    (k1, "Goalies in Sample", f"{len(dff)}", f"of {len(df)} total"),
    (k2, "Avg GSAX — Elite", f"{elite_gsax:.1f}", "Goals saved above expected"),
    (k3, "Avg GSAX — Value", f"{value_gsax:.1f}", "Goals saved above expected"),
    (k4, "Elite GSAX/\\$M", f"{elite_eff:.1f}", "Efficiency (elite starters)"),
    (k5, "Value GSAX/\\$M", f"{value_eff:.1f}", "Efficiency (value contracts)"),
]:
    col.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{val}</div>
      <div class="metric-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Value & Efficiency",
    "📈  Regression Model",
    "🏒  Player Explorer",
    "🧠  GM Decision Tool",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — VALUE & EFFICIENCY
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">GSAX vs. Cap Hit — Are Teams Getting What They Pay For?</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 1])

    with col_left:
        # Bubble chart: Cap Hit vs GSAX, sized by GP, colored by contract type
        fig = go.Figure()

        for ctype, color in CONTRACT_COLORS.items():
            sub = dff[dff['Contract Type'] == ctype]
            if sub.empty:
                continue
            fig.add_trace(go.Scatter(
                x=sub['Cap Hit M'], y=sub['GSAX'],
                mode='markers+text',
                name=ctype,
                marker=dict(
                    size=sub['GP'] / 3,
                    color=color,
                    opacity=0.75,
                    line=dict(width=1, color='#21262d'),
                ),
                text=sub['Player'].apply(lambda n: n.split()[-1]),
                textposition='top center',
                textfont=dict(size=9, color='#8b949e'),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Cap Hit: $%{x:.2f}M<br>"
                    "GSAX: %{y:.1f}<br>"
                    "GP: %{customdata[1]}<br>"
                    "Team: %{customdata[2]}<extra></extra>"
                ),
                customdata=list(zip(sub['Player'], sub['GP'], sub['Team'])),
            ))

        # Highlight selected goalie
        if highlight != "None" and highlight in dff['Player'].values:
            row = dff[dff['Player'] == highlight].iloc[0]
            fig.add_trace(go.Scatter(
                x=[row['Cap Hit M']], y=[row['GSAX']],
                mode='markers+text',
                marker=dict(size=22, color=PURPLE, symbol='star',
                            line=dict(width=2, color='white')),
                text=[row['Player']], textposition='top center',
                textfont=dict(size=11, color=PURPLE, family='Inter'),
                showlegend=False, name='Highlighted',
                hovertemplate=f"<b>{row['Player']}</b><br>Cap Hit: ${row['Cap Hit M']:.2f}M<br>GSAX: {row['GSAX']:.1f}<extra></extra>"
            ))

        # Trendline
        if len(dff) > 3:
            z = np.polyfit(dff['Cap Hit M'], dff['GSAX'], 1)
            xl = np.linspace(dff['Cap Hit M'].min(), dff['Cap Hit M'].max(), 100)
            fig.add_trace(go.Scatter(
                x=xl, y=np.polyval(z, xl),
                mode='lines', line=dict(color=BLUE, width=1.5, dash='dash'),
                name='Trend', showlegend=False
            ))

        # Zero line
        fig.add_hline(y=0, line_color=GRID_CLR, line_width=1)

        fig.update_layout(
            **base_layout(title="Cap Hit vs GSAX  (bubble size = games played)"),
            xaxis_title="Cap Hit ($M)", yaxis_title="Goals Saved Above Expected (GSAX)",
            height=480,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Efficiency bar (GSAX per $M)
        eff_df = (
            dff.groupby('Contract Type')['GSAX/M']
            .mean().reset_index()
            .sort_values('GSAX/M', ascending=True)
        )
        colors_bar = [CONTRACT_COLORS.get(c, BLUE) for c in eff_df['Contract Type']]
        fig2 = go.Figure(go.Bar(
            x=eff_df['GSAX/M'], y=eff_df['Contract Type'],
            orientation='h',
            marker_color=colors_bar,
            text=eff_df['GSAX/M'].apply(lambda v: f"{v:.1f}"),
            textposition='outside', textfont=dict(color='#e6edf3'),
        ))
        fig2.update_layout(
            **base_layout(title="Avg GSAX per $1M<br>by Contract Type"),
            xaxis_title="GSAX / $M", yaxis_title="",
            height=280, margin=dict(l=10, r=50, t=60, b=40),
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Pts% box by contract
        fig3 = go.Figure()
        for ctype, color in CONTRACT_COLORS.items():
            sub = dff[dff['Contract Type'] == ctype]
            if sub.empty: continue
            fig3.add_trace(go.Box(
                y=sub['Pts%'], name=ctype.split(' ')[0],
                marker_color=color, line_color=color,
                fillcolor=color.replace(')', ', 0.15)').replace('rgb', 'rgba') if 'rgb' in color else color,
                boxmean=True,
            ))
        fig3.update_layout(
            **base_layout(title="Pts% Distribution<br>by Contract Type"),
            yaxis_title="Team Pts%", height=240,
            margin=dict(l=10, r=20, t=60, b=40), showlegend=False,
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
      <strong>Key Insight:</strong> Value contracts (&lt;$3M) deliver more GSAX per cap dollar than elite deals ($7M+).
      The trendline shows that beyond roughly $5M, additional spending yields diminishing GSAX returns.
      This supports the tandem model: two capable, cheaper goalies can match the aggregate performance of a single elite starter
      while freeing cap space to strengthen the rest of the roster.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — REGRESSION MODEL
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Multiple Regression: What Actually Predicts Winning?</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box" style="margin-bottom:1rem;">
      Model: <strong>Pts% ~ GP + HDSV% + GSAX</strong> &nbsp;·&nbsp;
      Estimated on all 56 qualifying goalies &nbsp;·&nbsp;
      Filters do not affect the regression coefficients (full-sample model).
    </div>
    """, unsafe_allow_html=True)

    rc1, rc2 = st.columns([2, 1])

    with rc2:
        # Model summary cards
        st.markdown('<div class="section-header" style="font-size:1.1rem;">Model Summary</div>', unsafe_allow_html=True)
        for label, val, sub in [
            ("R²",             f"{reg['R2']:.3f}",  "Variance explained"),
            ("Adjusted R²",    f"{reg['R2a']:.3f}", "Penalised for # predictors"),
            ("F-statistic",    f"{reg['F']:.2f}",   f"p = {reg['Fp']:.6f}"),
            ("Sample Size",    f"{reg['n']}",        "Goalies (≥20 GP)"),
        ]:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:0.6rem; text-align:left; padding:0.8rem 1rem;">
              <div class="metric-label">{label}</div>
              <div class="metric-value" style="font-size:1.6rem;">{val}</div>
              <div class="metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        # Coefficient table
        coef_df = pd.DataFrame({
            'Variable':  ['Intercept', 'GP', 'HDSV%', 'GSAX'],
            'Coef':      [f"{b:.5f}" for b in reg['beta']],
            'p-value':   [f"{p:.4f}" for p in reg['pv']],
            'Sig':       ['', '' if reg['pv'][1]>=0.05 else '*',
                          '' if reg['pv'][2]>=0.05 else '*',
                          '***' if reg['pv'][3]<0.001 else ''],
        })
        st.dataframe(coef_df, hide_index=True, use_container_width=True)

    with rc1:
        viz_choice = st.radio(
            "Select visualization",
            ["Fitted vs Actual", "Residuals vs Fitted", "Partial: GSAX"],
            horizontal=True
        )

        if viz_choice == "Fitted vs Actual":
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=reg['y_hat'], y=df['Pts%'],
                mode='markers',
                marker=dict(color=BLUE, size=9, opacity=0.8,
                            line=dict(width=1, color='#21262d')),
                hovertemplate="<b>%{customdata}</b><br>Fitted: %{x:.3f}<br>Actual: %{y:.3f}<extra></extra>",
                customdata=df['Player'],
                name='Goalies'
            ))
            lims = [min(reg['y_hat'].min(), df['Pts%'].min()) - 0.02,
                    max(reg['y_hat'].max(), df['Pts%'].max()) + 0.02]
            fig.add_trace(go.Scatter(x=lims, y=lims, mode='lines',
                line=dict(color=RED, width=1.5, dash='dash'), name='Perfect fit'))
            fig.update_layout(**base_layout(title="Fitted vs Actual Pts%"),
                xaxis_title="Fitted Pts%", yaxis_title="Actual Pts%", height=440)

        elif viz_choice == "Residuals vs Fitted":
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=reg['y_hat'], y=reg['resid'],
                mode='markers',
                marker=dict(color=ORANGE, size=9, opacity=0.8,
                            line=dict(width=1, color='#21262d')),
                hovertemplate="<b>%{customdata}</b><br>Fitted: %{x:.3f}<br>Residual: %{y:.3f}<extra></extra>",
                customdata=df['Player'], name='Residuals'
            ))
            fig.add_hline(y=0, line_color=RED, line_dash='dash', line_width=1.5)
            fig.update_layout(**base_layout(title="Residuals vs Fitted Values"),
                xaxis_title="Fitted Pts%", yaxis_title="Residual", height=440)

        else:  # Partial GSAX
            p_col = 2  # GSAX index in X_raw
            X_raw = df[['GP', 'HDSV%', 'GSAX']].values
            y_arr = df['Pts%'].values
            n_ = len(y_arr)
            others = [0, 1]
            X_other = np.column_stack([np.ones(n_), X_raw[:, others]])
            def pr(Z, t): b = np.linalg.lstsq(Z, t, rcond=None)[0]; return t - Z @ b
            e_x = pr(X_other, X_raw[:, p_col])
            e_y = pr(X_other, y_arr)
            m, b2 = np.polyfit(e_x, e_y, 1)
            xl = np.linspace(e_x.min(), e_x.max(), 200)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=e_x, y=e_y, mode='markers',
                marker=dict(color=GREEN, size=9, opacity=0.8,
                            line=dict(width=1, color='#21262d')),
                hovertemplate="<b>%{customdata}</b><br>e(GSAX): %{x:.2f}<br>e(Pts%): %{y:.3f}<extra></extra>",
                customdata=df['Player'], name='Partial residuals'
            ))
            fig.add_trace(go.Scatter(x=xl, y=m*xl+b2, mode='lines',
                line=dict(color=RED, width=2), name='Partial slope'))
            fig.update_layout(**base_layout(
                title=f"Partial Regression: GSAX  (p < 0.001)"),
                xaxis_title="e(GSAX | GP, HDSV%)",
                yaxis_title="e(Pts% | GP, HDSV%)", height=440)

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
      <strong>Interpretation:</strong> GSAX is the only statistically significant predictor (p &lt; 0.001).
      Each additional goal saved above expected is associated with a ~0.44 percentage point increase in team Pts%.
      The model explains <strong>39% of the variance</strong> in team points percentage — a meaningful result given that
      goaltending is just one component of team success. GP and HDSV% are not independently significant once GSAX
      is in the model, likely because GSAX already absorbs their explanatory signal.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PLAYER EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Player Explorer — Compare Goalies Across Metrics</div>', unsafe_allow_html=True)

    pe1, pe2 = st.columns([1, 2])

    with pe1:
        x_axis = st.selectbox("X-Axis", ['Cap Hit M', 'GSAX', 'HDSV%', 'GP', 'Sv%', 'GAA', 'Pts%', 'GSAX/M'], index=0)
        y_axis = st.selectbox("Y-Axis", ['GSAX', 'Pts%', 'HDSV%', 'Sv%', 'GAA', 'GP', 'Cap Hit M', 'GSAX/M'], index=0)
        size_by = st.selectbox("Bubble Size", ['GP', 'GSAX', 'Cap Hit M'], index=0)
        color_by = st.selectbox("Color By", ['Contract Type', 'Team', 'Pts%'], index=0)

    with pe2:
        if color_by == 'Contract Type':
            color_map = CONTRACT_COLORS
            fig_ex = px.scatter(
                dff, x=x_axis, y=y_axis, size=size_by,
                color='Contract Type', color_discrete_map=color_map,
                hover_name='Player',
                hover_data={'Team': True, 'GP': True, 'Cap Hit M': ':.2f',
                            'GSAX': ':.1f', 'HDSV%': ':.3f', 'Pts%': ':.3f'},
                size_max=40,
            )
        else:
            fig_ex = px.scatter(
                dff, x=x_axis, y=y_axis, size=size_by,
                color=color_by,
                color_continuous_scale='Blues' if color_by == 'Pts%' else None,
                hover_name='Player',
                hover_data={'Team': True, 'GP': True, 'Cap Hit M': ':.2f',
                            'GSAX': ':.1f', 'HDSV%': ':.3f', 'Pts%': ':.3f'},
                size_max=40,
            )

        fig_ex.update_layout(**base_layout(title=f"{y_axis} vs {x_axis}"), height=420)
        fig_ex.update_traces(marker=dict(line=dict(width=1, color='#21262d')))
        st.plotly_chart(fig_ex, use_container_width=True)

    # Sortable data table
    st.markdown('<div class="section-header" style="font-size:1.1rem;">Full Data Table</div>', unsafe_allow_html=True)
    sort_col = st.selectbox("Sort by", ['GSAX', 'GSAX/M', 'Pts%', 'Cap Hit M', 'HDSV%', 'GP'], index=0)
    display_df = (
        dff[['Player', 'Team', 'Contract Type', 'Cap Hit M', 'GP', 'Pts%', 'GSAX', 'HDSV%', 'Sv%', 'GAA', 'GSAX/M']]
        .sort_values(sort_col, ascending=False)
        .reset_index(drop=True)
    )
    display_df.columns = ['Player', 'Team', 'Contract', 'Cap Hit ($M)', 'GP', 'Pts%', 'GSAX', 'HDSV%', 'Sv%', 'GAA', 'GSAX/$M']
    display_df['Cap Hit ($M)'] = display_df['Cap Hit ($M)'].round(2)
    display_df['Pts%']         = display_df['Pts%'].round(3)
    display_df['HDSV%']        = display_df['HDSV%'].round(3)
    display_df['Sv%']          = display_df['Sv%'].round(3)
    display_df['GAA']          = display_df['GAA'].round(2)
    display_df['GSAX/$M']      = display_df['GSAX/$M'].round(1)
    st.dataframe(display_df, use_container_width=True, height=320)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — GM DECISION TOOL
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">GM Decision Tool — Elite Starter vs. 1A/1B Tandem</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box" style="margin-bottom:1.25rem;">
      Use the <strong>Budget Simulator</strong> in the sidebar to configure your cap allocation,
      then explore how goalies at each price point have performed. The analysis below uses your
      selected budget and strategy to project expected GSAX and team Pts%.
    </div>
    """, unsafe_allow_html=True)

    # ── Projected outcomes ───────────────────────────────────────────────────
    def predict_pts(gsax_val, mean_gp=40, mean_hdsv=0.779):
        b = reg['beta']
        return b[0] + b[1]*mean_gp + b[2]*mean_hdsv + b[3]*gsax_val

    if strategy == "Elite Starter":
        elite_pool  = df[df['Cap Hit M'] >= 7]
        backup_pool = df[df['Cap Hit M'] < 3]
        proj_gsax_s = elite_pool['GSAX'].mean() + backup_pool['GSAX'].mean()
        proj_pts_s  = predict_pts(proj_gsax_s)
        label_s     = f"Elite Starter (${starter_cap:.1f}M) + Backup (${backup_cap:.1f}M)"
    else:
        g1_pool = df[(df['Cap Hit M'] >= g1_cap * 0.7) & (df['Cap Hit M'] <= g1_cap * 1.3)]
        g2_pool = df[(df['Cap Hit M'] >= g2_cap * 0.7) & (df['Cap Hit M'] <= g2_cap * 1.3)]
        if g1_pool.empty: g1_pool = df
        if g2_pool.empty: g2_pool = df
        proj_gsax_s = g1_pool['GSAX'].mean() + g2_pool['GSAX'].mean()
        proj_pts_s  = predict_pts(proj_gsax_s)
        label_s     = f"Tandem: ${g1_cap:.1f}M + ${g2_cap:.1f}M"

    # Compare both strategies at same budget
    elite_gsax_proj  = df[df['Cap Hit M'] >= 7]['GSAX'].mean() + df[df['Cap Hit M'] < 3]['GSAX'].mean()
    tandem_g1        = df[(df['Cap Hit M'] >= budget*0.5*0.7) & (df['Cap Hit M'] <= budget*0.5*1.3)]
    tandem_g2        = tandem_g1
    if tandem_g1.empty: tandem_g1 = df
    tandem_gsax_proj = tandem_g1['GSAX'].mean() * 2
    elite_pts_proj   = predict_pts(elite_gsax_proj)
    tandem_pts_proj  = predict_pts(tandem_gsax_proj)

    d1, d2 = st.columns(2)

    with d1:
        st.markdown(f"""
        <div class="verdict-elite">
          <div class="verdict-title">⭐ Elite Starter Model</div>
          <div class="verdict-body">
            <strong>Projected combined GSAX:</strong> {elite_gsax_proj:.1f}<br>
            <strong>Projected Pts%:</strong> {elite_pts_proj:.3f}<br>
            <strong>Cap spent on goaltending:</strong> ${budget:.1f}M<br><br>
            High upside, but cap-heavy. One injury or regression collapses
            the plan. The backup often costs $1–2M and contributes very little.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with d2:
        delta = tandem_pts_proj - elite_pts_proj
        delta_str = f"+{delta:.3f}" if delta >= 0 else f"{delta:.3f}"
        st.markdown(f"""
        <div class="verdict-tandem">
          <div class="verdict-title">🤝 1A/1B Tandem Model</div>
          <div class="verdict-body">
            <strong>Projected combined GSAX:</strong> {tandem_gsax_proj:.1f}<br>
            <strong>Projected Pts%:</strong> {tandem_pts_proj:.3f}
            <span style="color:#3fb950; font-weight:600;"> ({delta_str})</span><br>
            <strong>Cap spent on goaltending:</strong> ${budget:.1f}M<br><br>
            More resilient to injury. Potential to redistribute saved cap to
            defence or top-six forwards. Data suggests competitive GSAX at lower cost.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── GSAX distribution by contract bin ───────────────────────────────────
    dc1, dc2 = st.columns([2, 1])

    with dc1:
        st.markdown('<div class="section-header" style="font-size:1.1rem;">GSAX Distribution by Cap Range</div>', unsafe_allow_html=True)
        bins = [0, 1.5, 3, 5, 7, 11]
        labels_b = ['<$1.5M', '$1.5–3M', '$3–5M', '$5–7M', '$7M+']
        df_bin = df.copy()
        df_bin['Cap Bin'] = pd.cut(df_bin['Cap Hit M'], bins=bins, labels=labels_b)

        fig_v = go.Figure()
        colors_v = [GREEN, GREEN, ORANGE, ORANGE, RED]
        for i, (label, color) in enumerate(zip(labels_b, colors_v)):
            sub = df_bin[df_bin['Cap Bin'] == label]
            if sub.empty: continue
            fig_v.add_trace(go.Violin(
                y=sub['GSAX'], name=label,
                box_visible=True, meanline_visible=True,
                fillcolor=color, opacity=0.55,
                line_color=color, points='all',
                pointpos=0, jitter=0.3,
                marker=dict(size=5, opacity=0.6),
            ))
        fig_v.update_layout(**base_layout(title="GSAX Distribution by Cap Bracket"),
            yaxis_title="GSAX", height=380, showlegend=False)
        fig_v.add_hline(y=0, line_color=GRID_CLR, line_dash='dot')
        st.plotly_chart(fig_v, use_container_width=True)

    with dc2:
        st.markdown('<div class="section-header" style="font-size:1.1rem;">Avg Pts% by Cap Bracket</div>', unsafe_allow_html=True)
        pts_bin = df_bin.groupby('Cap Bin', observed=True)['Pts%'].mean().reset_index()
        fig_bar = go.Figure(go.Bar(
            x=pts_bin['Cap Bin'], y=pts_bin['Pts%'],
            marker_color=[GREEN, GREEN, ORANGE, ORANGE, RED],
            text=pts_bin['Pts%'].apply(lambda v: f"{v:.3f}"),
            textposition='outside', textfont=dict(color='#e6edf3'),
        ))
        fig_bar.update_layout(**base_layout(title="Avg Team Pts%<br>by Goalie Cap Bracket"),
            yaxis_title="Avg Pts%", height=380,
            yaxis_range=[0, 0.75], showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Final recommendation ─────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-header" style="font-size:1.2rem;">Data-Driven Recommendation</div>', unsafe_allow_html=True)

    winner = "Tandem" if tandem_pts_proj >= elite_pts_proj else "Elite Starter"
    st.markdown(f"""
    <div class="insight-box">
      <strong>Bottom Line for a GM with ${budget:.1f}M in goaltending cap space:</strong><br><br>
      The 2024-25 data favours the <strong>{winner} model</strong>.
      Value and mid-tier goalies (&lt;$5M) collectively deliver competitive GSAX at a fraction of the cost.
      The regression confirms that <strong>GSAX — not salary — is what predicts team Pts%</strong> (p &lt; 0.001, β = 0.00444).
      A well-constructed tandem can match or exceed the projected Pts% of a single elite starter while preserving
      cap flexibility to address other roster needs. The key risk is identifying two goalies with proven positive GSAX
      trajectories — this requires strong scouting and analytics infrastructure, but the financial upside is significant.
      <br><br>
      <strong>Limitations to consider:</strong> This model explains ~39% of Pts% variance. Team defence, offence,
      coaching, and schedule difficulty account for the remainder. Correlation does not imply causation — high GSAX
      may reflect strong team defence as much as individual goalie quality.
    </div>
    """, unsafe_allow_html=True)
