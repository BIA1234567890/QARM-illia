# app.py
import streamlit as st
import pandas as pd
import altair as alt
from groq import Groq
import time  # <- for timing the backtest

from engine import (
    PortfolioConfig,
    load_all_data,
    run_backtest,
    run_today_optimization,
)

from functions import (
    validate_constraints,
    compute_backtest_stats,
    management_fee_from_wealth,
    build_backtest_context_text,
)


# --------------- GLOBAL DATA (cached) ---------------
@st.cache_data
def get_data():
    return load_all_data()


def main():
    st.set_page_config(
        page_title="QARM Portfolio Manager",
        layout="wide",
    )

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ("About us", "Portfolio optimization", "Phi assistant"),
    )

    data = get_data()

    if page == "About us":
        page_about()
    elif page == "Portfolio optimization":
        page_portfolio_optimization(data)
    elif page == "Phi assistant":
        page_ai_assistant()


def get_llm_client():
    """
    Returns a Groq client using the secret API key.
    """
    api_key = st.secrets["groq"]["api_key"]
    client = Groq(api_key=api_key)
    return client


# --------------- PAGE 1: ABOUT US ---------------
def page_about():
    st.title("Our Investment Firm")

    st.markdown(
        """def page_about():
    # --- Custom CSS for premium look ---
    st.markdown(
        """
        <style>
        /* Overall page background tweak */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .phi-hero {
            border-radius: 24px;
            padding: 2.8rem 3rem;
            background: radial-gradient(circle at 0% 0%, #1f2937 0, #020617 45%, #020617 100%);
            color: #e5e7eb;
            box-shadow: 0 28px 60px rgba(0,0,0,0.55);
            border: 1px solid rgba(148,163,184,0.35);
        }

        .phi-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.35rem 0.9rem;
            border-radius: 999px;
            font-size: 0.8rem;
            letter-spacing: .06em;
            text-transform: uppercase;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(148,163,184,0.6);
            color: #e5e7eb;
        }

        .phi-tag-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: #22c55e;
            box-shadow: 0 0 0 4px rgba(34,197,94,0.35);
        }

        .phi-hero-title {
            font-size: 2.2rem;
            line-height: 1.1;
            font-weight: 700;
            margin-top: 1.3rem;
            margin-bottom: 0.8rem;
        }

        .phi-hero-subtitle {
            font-size: 1.02rem;
            color: #cbd5f5;
            max-width: 34rem;
        }

        .phi-hero-stats {
            display: flex;
            gap: 1.8rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }

        .phi-stat {
            min-width: 130px;
        }

        .phi-stat-label {
            font-size: 0.82rem;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: .08em;
        }

        .phi-stat-value {
            font-size: 1.15rem;
            font-weight: 600;
            color: #e5e7eb;
        }

        .phi-badge {
            display: inline-flex;
            gap: 0.35rem;
            align-items: center;
            padding: 0.4rem 0.75rem;
            border-radius: 999px;
            background: rgba(15,23,42,0.8);
            font-size: 0.78rem;
            color: #e5e7eb;
            border: 1px solid rgba(55,65,81,0.9);
        }

        .phi-badge span:nth-child(1) {
            font-size: 1rem;
        }

        .phi-section {
            margin-top: 2.8rem;
        }

        .phi-section-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }

        .phi-section-subtitle {
            font-size: 0.95rem;
            color: #6b7280;
            margin-bottom: 1.8rem;
        }

        .phi-card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 1.4rem;
        }

        .phi-card {
            border-radius: 18px;
            padding: 1.25rem 1.4rem;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            box-shadow: 0 10px 30px rgba(15,23,42,0.04);
        }

        .phi-card-icon {
            width: 34px;
            height: 34px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            margin-bottom: 0.4rem;
            background: radial-gradient(circle at 0% 0%, #0ea5e9, #1d4ed8);
            color: #eff6ff;
        }

        .phi-card-title {
            font-size: 0.98rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        .phi-card-text {
            font-size: 0.9rem;
            color: #6b7280;
        }

        .phi-pill-small {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            background: #eff6ff;
            color: #1d4ed8;
            font-size: 0.78rem;
            font-weight: 500;
            margin-bottom: 0.6rem;
        }

        .phi-process {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 1.2rem;
        }

        .phi-step {
            border-radius: 14px;
            padding: 1rem 1.1rem;
            background: #f9fafb;
            border: 1px solid #e5e7eb;
        }

        .phi-step-label {
            font-size: 0.8rem;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: .08em;
        }

        .phi-step-title {
            font-size: 0.98rem;
            font-weight: 600;
            margin: 0.15rem 0 0.3rem 0;
        }

        .phi-step-text {
            font-size: 0.9rem;
            color: #6b7280;
        }

        .phi-contact {
            margin-top: 3.2rem;
            border-radius: 20px;
            padding: 1.7rem 1.9rem;
            background: linear-gradient(135deg, #0f172a, #020617);
            color: #e5e7eb;
            border: 1px solid rgba(148,163,184,0.55);
            box-shadow: 0 20px 40px rgba(15,23,42,0.5);
        }

        .phi-contact-title {
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 0.35rem;
        }

        .phi-contact-text {
            font-size: 0.95rem;
            color: #cbd5f5;
            margin-bottom: 0.9rem;
        }

        .phi-contact-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.9rem;
            align-items: center;
        }

        .phi-contact-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            padding: 0.55rem 0.9rem;
            border-radius: 999px;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(148,163,184,0.8);
            font-size: 0.85rem;
            color: #e5e7eb;
        }

        .phi-contact-chip a {
            color: #38bdf8;
            text-decoration: none;
            font-weight: 500;
        }

        .phi-contact-chip a:hover {
            text-decoration: underline;
        }

        .phi-contact-note {
            font-size: 0.8rem;
            color: #9ca3af;
        }

        @media (max-width: 768px) {
            .phi-hero {
                padding: 1.9rem 1.4rem;
            }
            .phi-hero-title {
                font-size: 1.75rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- HERO SECTION ---
    st.markdown(
        """
        <div class="phi-hero">
          <div class="phi-pill">
            <div class="phi-tag-dot"></div>
            PHI INVESTMENT CAPITAL · QUANTITATIVE PORTFOLIO MANAGERS
          </div>

          <div style="display:flex;flex-wrap:wrap;gap:2.5rem;margin-top:1.5rem;">
            <div style="flex:1 1 260px;min-width:260px;">
              <div class="phi-hero-title">
                Quietly obsessing over risk,<br/>so you don't have to.
              </div>
              <div class="phi-hero-subtitle">
                Phi Investment Capital is a quantitative asset &amp; risk management boutique.
                We build rule-based portfolios where every position, constraint and trade
                has a clear, documented rationale – no black boxes, no story-telling after the fact.
              </div>

              <div class="phi-hero-stats">
                <div class="phi-stat">
                  <div class="phi-stat-label">Approach</div>
                  <div class="phi-stat-value">Systematic &amp; evidence-based</div>
                </div>
                <div class="phi-stat">
                  <div class="phi-stat-label">Focus</div>
                  <div class="phi-stat-value">Risk before return</div>
                </div>
                <div class="phi-stat">
                  <div class="phi-stat-label">Mandates</div>
                  <div class="phi-stat-value">Bespoke constraints</div>
                </div>
              </div>
            </div>

            <div style="flex:1 1 230px;min-width:230px;display:flex;flex-direction:column;gap:0.7rem;justify-content:flex-start;">
              <div class="phi-badge">
                <span>📊</span>
                <span>Markowitz mean–variance architecture with robust covariance (Ledoit–Wolf).</span>
              </div>
              <div class="phi-badge">
                <span>🧭</span>
                <span>Client-specific risk profile translated into a clear risk-aversion parameter (γ).</span>
              </div>
              <div class="phi-badge">
                <span>🌱</span>
                <span>ESG &amp; sector constraints built into the optimizer, not added as an afterthought.</span>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- WHO WE ARE / WHAT WE DO / HOW WE INVEST ---
    st.markdown('<div class="phi-section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="phi-section-title">Who we are &amp; how we invest</div>
        <div class="phi-section-subtitle">
          Our starting point is simple: clients accept market risk, we accept process risk.
          We cannot control markets – but we can control how disciplined, transparent and robust
          our investment process is.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="phi-card-grid">
          <div class="phi-card">
            <div class="phi-card-icon">🧠</div>
            <div class="phi-card-title">Quantitative, not impersonal</div>
            <div class="phi-card-text">
              We rely on data, statistics and portfolio theory to build portfolios,
              but we never forget that behind each mandate there is a family,
              a company, or an institution with real obligations. Our work is to
              translate those constraints into numbers the optimizer understands.
            </div>
          </div>

          <div class="phi-card">
            <div class="phi-card-icon">🧩</div>
            <div class="phi-card-title">From story to constraints</div>
            <div class="phi-card-text">
              Every “I can’t afford a 40% drawdown”, “I want equity exposure but not to any one sector”,
              or “ESG is important, but not at any price” becomes a formal constraint in the model.
              This forces us to be explicit, consistent and accountable in how we manage risk.
            </div>
          </div>

          <div class="phi-card">
            <div class="phi-card-icon">🔍</div>
            <div class="phi-card-title">Transparency by design</div>
            <div class="phi-card-text">
              The app you are using is the same engine we use internally:
              you can see the filters, constraints and backtests exactly as we do.
              There is no “investment committee magic” between the portfolio you see
              and the portfolio we would implement.
            </div>
          </div>

          <div class="phi-card">
            <div class="phi-card-icon">🛡️</div>
            <div class="phi-card-title">Risk before return</div>
            <div class="phi-card-text">
              We accept that market cycles are unpredictable. Instead of promising the
              unattainable, we focus on position sizing, diversification, max-weight controls
              and drawdown awareness – the levers that are actually under our control.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # --- OUR PROCESS / CLIENT JOURNEY ---
    st.markdown('<div class="phi-section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="phi-pill-small">Our process · From conversation to portfolio</div>
        <div class="phi-section-title">How we work with you</div>
        <div class="phi-section-subtitle">
          We try to make the journey from first discussion to live portfolio as
          clear and predictable as the portfolios themselves.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="phi-process">
          <div class="phi-step">
            <div class="phi-step-label">Step 1</div>
            <div class="phi-step-title">Understand your reality</div>
            <div class="phi-step-text">
              We start with your balance sheet, liabilities, time horizon and
              tolerance to drawdowns – not abstract risk questionnaires.
              The result is a documented risk profile and a clear mandate.
            </div>
          </div>

          <div class="phi-step">
            <div class="phi-step-label">Step 2</div>
            <div class="phi-step-title">Translate into rules</div>
            <div class="phi-step-text">
              Together we define the investment universe, ESG &amp; sector rules,
              concentration limits and liquidity requirements. These become
              explicit constraints for the optimizer.
            </div>
          </div>

          <div class="phi-step">
            <div class="phi-step-label">Step 3</div>
            <div class="phi-step-title">Build &amp; backtest</div>
            <div class="phi-step-text">
              We run long-only Markowitz optimizations with robust covariance,
              backtest the strategy through multiple market regimes and stress
              test key assumptions before capital is deployed.
            </div>
          </div>

          <div class="phi-step">
            <div class="phi-step-label">Step 4</div>
            <div class="phi-step-title">Monitor &amp; report</div>
            <div class="phi-step-text">
              Once invested, we rebalance at the agreed frequency and provide
              transparent reporting on performance, risk and adherence to your mandate.
              No surprises, no style drift.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # --- CONTACT / CALL TO ACTION ---
    st.markdown(
        """
        <div class="phi-contact">
          <div class="phi-contact-title">Let’s talk about your constraints, not a generic model.</div>
          <div class="phi-contact-text">
            If you would like to explore what a fully transparent, rule-based portfolio
            could look like for your situation, you can reach us directly or share
            your mandate constraints for a first diagnostic.
          </div>

          <div class="phi-contact-row">
            <div class="phi-contact-chip">
              <span>📧</span>
              <span>Email:&nbsp;
                <a href="mailto:contact@phi-investment.capital">
                  contact@phi-investment.capital
                </a>
              </span>
            </div>

            <div class="phi-contact-chip">
              <span>📄</span>
              <span>Send us a short description of your objectives, constraints and time horizon.</span>
            </div>
          </div>

          <div style="margin-top:0.8rem;" class="phi-contact-note">
            We typically respond within one business day. Please note that we do not provide
            investment advice through this app – any discussion begins with understanding
            your situation and regulatory context.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

        ### Who we are
        We are a quantitative asset & risk management boutique.

        Our mission is to build **transparent, rule-based portfolios**
        tailored to each client's risk profile, constraints and ESG preferences.

        ### What this app does
        - Builds a diversified multi-asset portfolio (Equity, Fixed Income, Commodities, Alternatives)
        - Applies **sector** and **ESG** constraints inside the equity bucket
        - Applies **asset-class** constraints at the total portfolio level
        - Optimizes using a **Markowitz mean–variance** model with a robust covariance estimator (Ledoit–Wolf)
        - Backtests the strategy over the selected horizon

        Use the *Portfolio optimization* page from the sidebar to try it.
        """
    )


# --------------- PAGE 2: PORTFOLIO OPTIMIZATION ---------------
def page_portfolio_optimization(data):
    st.title("Portfolio Optimization")

    st.markdown(
        """
        This tool builds a **constrained multi-asset portfolio** based on your preferences:

        1. Choose the **market universe & technical settings**  
        2. Refine the **investment universe with filters** (sectors, ESG, asset classes)  
        3. Answer a short **risk profile questionnaire**  
        4. Set **portfolio constraints** (sectors, ESG, asset classes, max weights)  
        5. Run the **optimization & backtest** and analyze the results  
        """
    )

    # ============================================================
    # STEP 1 – GENERAL SETTINGS
    # ============================================================
    st.markdown("### Step 1 – General Settings")

    colA, colB, colC, colD, colE = st.columns(5)

    with colA:
        universe_choice = st.radio(
            "Equity Universe",
            options=["SP500", "MSCI"],
            format_func=lambda x: "S&P 500" if x == "SP500" else "MSCI World",
        )

    with colB:
        investment_amount = st.number_input(
            "Investment Amount",
            min_value=1_000_000.0,
            value=1_000_000.0,
            step=100_000.0,
            help="Portfolio simulations and backtests will be expressed in this monetary amount.",
        )
        mgmt_fee_annual = management_fee_from_wealth(investment_amount)
        st.caption(
            f"Estimated annual management fee: **{mgmt_fee_annual:.2%}** "
            "(applied pro rata on a monthly basis)."
        )

    with colC:
        investment_horizon_years = st.selectbox(
            "Investment Horizon",
            options=[1, 2, 3, 5, 7, 10],
            index=0,
            format_func=lambda x: f"{x} year" if x == 1 else f"{x} years",
        )

    with colD:
        rebalance_label = st.selectbox(
            "Rebalancing Frequency",
            options=["Yearly", "Quarterly", "Monthly"],
            index=0,
        )
        if rebalance_label == "Yearly":
            rebalancing = 12
        elif rebalance_label == "Quarterly":
            rebalancing = 3
        else:
            rebalancing = 1

    with colE:
        est_months = st.selectbox(
            "Estimation Window",
            options=[6, 12, 24, 36, 60],
            index=1,
            format_func=lambda m: f"{m} months",
        )

    st.markdown("---")

    # ============================================================
    # STEP 2 – UNIVERSE & FILTERS
    # ============================================================
    st.markdown("### Step 2 – Universe & Filters")

    # --- Get metadata for chosen equity universe and other assets ---
    if universe_choice == "SP500":
        metadata_equity = data["metadata"]["SP500"]
    else:
        metadata_equity = data["metadata"]["MSCI"]

    metadata_other = data["metadata"]["Other"]

    # ---------- 2.1 Equity filters: sectors & ESG ----------
    st.subheader("Equity Filters")

    sectors_available = (
        metadata_equity["SECTOR"]
        .dropna()
        .astype(str)
        .sort_values()
        .unique()
        .tolist()
    )

    col_sect, col_esg = st.columns(2)

    with col_sect:
        selected_sectors = st.multiselect(
            "Sectors to include in equity universe",
            options=sectors_available,
            default=sectors_available,
            help="If you select all sectors, no sector filter is applied.",
        )

        if len(selected_sectors) == len(sectors_available) or len(selected_sectors) == 0:
            keep_sectors = None
        else:
            keep_sectors = selected_sectors

    with col_esg:
        esg_options = ["L", "M", "H"]
        selected_esg = st.multiselect(
            "ESG categories to include",
            options=esg_options,
            default=esg_options,
            help="L = Low, M = Medium, H = High. Selecting all applies no ESG filter.",
        )

        if len(selected_esg) == len(esg_options) or len(selected_esg) == 0:
            keep_esg = None
        else:
            keep_esg = selected_esg

    # ---------- 2.2 Other asset classes & instruments ----------
    st.subheader("Other Asset Classes")

    asset_classes_all = (
        metadata_other["ASSET_CLASS"]
        .dropna()
        .astype(str)
        .sort_values()
        .unique()
        .tolist()
    )

    selected_asset_classes_other = st.multiselect(
        "Asset classes to include in the universe (beyond equity)",
        options=asset_classes_all,
        default=asset_classes_all,
        help="These asset classes will be available to the optimizer. "
        "Constraints later control how much can be allocated to each.",
    )

    keep_ids_by_class = {}

    for ac in selected_asset_classes_other:
        subset = metadata_other[metadata_other["ASSET_CLASS"] == ac]
        ids_in_class = subset.index.astype(str).tolist()

        # Label map for nicer display
        label_map = {}
        if "TICKER" in subset.columns:
            for idx, row in subset.iterrows():
                label_map[str(idx)] = f"{row['TICKER']}"
        elif "NAME" in subset.columns:
            for idx, row in subset.iterrows():
                label_map[str(idx)] = f"{row['NAME']}"
        else:
            for idx in subset.index:
                label_map[str(idx)] = str(idx)

        labeled_options = [f"{id_} – {label_map[id_]}" for id_ in ids_in_class]

        st.markdown(f"**{ac} instruments to include**")
        selected_labels = st.multiselect(
            f"Select {ac} instruments (leave all selected to keep full class)",
            options=labeled_options,
            default=labeled_options,
        )

        selected_ids = [s.split(" – ")[0] for s in selected_labels]

        if 0 < len(selected_ids) < len(ids_in_class):
            keep_ids_by_class[ac] = selected_ids

    keep_ids_by_class = keep_ids_by_class if keep_ids_by_class else None

    st.markdown("---")

    # ============================================================
    # STEP 3 – RISK PROFILE QUESTIONNAIRE → GAMMA
    # ============================================================
    st.markdown("### Step 3 – Risk Profile Questionnaire")

    st.caption(
        "Answer each question on a 1–5 scale. "
        "1 = very conservative, 5 = very aggressive."
    )

    col_left, col_right = st.columns(2)

    with col_left:
        q1 = st.slider(
            "1. Reaction to a -20% loss in one year\n"
            "1 = sell everything, 5 = buy more",
            min_value=1,
            max_value=5,
            value=3,
        )

        q2 = st.slider(
            "2. Comfort with large fluctuations\n"
            "1 = not at all, 5 = very comfortable",
            min_value=1,
            max_value=5,
            value=3,
        )

        q3 = st.slider(
            "3. Return vs risk trade-off\n"
            "1 = stable low returns, 5 = max return even with large risk",
            min_value=1,
            max_value=5,
            value=3,
        )

        q4 = st.slider(
            "4. Investment horizon\n"
            "1 = < 1 year, 5 = > 10 years",
            min_value=1,
            max_value=5,
            value=3,
        )

        q5 = st.slider(
            "5. How do you view risk?\n"
            "1 = something to avoid, 5 = essential for higher returns",
            min_value=1,
            max_value=5,
            value=3,
        )

    with col_right:
        q6 = st.slider(
            "6. Stress during market crashes\n"
            "1 = extremely stressed, 5 = not stressed at all",
            min_value=1,
            max_value=5,
            value=3,
        )

        q7 = st.slider(
            "7. Stability of your income/finances\n"
            "1 = very unstable, 5 = very stable",
            min_value=1,
            max_value=5,
            value=3,
        )

        q8 = st.slider(
            "8. Experience with investing\n"
            "1 = not familiar, 5 = very experienced",
            min_value=1,
            max_value=5,
            value=3,
        )

        q9 = st.slider(
            "9. Reaction to a +20% gain in one year\n"
            "1 = sell to lock gains, 5 = add significantly more money",
            min_value=1,
            max_value=5,
            value=3,
        )

        q10 = st.slider(
            "10. Share of net worth in risky assets\n"
            "1 = < 10%, 5 = > 60%",
            min_value=1,
            max_value=5,
            value=3,
        )

    scores = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    S = sum(scores)
    gamma = 0.5 + 0.15 * (S - 10)  # internal only

    if S <= 20:
        profile_label = "Very Conservative"
        profile_text = (
            "You have a **very low tolerance for risk** and prefer capital preservation. "
            "The portfolio will be tilted towards safer, lower-volatility assets."
        )
    elif S <= 30:
        profile_label = "Conservative"
        profile_text = (
            "You are **cautious with risk**, but willing to accept some fluctuations. "
            "The portfolio will prioritize stability with a moderate growth component."
        )
    elif S <= 35:
        profile_label = "Balanced"
        profile_text = (
            "You have a **balanced attitude** towards risk and return. "
            "The portfolio will mix growth assets with stabilizing components."
        )
    elif S <= 42:
        profile_label = "Dynamic"
        profile_text = (
            "You are **comfortable with risk** and seek higher returns. "
            "The portfolio will have a strong allocation to growth and risky assets."
        )
    else:
        profile_label = "Aggressive"
        profile_text = (
            "You have a **high risk tolerance** and focus on return maximization. "
            "The portfolio will be heavily exposed to volatile, return-seeking assets."
        )

    st.markdown("")
    col_score, col_profile = st.columns(2)
    with col_score:
        st.metric("Total Risk Score (S)", f"{S} / 50")
    with col_profile:
        st.markdown(f"**Risk Profile:** {profile_label}")
        st.caption(profile_text)

    st.markdown("---")

    # ============================================================
    # STEP 4 – CONSTRAINTS
    # ============================================================
    st.markdown("### Step 4 – Constraints")

    st.caption(
        "All constraints are expressed as **fractions** (0.10 = 10%). "
        "Leave min = 0 and max = 1 to avoid imposing a constraint."
    )

    # ------------------------------------------------------------
    # 4.1 Max weight per asset (with safe default + warning)
    # ------------------------------------------------------------
    st.subheader("Maximum Weight per Asset")

    use_custom_max = st.checkbox(
        "Enable custom maximum weight per asset",
        value=False,
        help="By default, each asset is capped at 5%. Enable only if you understand concentration risk.",
    )

    if not use_custom_max:
        max_weight_per_asset = 0.05
        st.info("Using default limit: **5% maximum per individual asset**.")
    else:
        max_weight_per_asset = st.slider(
            "Select maximum weight per asset",
            min_value=0.01,
            max_value=0.25,
            value=0.05,
            step=0.01,
            help="Higher caps increase concentration risk and may reduce diversification.",
        )

        st.warning(
            "**Caution:** Increasing the maximum weight per asset may significantly raise your "
            "**idiosyncratic risk** and reduce the portfolio's **diversification benefits**. "
            "Large individual exposures can amplify the impact of adverse movements in a single "
            "security, especially during periods of market stress."
        )

    st.markdown("---")

    # ------------------------------------------------------------
    # 4.2 Sector constraints within equity (relative to equity)
    # ------------------------------------------------------------
    st.subheader("Equity Sector Constraints (relative to the equity exposure)")

    if keep_sectors is None:
        sectors_for_constraints = sectors_available
    else:
        sectors_for_constraints = keep_sectors

    sector_constraints = {}
    sector_min_budget = 0.0  # sum of mins so far, must stay <= 1

    for sec in sectors_for_constraints:
        remaining_min_budget = max(0.0, 1.0 - sector_min_budget)

        with st.expander(f"{sec}", expanded=False):
            col_min, col_max = st.columns(2)

            with col_min:
                sec_min = st.number_input(
                    f"Min share of {sec} in Equity",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.0,
                    step=0.01,
                    format="%.2f",
                    key=f"sec_min_{sec}",
                )

            # update budget after this min
            sector_min_budget += sec_min

            with col_max:
                sec_max = st.number_input(
                    f"Max share of {sec} in Equity",
                    min_value=0.0,  # ensures min <= max
                    max_value=1.0,
                    value=1.0,
                    step=0.01,
                    format="%.2f",
                    key=f"sec_max_{sec}",
                )

            # Professional-style warnings at boundaries
            eps = 1e-8
            if remaining_min_budget > 0 and abs(sec_min - remaining_min_budget) < eps:
                st.warning(
                    f"The minimum allocation entered for **{sec}** is at the upper feasible bound. "
                    "Any higher minimum would force the sum of sector minima above **100% of the equity slice** "
                    "and is therefore not admissible."
                )

            if sec_min > 0 and abs(sec_max - sec_min) < eps:
                st.info(
                    f"For **{sec}**, the minimum and maximum allocations are effectively identical. "
                    "This leaves no flexibility for the optimizer to rebalance within this sector."
                )

        cons = {}
        if sec_min > 0:
            cons["min"] = float(sec_min)
        if sec_max < 1.0:
            cons["max"] = float(sec_max)
        if cons:
            sector_constraints[sec] = cons

    if not sector_constraints:
        sector_constraints = None

    st.markdown("---")

    # ------------------------------------------------------------
    # 4.3 ESG constraints within equity (relative to equity)
    # ------------------------------------------------------------
    st.subheader("Equity ESG Score Constraints (relative to the equity exposure)")

    esg_all_labels = ["L", "M", "H"]
    if keep_esg is None:
        esg_for_constraints = esg_all_labels
    else:
        esg_for_constraints = keep_esg

    esg_constraints = {}
    esg_min_budget = 0.0

    for label in esg_for_constraints:
        remaining_min_budget = max(0.0, 1.0 - esg_min_budget)

        with st.expander(f"ESG {label}", expanded=False):
            col_min, col_max = st.columns(2)

            with col_min:
                esg_min = st.number_input(
                    f"Min share of ESG {label} score in Equity",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.0,
                    step=0.01,
                    format="%.2f",
                    key=f"esg_min_{label}",
                )

            esg_min_budget += esg_min

            with col_max:
                esg_max = st.number_input(
                    f"Max share ESG {label} score in Equity",
                    min_value=0.0,
                    max_value=1.0,
                    value=1.0,
                    step=0.01,
                    format="%.2f",
                    key=f"esg_max_{label}",
                )

            eps = 1e-8
            if remaining_min_budget > 0 and abs(esg_min - remaining_min_budget) < eps:
                st.warning(
                    f"The minimum allocation entered for **ESG {label}** is at the upper feasible bound. "
                    "Any higher minimum would force the sum of ESG minima above **100% of the equity slice** "
                    "and is therefore not admissible."
                )

            if esg_min > 0 and abs(esg_max - esg_min) < eps:
                st.info(
                    f"For **ESG {label}**, the minimum and maximum allocations are effectively identical. "
                    "This leaves no flexibility for the optimizer within this ESG bucket."
                )

        cons = {}
        if esg_min > 0:
            cons["min"] = float(esg_min)
        if esg_max < 1.0:
            cons["max"] = float(esg_max)
        if cons:
            esg_constraints[label] = cons

    if not esg_constraints:
        esg_constraints = None

    st.markdown("---")

    # ------------------------------------------------------------
    # 4.4 Asset-class constraints (total portfolio)
    # ------------------------------------------------------------
    st.subheader("Asset-Class Constraints (total portfolio)")

    if not selected_asset_classes_other:
        st.info(
            "You have selected an **equity-only universe**. "
            "By construction, 100% of the portfolio will be invested in Equity."
        )
        asset_class_constraints = None

    else:
        asset_classes_for_constraints = ["Equity"] + selected_asset_classes_other

        asset_class_constraints = {}
        ac_min_budget = 0.0

        for ac in asset_classes_for_constraints:
            remaining_min_budget = max(0.0, 1.0 - ac_min_budget)

            with st.expander(f"{ac}", expanded=False):
                col_min, col_max = st.columns(2)

                with col_min:
                    ac_min = st.number_input(
                        f"Min portfolio weight in {ac}",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.0,
                        step=0.05,
                        format="%.2f",
                        key=f"ac_min_{ac}",
                    )

                ac_min_budget += ac_min

                with col_max:
                    ac_max = st.number_input(
                        f"Max portfolio weight in {ac}",
                        min_value=0.0,
                        max_value=1.0,
                        value=1.0,
                        step=0.05,
                        format="%.2f",
                        key=f"ac_max_{ac}",
                    )

                eps = 1e-8
                if remaining_min_budget > 0 and abs(ac_min - remaining_min_budget) < eps:
                    st.warning(
                        f"The minimum allocation entered for **{ac}** is at the upper feasible bound. "
                        "Any higher minimum would force the sum of asset-class minima above **100% of the portfolio** "
                        "and is therefore not admissible."
                    )

                if ac_min > 0 and abs(ac_max - ac_min) < eps:
                    st.info(
                        f"For **{ac}**, the minimum and maximum allocations are effectively identical. "
                        "This leaves no flexibility for the optimizer to reallocate across asset classes."
                    )

            cons = {}
            if ac_min > 0:
                cons["min"] = float(ac_min)
            if ac_max < 1.0:
                cons["max"] = float(ac_max)
            if cons:
                asset_class_constraints[ac] = cons

        if not asset_class_constraints:
            asset_class_constraints = None

        st.markdown("---")

    constraint_errors = validate_constraints(
        sector_constraints=sector_constraints,
        esg_constraints=esg_constraints,
        asset_class_constraints=asset_class_constraints,
    )

    if constraint_errors:
        st.error("The current constraint configuration is not feasible:")
        for msg in constraint_errors:
            st.write(f"• {msg}")

    # ============================================================
    # STEP 5 – RUN OPTIMIZATION & BACKTEST
    # ============================================================
    st.markdown("### Step 5 – Run Optimization & Backtest")

    run_clicked = st.button(
        "Run Optimization & Backtest",
        type="primary",
        disabled=bool(constraint_errors),
    )

    # ---- 5A) Run the backtest only when button is clicked ----
    if run_clicked:
        # 1) Check constraints first
        if constraint_errors:
            st.error("The current constraint configuration is not feasible:")
            for msg in constraint_errors:
                st.write(f"• {msg}")
            st.stop()  # do not run the optimizer

        # 2) Build config only if constraints are okay
        config = PortfolioConfig(
            today_date=pd.Timestamp("2025-10-01"),
            investment_horizon_years=investment_horizon_years,
            est_months=est_months,
            rebalancing=rebalancing,
            gamma=gamma,
            universe_choice=universe_choice,
            keep_sectors=keep_sectors,
            keep_esg=keep_esg,
            selected_asset_classes_other=selected_asset_classes_other,
            keep_ids_by_class=keep_ids_by_class,
            max_weight_per_asset=max_weight_per_asset,
            sector_constraints=sector_constraints,
            esg_constraints=esg_constraints,
            asset_class_constraints=asset_class_constraints,
            initial_wealth=investment_amount,
        )

        # 3) Run **ONLY** the backtest here (timed)
        try:
            with st.spinner("Optimizing and backtesting..."):
                t0 = time.perf_counter()
                perf, summary_df, debug_weights_df = run_backtest(config, data)
                t1 = time.perf_counter()

            st.write(f"⏱️ Backtest time: {t1 - t0:.2f} seconds")

        except ValueError as e:
            st.error(
                "The optimizer could not find a feasible portfolio with the current constraints."
            )
            st.caption(
                "This usually means sector/ESG minimums or max-weight-per-asset are too tight."
            )
            st.stop()

        st.success("Backtest completed.")

        # store everything — NOT today's optimization
        st.session_state["backtest_results"] = {
            "config": config,
            "perf": perf,
            "summary_df": summary_df,
            "debug_weights_df": debug_weights_df,
            "today_res": None,
            "investment_amount": investment_amount,
            "universe_choice": universe_choice,
            "investment_horizon_years": investment_horizon_years,
            "est_months": est_months,
            "rebalancing": rebalancing,
            "gamma": gamma,
            "profile_label": profile_label,
            "max_weight_per_asset": max_weight_per_asset,
            "selected_asset_classes_other": selected_asset_classes_other,
            "sector_constraints": sector_constraints,
            "esg_constraints": esg_constraints,
            "asset_class_constraints": asset_class_constraints,
        }

    # ---- 5B) If we have results in session_state, display them ----
    if "backtest_results" in st.session_state:
        r = st.session_state["backtest_results"]

        config = r["config"]  # full config stored
        perf = r["perf"]
        summary_df = r["summary_df"]
        debug_weights_df = r["debug_weights_df"]
        today_res = r.get("today_res")  # may be None the first time

        investment_amount = r["investment_amount"]
        universe_choice = r["universe_choice"]
        investment_horizon_years = r["investment_horizon_years"]
        est_months = r["est_months"]
        rebalancing = r["rebalancing"]
        gamma = r["gamma"]
        profile_label = r["profile_label"]
        max_weight_per_asset = r["max_weight_per_asset"]
        selected_asset_classes_other = r["selected_asset_classes_other"]
        sector_constraints = r["sector_constraints"]
        esg_constraints = r["esg_constraints"]
        asset_class_constraints = r["asset_class_constraints"]

        tab_backtest, tab_today = st.tabs(["📈 Backtest", "📌 Today's Portfolio"])

        # ======================= BACKTEST TAB =======================
        with tab_backtest:
            st.subheader("Backtest Performance")

            if not perf.empty:
                # 1) Compute backtest stats (for max drawdown, etc.)
                stats = compute_backtest_stats(perf)

                # --------------------------------------------------------
                # A) BUILD DATAFRAME WITH PORTFOLIO + BENCHMARKS (CUMRET)
                # --------------------------------------------------------
                returns_bench = data.get("benchmarks", None)

                if returns_bench is not None and not returns_bench.empty:
                    bench = returns_bench.reindex(perf.index)
                    bench_cum = (1.0 + bench).cumprod() - 1.0
                    combined = pd.concat([perf["CumReturn"], bench_cum], axis=1)
                    combined.columns = ["Portfolio"] + list(bench_cum.columns)
                else:
                    combined = pd.DataFrame({"Portfolio": perf["CumReturn"]})

                # Convert index to timestamp
                if isinstance(combined.index, pd.PeriodIndex):
                    combined.index = combined.index.to_timestamp()

                chart_data = combined.reset_index().rename(columns={"Date": "Date"})

                chart_data_long = chart_data.melt(
                    "Date", var_name="Series", value_name="Return"
                )

                # --------------------------------------------------------
                # B) CUMULATIVE RETURN CHART WITH BENCHMARKS
                # --------------------------------------------------------
                st.markdown("**Cumulative Return of the Strategy vs Benchmarks**")

                max_ret = (
                    float(chart_data_long["Return"].max())
                    if not chart_data_long["Return"].isna().all()
                    else 0.0
                )
                max_ret = max(max_ret, 0.0)
                max_tick = (int(max_ret * 10) + 1) / 10.0 if max_ret > 0 else 0.1
                tick_values = [i / 10.0 for i in range(0, int(max_tick * 10) + 1)]

                base_ret = (
                    alt.Chart(chart_data_long)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X(
                            "Date:T",
                            axis=alt.Axis(format="%b %Y", labelAngle=-45),
                        ),
                        y=alt.Y(
                            "Return:Q",
                            title="Cumulative return",
                            scale=alt.Scale(domain=[0, max_tick], nice=False),
                            axis=alt.Axis(format="%", values=tick_values),
                        ),
                        color=alt.Color(
                            "Series:N",
                            sort=["Portfolio", "S&P 500", "MSCI WORLD"],
                        ),
                        tooltip=[
                            alt.Tooltip(
                                "Date:T", title="Date", format="%b %Y"
                            ),
                            alt.Tooltip("Series:N", title="Series"),
                            alt.Tooltip(
                                "Return:Q",
                                title="Cumulative return",
                                format=".2%",
                            ),
                        ],
                    )
                )

                # Drawdown vertical lines
                if stats and stats["max_drawdown_start"] is not None:
                    dd_start, dd_end = (
                        stats["max_drawdown_start"],
                        stats["max_drawdown_end"],
                    )
                    vline_data = pd.DataFrame(
                        {"Date": [dd_start, dd_end], "Label": ["DD start", "DD end"]}
                    )

                    vlines = (
                        alt.Chart(vline_data)
                        .mark_rule(color="red", strokeDash=[4, 4], size=2)
                        .encode(x="Date:T")
                    )

                    chart_ret = alt.layer(base_ret, vlines).interactive()
                else:
                    chart_ret = base_ret.interactive()

                st.altair_chart(chart_ret, use_container_width=True)

                st.markdown(
                    "<span style='color:red;'>Red dashed vertical lines indicate the "
                    "<b>start</b> and <b>end</b> of the worst drawdown observed over the backtest period.</span>",
                    unsafe_allow_html=True,
                )

                st.markdown("---")

                # --------------------------------------------------------
                # C) SECOND CHART – PORTFOLIO WEALTH
                # --------------------------------------------------------
                st.markdown("**Evolution of Portfolio Wealth**")

                perf_plot = perf.copy()
                if isinstance(perf_plot.index, pd.PeriodIndex):
                    perf_plot.index = perf_plot.index.to_timestamp()
                perf_plot = perf_plot.reset_index()

                max_wealth = float(perf["Wealth"].max())
                upper_wealth = max(max_wealth, 1.0) * 1.05

                base_wealth = (
                    alt.Chart(perf_plot)
                    .mark_line(point=True)
                    .encode(
                        x=alt.X(
                            "Date:T",
                            axis=alt.Axis(format="%b %Y", labelAngle=-45),
                        ),
                        y=alt.Y(
                            "Wealth:Q",
                            scale=alt.Scale(domain=[0, upper_wealth]),
                        ),
                        tooltip=[
                            alt.Tooltip("Date:T"),
                            alt.Tooltip("Wealth:Q", format=",.0f"),
                        ],
                    )
                )

                if stats and stats["max_drawdown_start"] is not None:
                    chart_wealth = alt.layer(base_wealth, vlines).interactive()
                else:
                    chart_wealth = base_wealth.interactive()

                st.altair_chart(chart_wealth, use_container_width=True)

                # --------------------------------------------------------
                # D) BACKTEST STATISTICS TABLE
                # --------------------------------------------------------
                st.markdown("**Backtest Statistics**")

                initial = investment_amount
                final_wealth = investment_amount * float(perf["Growth"].iloc[-1])

                def fmt_pct(x):
                    return f"{x:.2%}"

                stats_rows = [
                    ("Initial invested wealth", f"{initial:,.0f}"),
                    ("Final wealth at end of backtest", f"{final_wealth:,.0f}"),
                    (
                        "Annualised average return",
                        fmt_pct(stats["annualised_avg_return"]),
                    ),
                    (
                        "Annualised volatility",
                        fmt_pct(stats["annualised_volatility"]),
                    ),
                    (
                        "Annualised cumulative return",
                        fmt_pct(stats["annualised_cum_return"]),
                    ),
                    ("Min monthly return", fmt_pct(stats["min_monthly_return"])),
                    ("Max monthly return", fmt_pct(stats["max_monthly_return"])),
                    ("Max drawdown", fmt_pct(stats["max_drawdown"])),
                    (
                        "Max drawdown start",
                        stats["max_drawdown_start"].strftime("%b %Y"),
                    ),
                    (
                        "Max drawdown end",
                        stats["max_drawdown_end"].strftime("%b %Y"),
                    ),
                    (
                        "Max drawdown duration",
                        f"{stats['max_drawdown_duration_months']} months",
                    ),
                ]

                st.table(pd.DataFrame(stats_rows, columns=["Metric", "Value"]))

                # --------------------------------------------------------
                # E) AI Commentary on the Backtest
                # --------------------------------------------------------
                st.markdown("### AI Commentary on Backtest Results")

                explain_btn = st.button(
                    "Generate AI Commentary on Backtest",
                    type="secondary",
                    help=(
                        "Ask the Phi Investment Capital digital assistant to provide a "
                        "client-friendly interpretation of the backtest results."
                    ),
                )

                if explain_btn:
                    client_llm = get_llm_client()

                    # Build a textual context for the model, including client inputs
                    context_text = build_backtest_context_text(
                        stats=stats,
                        perf=perf,
                        investment_amount=investment_amount,
                        universe_choice=universe_choice,
                        investment_horizon_years=investment_horizon_years,
                        est_months=est_months,
                        rebalancing=rebalancing,
                        gamma=gamma,
                        profile_label=profile_label,
                        max_weight_per_asset=max_weight_per_asset,
                        selected_asset_classes_other=selected_asset_classes_other,
                        sector_constraints=sector_constraints,
                        esg_constraints=esg_constraints,
                        asset_class_constraints=asset_class_constraints,
                    )

                    system_prompt = (
                        "You are a digital investment assistant for Phi Investment Capital. "
                        "You are given a summary of a client's configuration and portfolio backtest. "
                        "Provide a professional, client-friendly commentary on the results.\n\n"
                        "Guidelines:\n"
                        "- Refer to the client's risk profile, constraints, and investment horizon when relevant.\n"
                        "- Comment on constraints the client choose"
                        "- Comment on the balance between return and risk (volatility and drawdowns).\n"
                        "- Highlight any notable features of the drawdown profile and overall behaviour over time.\n"
                        "- You may mention that tighter constraints or lower max weights can limit performance but improve diversification.\n"
                        "- Do NOT give investment recommendations or instructions to buy/sell.\n"
                        "- Do NOT make promises about future performance.\n"
                        "- Keep the answer to about 2–5 short paragraphs, in a calm and professional tone."
                    )

                    user_message = (
                        "Here is the full context (client configuration and backtest summary). "
                        "Please provide a concise commentary for the client:\n\n"
                        f"{context_text}"
                    )

                    with st.spinner("Generating AI commentary..."):
                        response = client_llm.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": user_message},
                            ],
                        )
                        commentary = response.choices[0].message.content

                    st.markdown(
                        """
                        **Phi Investment Capital – Backtest Commentary**  
                        *(Generated by the digital assistant based on your inputs and the statistics above.)*
                        """
                    )
                    st.markdown(commentary)
            else:
                st.warning("No valid backtest window for the selected settings.")

        # ======================= TODAY'S PORTFOLIO TAB =======================
        with tab_today:
            st.subheader("Today's Optimal Portfolio")

            # Lazily compute today's optimal portfolio only the first time
            today_res = r.get("today_res")
            if today_res is None:
                with st.spinner("Computing today's optimal portfolio..."):
                    today_res = run_today_optimization(config, data)
                # cache in session_state so we don't recompute
                st.session_state["backtest_results"]["today_res"] = today_res

            today_df = today_res["weights"]
            top5 = today_res["top5"]
            alloc_by_ac = today_res["alloc_by_asset_class"]
            sector_in_eq = today_res["sector_in_equity"]
            esg_in_eq = today_res["esg_in_equity"]

            st.markdown("**Top 5 Holdings**")
            st.dataframe(top5)

            colA, colB, colC = st.columns(3)

            # ----- Asset-class allocation -----
            with colA:
                st.markdown("**By Asset Class**")

                if not alloc_by_ac.empty:
                    df_ac = alloc_by_ac.reset_index()
                    df_ac.columns = ["AssetClass", "Weight"]

                    df_ac["Min"] = df_ac["AssetClass"].map(
                        lambda ac: asset_class_constraints.get(ac, {}).get("min", None)
                        if asset_class_constraints
                        else None
                    )
                    df_ac["Max"] = df_ac["AssetClass"].map(
                        lambda ac: asset_class_constraints.get(ac, {}).get("max", None)
                        if asset_class_constraints
                        else None
                    )

                    bars_ac = (
                        alt.Chart(df_ac)
                        .mark_bar(color="#4BA3FF")
                        .encode(
                            x=alt.X("AssetClass:N", title=""),
                            y=alt.Y("Weight:Q", title="Portfolio weight"),
                            tooltip=[
                                alt.Tooltip("AssetClass:N", title="Asset class"),
                                alt.Tooltip(
                                    "Weight:Q", title="Weight", format=".2%"
                                ),
                            ],
                        )
                    )

                    min_marks_ac = (
                        alt.Chart(df_ac)
                        .mark_tick(
                            orient="horizontal",
                            color="yellow",
                            size=40,
                            thickness=3,
                        )
                        .encode(
                            x="AssetClass:N",
                            y="Min:Q",
                            tooltip=[
                                alt.Tooltip("Min:Q", title="Min", format=".2%")
                            ],
                        )
                        .transform_filter("datum.Min != null")
                    )

                    max_marks_ac = (
                        alt.Chart(df_ac)
                        .mark_tick(
                            orient="horizontal",
                            color="red",
                            size=40,
                            thickness=3,
                        )
                        .encode(
                            x="AssetClass:N",
                            y="Max:Q",
                            tooltip=[
                                alt.Tooltip("Max:Q", title="Max", format=".2%")
                            ],
                        )
                        .transform_filter("datum.Max != null")
                    )

                    chart_ac = (bars_ac + min_marks_ac + max_marks_ac).properties(
                        height=300
                    ).interactive()

                    st.altair_chart(chart_ac, use_container_width=True)
                else:
                    st.info("No allocation across asset classes.")

            # ----- Sector breakdown -----
            with colB:
                st.markdown("**Sector Breakdown (Equity)**")

                if not sector_in_eq.empty:
                    df_sector = sector_in_eq.reset_index()
                    df_sector.columns = ["Sector", "Weight"]

                    df_sector["Min"] = df_sector["Sector"].map(
                        lambda s: sector_constraints.get(s, {}).get("min", None)
                        if sector_constraints
                        else None
                    )
                    df_sector["Max"] = df_sector["Sector"].map(
                        lambda s: sector_constraints.get(s, {}).get("max", None)
                        if sector_constraints
                        else None
                    )

                    bars = (
                        alt.Chart(df_sector)
                        .mark_bar(color="#4BA3FF")
                        .encode(
                            x=alt.X("Sector:N", title="", sort="-y"),
                            y=alt.Y("Weight:Q", title="Weight in Equity"),
                            tooltip=[
                                alt.Tooltip("Sector:N"),
                                alt.Tooltip("Weight:Q", format=".2%"),
                            ],
                        )
                    )

                    min_marks = (
                        alt.Chart(df_sector)
                        .mark_tick(
                            orient="horizontal",
                            color="yellow",
                            size=40,
                            thickness=3,
                        )
                        .encode(
                            x="Sector:N",
                            y="Min:Q",
                            tooltip=[
                                alt.Tooltip("Min:Q", title="Min", format=".2%")
                            ],
                        )
                        .transform_filter("datum.Min != null")
                    )

                    max_marks = (
                        alt.Chart(df_sector)
                        .mark_tick(
                            orient="horizontal",
                            color="red",
                            size=40,
                            thickness=3,
                        )
                        .encode(
                            x="Sector:N",
                            y="Max:Q",
                            tooltip=[
                                alt.Tooltip("Max:Q", title="Max", format=".2%")
                            ],
                        )
                        .transform_filter("datum.Max != null")
                    )

                    chart_sector = (bars + min_marks + max_marks).properties(
                        height=300
                    ).interactive()

                    st.altair_chart(chart_sector, use_container_width=True)
                else:
                    st.info("No equity allocation.")

            # ----- ESG breakdown -----
            with colC:
                st.markdown("**ESG Breakdown (Equity)**")

                if not esg_in_eq.empty:
                    df_esg = esg_in_eq.reset_index()
                    df_esg.columns = ["ESG", "Weight"]

                    df_esg["Min"] = df_esg["ESG"].map(
                        lambda s: esg_constraints.get(s, {}).get("min", None)
                        if esg_constraints
                        else None
                    )
                    df_esg["Max"] = df_esg["ESG"].map(
                        lambda s: esg_constraints.get(s, {}).get("max", None)
                        if esg_constraints
                        else None
                    )

                    bars_esg = (
                        alt.Chart(df_esg)
                        .mark_bar(color="#4BA3FF")
                        .encode(
                            x=alt.X("ESG:N", title=""),
                            y=alt.Y("Weight:Q", title="Weight in Equity"),
                            tooltip=[
                                alt.Tooltip("ESG:N"),
                                alt.Tooltip("Weight:Q", format=".2%"),
                            ],
                        )
                    )

                    min_marks_esg = (
                        alt.Chart(df_esg)
                        .mark_tick(
                            orient="horizontal",
                            color="yellow",
                            size=40,
                            thickness=3,
                        )
                        .encode(
                            x="ESG:N",
                            y="Min:Q",
                            tooltip=[
                                alt.Tooltip("Min:Q", title="Min", format=".2%")
                            ],
                        )
                        .transform_filter("datum.Min != null")
                    )

                    max_marks_esg = (
                        alt.Chart(df_esg)
                        .mark_tick(
                            orient="horizontal",
                            color="red",
                            size=40,
                            thickness=3,
                        )
                        .encode(
                            x="ESG:N",
                            y="Max:Q",
                            tooltip=[
                                alt.Tooltip("Max:Q", title="Max", format=".2%")
                            ],
                        )
                        .transform_filter("datum.Max != null")
                    )

                    chart_esg = (bars_esg + min_marks_esg + max_marks_esg).properties(
                        height=300
                    ).interactive()

                    st.altair_chart(chart_esg, use_container_width=True)
                else:
                    st.info("No equity allocation.")

            st.markdown(
                "<span style='color:#DAA520;'>Yellow horizontal markers</span> "
                "indicate **minimum allocation bounds** (lower weights), while "
                "<span style='color:red;'>red horizontal markers</span> indicate "
                "**maximum allocation limits** for each sector, ESG bucket or asset class.",
                unsafe_allow_html=True,
            )

            with st.expander("Full Portfolio Weights"):
                st.dataframe(today_df)


# --------------- PAGE 3: AI ---------------
def page_ai_assistant():
    st.title("Phi Assistant ")

    st.markdown(
        """
        Our AI-powered assistant is designed to enhance your experience on our portfolio management platform. 
        It can support you across three key areas.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("1. Platform Guidance & Functionality")
        st.markdown(
            """
            Navigate the application with confidence:

            The assistant can explain each section of the site — 
            from selecting your investment universe to configuring 
            constraints, interpreting backtests, and reviewing today’s 
            optimal portfolio. Whether you're unsure about a step or want to
            understand how a specific feature works, it provides clear, client-friendly guidance.
            """
        )

    with col2:
        st.subheader("2. Financial & Theoretical Concepts")
        st.markdown(
            """
            Understand the rationale behind your portfolio.:

            Ask about diversification, risk/return trade-offs, gamma (risk aversion), the Markowitz optimization 
            framework, or the meaning of any chart or metric shown in the application. The assistant provides clear 
            explanations grounded in quantitative finance — always educational, never advisory.
            """
        )

    with col3:
        st.subheader("3. Market Context & Current Themes")
        st.markdown(
            """
            Stay informed about what’s happening in the financial world.:

            You can request neutral, factual insights about current market conditions, macroeconomic themes, 
            or asset-class developments. The assistant offers high-level context to help you make sense of the 
            broader environment in which portfolios operate.  
            """
        )

    st.markdown(
        """
        ⚠️ **Important:** The assistant provides general information and educational insights only.
        It does **not** offer personalized investment recommendations or specific trading advice.
        """
    )

    client = get_llm_client()

    # Initialize chat history in session_state
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = [
            {
                "role": "system",
                "content": (
                    "You are a digital investment assistant for an asset and risk management firm named "
                    "Phi Investment Capital. You are integrated into a web application. Your name is Phi Assiatant\n\n"
                    "Your primary role is to support clients in understanding:\n"
                    "- How the app works (its pages, steps, and main functionalities)\n"
                    "- The meaning of inputs (risk questionnaire, constraints, filters, universe choices)\n"
                    "- The outputs of the optimizer (performance charts, drawdowns, asset-class/sector/ESG breakdowns)\n"
                    "- General investment concepts related to diversification, risk/return, and portfolio construction\n"
                    "- High-level, factual information about financial markets and asset classes\n\n"
                    "Context about the app's functionality:\n"
                    "- The app has an 'About us' page describing Phi Investment Capital and its quantitative approach.\n"
                    "- The 'Portfolio optimization' page guides the client through:\n"
                    "  1) General settings: equity universe (S&P 500 or MSCI World), investment amount, horizon,\n"
                    "     rebalancing frequency, and estimation window.\n"
                    "  2) Universe & filters: sector and ESG filters for equities, plus selection of other asset classes\n"
                    "     (e.g. fixed income, commodities, alternatives) and instruments within them.\n"
                    "  3) A risk profile questionnaire (10 questions) that produces a risk score and an internal\n"
                    "     risk aversion parameter called gamma.\n"
                    "  4) Constraints: maximum weight per asset, sector constraints, ESG constraints, and asset-class\n"
                    "     constraints at the total portfolio level.\n"
                    "  5) Optimization & backtest: a Markowitz mean–variance long-only optimization with constraints,\n"
                    "     followed by a backtest showing cumulative returns, portfolio wealth, drawdowns, and summary statistics.\n"
                    "- The app also shows today's optimal portfolio with:\n"
                    "  - Top holdings\n"
                    "  - Allocation by asset class\n"
                    "  - Sector breakdown within equity\n"
                    "  - ESG breakdown within equity\n\n"
                    "How you should behave:\n"
                    "- When clients ask about functionality, clearly explain which step of the process it relates to and\n"
                    "  describe what the app does in that step (without assuming you see their exact numbers).\n"
                    "- When clients ask about charts or metrics, explain conceptually what they represent (e.g. cumulative return,\n"
                    "  max drawdown, annualised volatility, wealth evolution).\n"
                    "- When clients ask about constraints or filters, explain how they influence diversification, risk concentration,\n"
                    "  and the optimizer's feasible set.\n"
                    "- When clients ask about financial markets, provide neutral, factual, and high-level explanations only.\n\n"
                    "Compliance and limitations:\n"
                    "- Do NOT provide personalized investment advice or recommendations.\n"
                    "- Do NOT tell clients what they should buy, sell, or hold.\n"
                    "- Do NOT give specific portfolio allocations, target returns, or forecasts for individual securities.\n"
                    "- You may explain trade-offs (e.g. higher risk vs higher potential return) in general terms.\n"
                    "- Keep a professional, calm, and client-oriented tone, as a relationship manager in a wealth management\n"
                    "  or asset management firm would, but always focus on education and explanation rather than advice."
                ),
            }
        ]

    # Show previous messages (except system)
    for msg in st.session_state.ai_messages:
        if msg["role"] == "system":
            continue
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask a question")
    if user_input:
        # 1) Add user message to history
        st.session_state.ai_messages.append(
            {"role": "user", "content": user_input}
        )

        # 2) Display user bubble
        with st.chat_message("user"):
            st.markdown(user_input)

        # 3) Call LLM
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.ai_messages,
                )

                reply = response.choices[0].message.content
                st.markdown(reply)

        # 4) Save assistant reply in history
        st.session_state.ai_messages.append(
            {"role": "assistant", "content": reply}
        )


if __name__ == "__main__":
    main()
