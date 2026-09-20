import streamlit as st
import requests
import time
import pandas as pd
from typing import Dict

API_BASE = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="StratPlan",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --black: #000000;
    --white: #FFFFFF;
    --gray-50: #FAFAFA;
    --gray-100: #F5F5F5;
    --gray-200: #E5E5E5;
    --gray-300: #D4D4D4;
    --gray-400: #A3A3A3;
    --gray-500: #737373;
    --gray-600: #525252;
    --gray-700: #404040;
    --accent: #FF0000;
    --accent-hover: #CC0000;
}

* { font-family: 'Space Grotesk', -apple-system, sans-serif !important; }

.stApp {
    background: var(--white) !important;
}

section[data-testid="stSidebar"] {
    background: var(--black) !important;
    border-right: 1px solid var(--black) !important;
}

section[data-testid="stSidebar"] * {
    color: var(--white) !important;
}

section[data-testid="stSidebar"] .stRadio label {
    border: 1px solid #333 !important;
    border-radius: 0 !important;
    padding: 12px 16px !important;
    margin-bottom: 2px !important;
    font-size: 11px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: #222 !important;
}

section[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {
    background: transparent !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.04em !important;
    line-height: 0.92 !important;
    color: var(--black) !important;
    margin: 0 !important;
}

.stMarkdown h1 { font-size: 3.5rem !important; }
.stMarkdown h2 { font-size: 2rem !important; }
.stMarkdown h3 { font-size: 1.1rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; font-weight: 600 !important; }

.stMarkdown p, .stMarkdown li, .stMarkdown span, .stMarkdown div {
    color: var(--black) !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
}

.stMarkdown strong { font-weight: 600 !important; }

hr {
    border: none !important;
    border-top: 1px solid var(--black) !important;
    margin: 2rem 0 !important;
}

div[data-testid="stMetric"] {
    background: var(--white) !important;
    border: 1px solid var(--black) !important;
    border-radius: 0 !important;
    padding: 20px !important;
    margin: 0 !important;
}

div[data-testid="stMetric"] label {
    font-size: 9px !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    color: var(--gray-500) !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.03em !important;
    color: var(--black) !important;
}

.stButton > button {
    border-radius: 0 !important;
    border: 1px solid var(--black) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 14px 28px !important;
    transition: all 0.15s ease !important;
    background: var(--white) !important;
    color: var(--black) !important;
}

.stButton > button:hover {
    background: var(--black) !important;
    color: var(--white) !important;
}

.stButton > button[kind="primary"],
.stButton > button[data-baseweb="button"] {
    background: var(--accent) !important;
    color: var(--white) !important;
    border-color: var(--accent) !important;
}

.stButton > button[kind="primary"]:hover {
    background: var(--accent-hover) !important;
}

.stTextInput input, .stTextArea textarea {
    border-radius: 0 !important;
    border: 1px solid var(--black) !important;
    color: var(--black) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 12px 14px !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: none !important;
}

.stSelectbox div[data-baseweb="select"] {
    border-radius: 0 !important;
    border: 1px solid var(--black) !important;
}

.stSelectbox div[data-baseweb="select"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: none !important;
}

.stSelectbox div[data-baseweb="select"] span {
    color: var(--black) !important;
}

div[data-baseweb="select-dropdown"] {
    border: 1px solid var(--black) !important;
    border-radius: 0 !important;
}

div[data-baseweb="select-option"] {
    color: var(--black) !important;
    background: var(--white) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

div[data-baseweb="select-option"]:hover,
div[data-baseweb="select-option"]:focus {
    background: var(--gray-100) !important;
    color: var(--black) !important;
}

div[data-baseweb="select-option"][aria-selected="true"] {
    background: var(--black) !important;
    color: var(--white) !important;
}

ul[role="listbox"] li {
    color: var(--black) !important;
    background: var(--white) !important;
}

ul[role="listbox"] li:hover {
    background: var(--gray-100) !important;
}

div[data-baseweb="menu"] div {
    color: var(--black) !important;
}

section.main label, section.main [data-testid="stWidgetLabel"] {
    color: var(--black) !important;
    font-weight: 600 !important;
    font-size: 10px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    border-bottom: 1px solid var(--black) !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 0 !important;
    border: none !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 10px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    padding: 14px 20px !important;
    color: var(--gray-400) !important;
    background: transparent !important;
}

.stTabs [aria-selected="true"] {
    color: var(--black) !important;
    border-bottom: 2px solid var(--black) !important;
    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

.stDataFrame {
    border: 1px solid var(--black) !important;
    border-radius: 0 !important;
}

.stDataFrame th {
    background: var(--black) !important;
    color: var(--white) !important;
    font-size: 9px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

.stDataFrame td {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}

.stExpander {
    border: 1px solid var(--black) !important;
    border-radius: 0 !important;
}

.stDownloadButton button {
    border-radius: 0 !important;
    border: 1px solid var(--black) !important;
}

.stProgress > div > div {
    background: var(--accent) !important;
    border-radius: 0 !important;
}

.stProgress > div {
    border-radius: 0 !important;
    border: 1px solid var(--black) !important;
}

code, .stCode {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
}

.stAlert {
    border-radius: 0 !important;
    border: 1px solid var(--black) !important;
}

.swiss-section { margin-bottom: 3rem; }
.swiss-label {
    font-size: 9px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--gray-400);
    font-weight: 500;
    margin-bottom: 4px;
}
.swiss-heading {
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 0.92;
    color: var(--black);
}
.swiss-accent { color: var(--accent); }
.swiss-divider {
    border: none;
    border-top: 1px solid var(--black);
    margin: 2.5rem 0;
}
.swiss-card {
    border: 1px solid var(--black);
    padding: 24px;
    margin-bottom: 1px;
}
.swiss-card-header {
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--gray-500);
    margin-bottom: 12px;
    font-weight: 500;
}
.swiss-body-text {
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--gray-600);
    max-width: 640px;
}
.swiss-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)


def api_get(endpoint):
    try:
        resp = requests.get(f"{API_BASE}{endpoint}", timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def api_post(endpoint, data):
    try:
        resp = requests.post(f"{API_BASE}{endpoint}", json=data, timeout=900)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API Error: {e}")
        return None


def check_health():
    try:
        resp = requests.get(f"{API_BASE}/health", timeout=5)
        return resp.status_code == 200
    except:
        return False


def swiss_section(label, heading, accent=True):
    if accent:
        st.markdown(
            f"""<div class="swiss-section">
            <div class="swiss-label">{label}</div>
            <h2 style="font-size:2rem;font-weight:700;letter-spacing:-0.04em;line-height:0.92;">{heading}<span class="swiss-accent">.</span></h2>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div class="swiss-section">
            <div class="swiss-label">{label}</div>
            <h2 style="font-size:2rem;font-weight:700;letter-spacing:-0.04em;line-height:0.92;">{heading}</h2>
            </div>""",
            unsafe_allow_html=True,
        )


def swiss_metric_card(label, value):
    return f"""<div style="border:1px solid #000;padding:20px;min-height:100px;">
    <div style="font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#737373;font-weight:500;margin-bottom:8px;">{label}</div>
    <div style="font-size:1.8rem;font-weight:700;letter-spacing:-0.03em;">{value}</div>
    </div>"""


def main():
    with st.sidebar:
        st.markdown(
            """<div style="padding:8px 0 24px 0;">
            <div style="font-size:1.4rem;font-weight:700;letter-spacing:-0.04em;line-height:0.92;">STRATPLAN<span style="color:#FF0000;">.</span></div>
            <div style="font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#737373;margin-top:4px;">AI PLANNING SYSTEM</div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.markdown("<hr>", unsafe_allow_html=True)
        health_ok = check_health()
        if health_ok:
            st.markdown(
                """<div style="display:flex;align-items:center;gap:8px;">
                <div style="width:6px;height:6px;background:#000;border-radius:50%;"></div>
                <span style="font-size:10px;letter-spacing:0.15em;text-transform:uppercase;font-weight:500;">SYSTEM ONLINE</span>
                </div>""",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """<div style="display:flex;align-items:center;gap:8px;">
                <div style="width:6px;height:6px;background:#FF0000;border-radius:50%;"></div>
                <span style="font-size:10px;letter-spacing:0.15em;text-transform:uppercase;font-weight:500;color:#FF0000;">OFFLINE</span>
                </div>
                <div style="font-size:11px;color:#737373;margin-top:8px;">uvicorn app.main:app --port 8000</div>""",
                unsafe_allow_html=True,
            )
            st.stop()

        st.markdown("<hr>", unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            ["Create Plan", "Dashboard", "Plan Details"],
            label_visibility="collapsed",
        )

    if page == "Create Plan":
        create_plan_page()
    elif page == "Dashboard":
        dashboard_page()
    elif page == "Plan Details":
        plan_details_page()


def create_plan_page():
    swiss_section("01", "CREATE PLAN")
    st.markdown(
        """<p class="swiss-body-text">
        Six AI agents research, model, and write your plan. You get an investor-ready document
        with financial projections, market data, competitor intelligence, and execution tracking.
        </p>""",
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    with st.form("plan_form"):
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.markdown(
                '<div class="swiss-card-header">IDENTITY</div>',
                unsafe_allow_html=True,
            )
            name = st.text_input("Plan Name", placeholder="Q3 2024 Growth Plan")
            description = st.text_area("Description", placeholder="Brief description...", height=68)
            frequency = st.selectbox("Frequency", ["Monthly", "Quarterly", "Yearly"])
        with c2:
            st.markdown(
                '<div class="swiss-card-header">BUSINESS</div>',
                unsafe_allow_html=True,
            )
            industry = st.selectbox(
                "Industry",
                [
                    "SaaS", "FinTech", "HealthTech", "E-commerce", "Marketplace",
                    "EdTech", "PropTech", "Logistics", "Manufacturing",
                    "Professional Services", "Consumer App", "B2B Services", "Other",
                ],
            )
            stage = st.selectbox("Company Stage", ["Idea", "MVP", "Early Traction", "Growth", "Scale"])
            company_size = st.selectbox("Company Size", ["Pre-revenue", "$0-100k", "$100k-1M", "$1M-10M", "$10M+"])
        with c3:
            st.markdown(
                '<div class="swiss-card-header">CONTEXT</div>',
                unsafe_allow_html=True,
            )
            target_customer = st.text_input("Target Customer", placeholder="B2B SaaS 50-500")
            business_model = st.selectbox("Business Model", ["Subscription", "Marketplace", "E-commerce", "Freemium", "License", "Services", "Other"])
            current_revenue = st.number_input("Current Revenue ($)", min_value=0, value=0, step=1000)

        st.markdown("<hr>", unsafe_allow_html=True)

        c4, c5 = st.columns(2)
        with c4:
            st.markdown(
                '<div class="swiss-card-header">STRATEGY</div>',
                unsafe_allow_html=True,
            )
            differentiation = st.text_area("Key Differentiation", placeholder="What makes you unique?", height=68)
            competitors = st.text_area("Competitor URLs", placeholder="https://comp1.com, https://comp2.com", height=68)
        with c5:
            st.markdown(
                '<div class="swiss-card-header">GO-TO-MARKET</div>',
                unsafe_allow_html=True,
            )
            funding_status = st.selectbox("Funding Status", ["Bootstrapped", "Pre-Seed", "Seed", "Series A", "Series B+"])
            gtm_preference = st.selectbox("GTM Preference", ["No preference", "Content & SEO", "Paid Ads", "Outbound Sales", "Partnerships", "Product-Led Growth"])
            geography = st.text_input("Target Geography", value="US")

        st.markdown("<hr>", unsafe_allow_html=True)
        submitted = st.form_submit_button("GENERATE PLAN", type="primary", use_container_width=True)

        if submitted:
            if not name:
                st.error("Plan name is required")
                return

            plan_data = {
                "name": name,
                "description": description,
                "frequency": frequency.lower(),
                "industry": industry,
                "company_size": company_size,
                "revenue_range": company_size,
            }
            user_inputs = {
                "stage": stage.lower().replace(" ", "_"),
                "target_customer": target_customer,
                "business_model": business_model.lower(),
                "differentiation": differentiation,
                "competitors": competitors,
                "funding_status": funding_status.lower().replace(" ", "_"),
                "gtm_preference": gtm_preference.lower().replace(" & ", "_").replace(" ", "_"),
                "current_revenue": current_revenue,
                "geography": geography,
            }

            with st.spinner("Creating plan..."):
                result = api_post("/plans", plan_data)
                if not result:
                    return
                plan_id = result["id"]

            progress_bar = st.progress(0)
            status_text = st.empty()
            agents = [
                ("collect_data", "Collecting market data..."),
                ("plan_generator", "Generating executive summary..."),
                ("financial_agent", "Building financial model..."),
                ("market_research", "Researching TAM/SAM/SOM..."),
                ("competitor_agent", "Analyzing competitors..."),
                ("strategy_agent", "Creating strategy and OKRs..."),
                ("execution_agent", "Execution tracker..."),
                ("save_plan", "Saving..."),
            ]
            for i, (a, msg) in enumerate(agents):
                status_text.markdown(
                    f"""<div style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#737373;">
                    {msg}
                    </div>""",
                    unsafe_allow_html=True,
                )
                progress_bar.progress((i + 1) / len(agents))
                time.sleep(0.4)

            with st.spinner("Running AI agents (5-8 min on CPU)..."):
                result = api_post(f"/plans/{plan_id}/generate", {"plan_id": plan_id, "user_inputs": user_inputs})

            progress_bar.empty()
            status_text.empty()

            if result:
                st.markdown(
                    f"""<div style="border:1px solid #000;padding:24px;margin-top:16px;">
                    <div style="font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#737373;margin-bottom:8px;">PLAN GENERATED</div>
                    <div style="font-size:1.2rem;font-weight:700;letter-spacing:-0.03em;">Plan {plan_id} created successfully.</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.error("Generation failed. Check backend logs.")


def dashboard_page():
    swiss_section("02", "PLANS")
    st.markdown("<hr>", unsafe_allow_html=True)

    plans = api_get("/plans")
    if not plans:
        st.markdown(
            """<div style="text-align:center;padding:80px 0;">
            <div style="font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#A3A3A3;margin-bottom:12px;">EMPTY</div>
            <div style="font-size:1.1rem;font-weight:600;color:#000;">No plans yet. Create your first plan.</div>
            </div>""",
            unsafe_allow_html=True,
        )
        return

    for plan in plans:
        with st.container():
            c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 1])
            with c1:
                st.markdown(
                    f"""<div style="font-size:1.1rem;font-weight:700;letter-spacing:-0.02em;">{plan['name']}</div>
                    <div style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#737373;margin-top:4px;">
                    {plan['frequency'].title()}  /  {plan.get('industry', '--')}  /  {plan['status'].title()}
                    </div>""",
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    swiss_metric_card("Industry", plan.get("industry", "N/A")),
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    swiss_metric_card("Status", plan["status"].title()),
                    unsafe_allow_html=True,
                )
            with c4:
                if st.button("VIEW", key=f"view_{plan['id']}", use_container_width=True):
                    st.query_params["plan_id"] = str(plan["id"])
                    st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)


def export_plan(plan_id, fmt):
    try:
        resp = requests.post(
            f"{API_BASE}/plans/{plan_id}/export",
            json={"plan_id": plan_id, "format": fmt},
            timeout=60,
        )
        if resp.status_code == 200:
            st.download_button(
                f"Download {fmt.upper()}",
                resp.content,
                file_name=f"plan_{plan_id}.{fmt}",
                use_container_width=True,
            )
        else:
            st.error(f"Export failed: {resp.text[:300]}")
    except Exception as e:
        st.error(f"Export error: {e}")


def plan_details_page():
    plan_id = st.query_params.get("plan_id")
    if not plan_id:
        st.markdown(
            """<div style="text-align:center;padding:80px 0;">
            <div style="font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#A3A3A3;margin-bottom:12px;">NO PLAN SELECTED</div>
            <div style="font-size:1.1rem;font-weight:600;color:#000;">Select a plan from Dashboard.</div>
            </div>""",
            unsafe_allow_html=True,
        )
        return

    try:
        plan_id = int(plan_id)
    except:
        st.error("Invalid plan ID")
        return

    plan = api_get(f"/plans/{plan_id}")
    if not plan:
        st.error("Plan not found")
        return

    normalized_plan = normalize_plan_data(plan)

    swiss_section("03", normalized_plan["name"].upper())
    st.markdown(
        f"""<div style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#737373;margin-bottom:2rem;">
        {normalized_plan['frequency'].title()}  /  {normalized_plan.get('industry', '--')}  /  {normalized_plan['status'].title()}
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["OVERVIEW", "FINANCIALS", "MARKET", "COMPETITORS", "STRATEGY", "EXPORT"]
    )

    with tab1:
        overview_tab(normalized_plan)
    with tab2:
        financials_tab(normalized_plan)
    with tab3:
        market_tab(normalized_plan)
    with tab4:
        competitors_tab(normalized_plan)
    with tab5:
        strategy_tab(normalized_plan)
    with tab6:
        export_tab(plan_id)


def normalize_plan_data(plan: Dict) -> Dict:
    normalized = {
        "id": plan.get("plan", {}).get("id", plan.get("id", 0)),
        "name": plan.get("plan", {}).get("name", plan.get("name", "Untitled Plan")),
        "description": plan.get("plan", {}).get("description", plan.get("description", "")),
        "frequency": plan.get("plan", {}).get("frequency", plan.get("frequency", "quarterly")),
        "industry": plan.get("plan", {}).get("industry", plan.get("industry", "")),
        "company_size": plan.get("plan", {}).get("company_size", plan.get("company_size", "")),
        "revenue_range": plan.get("plan", {}).get("revenue_range", plan.get("revenue_range", "")),
        "status": plan.get("plan", {}).get("status", plan.get("status", "draft")),
        "executive_summary": plan.get("generated_plan", plan.get("executive_summary", "Not generated")),
        "financial_projections": [
            {
                "assumptions": plan.get("financial_projections", {}).get("assumptions", {}),
                "pnl": plan.get("financial_projections", {}).get("pnl", []),
                "cash_flow": plan.get("financial_projections", {}).get("cash_flow", []),
                "balance_sheet": plan.get("financial_projections", {}).get("balance_sheet", []),
                "key_metrics": plan.get("financial_projections", {}).get("key_metrics", {}),
                "sensitivity": plan.get("financial_projections", {}).get("sensitivity", {}),
            }
        ],
        "market_analysis": plan.get("market_analysis", {}),
        "competitor_analysis": plan.get("competitor_analysis", {}),
        "strategy": plan.get("strategy", {}),
    }
    return normalized


def overview_tab(plan):
    st.markdown(
        '<div class="swiss-card-header">EXECUTIVE SUMMARY</div>',
        unsafe_allow_html=True,
    )
    summary = plan.get("executive_summary", "Not generated")
    if summary:
        paragraphs = summary.split("\n\n")
        for p in paragraphs:
            if p.strip():
                st.markdown(
                    f"""<p class="swiss-body-text">{p.strip()}</p>""",
                    unsafe_allow_html=True,
                )

    fin = plan.get("financial_projections", [{}])[0] if plan.get("financial_projections") else {}
    assumptions = fin.get("assumptions", {})
    key_metrics = fin.get("key_metrics", {})

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        '<div class="swiss-card-header">KEY METRICS</div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            swiss_metric_card("Revenue Growth", f"{assumptions.get('revenue_growth_rate', 0) * 100:.0f}%"),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            swiss_metric_card("Gross Margin", f"{assumptions.get('gross_margin', 0) * 100:.0f}%"),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            swiss_metric_card("Runway", f"{key_metrics.get('runway_months', 0)} mo"),
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            swiss_metric_card("Break-even", f"Mo {key_metrics.get('break_even_month', '--')}"),
            unsafe_allow_html=True,
        )

    if plan.get("strategy", {}).get("okrs"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">TOP OBJECTIVES</div>',
            unsafe_allow_html=True,
        )
        for okr in plan["strategy"]["okrs"][:3]:
            st.markdown(
                f"""<div style="border:1px solid #000;padding:20px;margin-bottom:1px;">
                <div style="font-weight:700;font-size:0.95rem;margin-bottom:8px;">{okr['objective']}</div>
                <div style="font-size:0.85rem;color:#525252;">
                {"".join(f'<div style="margin-top:4px;">-- {kr["metric"]}: {kr["target"]} {kr.get("unit","")}</div>' for kr in okr.get("key_results", [])[:2])}
                </div>
                </div>""",
                unsafe_allow_html=True,
            )


def financials_tab(plan):
    fin = plan.get("financial_projections", [{}])[0] if plan.get("financial_projections") else {}
    pnl = fin.get("pnl", [])
    cashflow = fin.get("cash_flow", [])
    balance = fin.get("balance_sheet", [])
    assumptions = fin.get("assumptions", {})

    def safe_chart(df, x_col, y_cols):
        if df.empty or x_col not in df.columns:
            return False
        available_y = [c for c in y_cols if c in df.columns]
        if not available_y:
            return False
        try:
            st.line_chart(df.set_index(x_col)[available_y])
            return True
        except:
            return False

    if pnl:
        df = pd.DataFrame(pnl)
        st.markdown(
            '<div class="swiss-card-header">P&L PROJECTION</div>',
            unsafe_allow_html=True,
        )
        safe_chart(df, "period", ["revenue", "gross_profit", "ebitda", "net_income"])

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">CASH FLOW</div>',
            unsafe_allow_html=True,
        )
        df_cf = pd.DataFrame(cashflow)
        safe_chart(df_cf, "period", ["operating", "investing", "financing", "net_cash_flow"])

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">BALANCE SHEET</div>',
            unsafe_allow_html=True,
        )
        df_bs = pd.DataFrame(balance)
        safe_chart(df_bs, "period", ["total_assets", "total_liabilities", "equity"])

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">P&L TABLE</div>',
            unsafe_allow_html=True,
        )
        table_cols = ["period", "revenue", "cogs", "gross_profit", "operating_expenses", "ebitda", "net_income"]
        available_cols = [c for c in table_cols if c in df.columns]
        if available_cols:
            st.dataframe(df[available_cols], use_container_width=True)
    else:
        st.info("No financial projection data available")

    if assumptions:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">ASSUMPTIONS</div>',
            unsafe_allow_html=True,
        )
        st.json(assumptions)


def market_tab(plan):
    market = plan.get("market_analysis", {})
    if not market:
        st.info("No market data")
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(swiss_metric_card("TAM", f"${market.get('tam', 0):,.0f}"), unsafe_allow_html=True)
    with c2:
        st.markdown(swiss_metric_card("SAM", f"${market.get('sam', 0):,.0f}"), unsafe_allow_html=True)
    with c3:
        st.markdown(swiss_metric_card("SOM", f"${market.get('som', 0):,.0f}"), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(swiss_metric_card("Market Growth", f"{market.get('market_growth_rate', 0) * 100:.1f}%"), unsafe_allow_html=True)

    if market.get("key_trends"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">KEY TRENDS</div>',
            unsafe_allow_html=True,
        )
        for t in market["key_trends"]:
            st.markdown(
                f"""<div style="padding:12px 0;border-bottom:1px solid #E5E5E5;font-size:0.9rem;">
                -- {t}
                </div>""",
                unsafe_allow_html=True,
            )

    if market.get("target_segments"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">SEGMENTS</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(pd.DataFrame(market["target_segments"]), use_container_width=True)

    if market.get("industry_benchmarks"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">BENCHMARKS</div>',
            unsafe_allow_html=True,
        )
        st.json(market["industry_benchmarks"])


def competitors_tab(plan):
    comp = plan.get("competitor_analysis", {})
    competitors = comp.get("competitors", [])
    matrix = comp.get("competitive_matrix", {})

    if not competitors:
        st.info("No competitor data")
        return

    st.markdown(
        '<div class="swiss-card-header">COMPETITOR PROFILES</div>',
        unsafe_allow_html=True,
    )

    for c in competitors:
        with st.expander(c["name"]):
            a, b = st.columns(2)
            with a:
                st.markdown(f"**Website:** {c.get('website', '--')}")
                st.markdown(f"**Pricing:** {c.get('pricing_model', '--')}")
                st.markdown(f"**Stage:** {c.get('funding_stage', '--')}")
            with b:
                st.markdown("**Key Features**")
                for f in c.get("key_features", [])[:5]:
                    st.markdown(f"-- {f}")

    if matrix.get("criteria") and matrix.get("scores"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">COMPETITIVE MATRIX</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(
            pd.DataFrame(matrix["scores"], index=matrix["criteria"]).T,
            use_container_width=True,
        )


def strategy_tab(plan):
    strat = plan.get("strategy", {})
    if not strat:
        st.info("No strategy data")
        return

    swot = strat.get("swot", {})
    if swot:
        st.markdown(
            '<div class="swiss-card-header">SWOT ANALYSIS</div>',
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Strengths**")
            for s in swot.get("strengths", []):
                st.markdown(f"-- {s}")
            st.markdown("**Weaknesses**")
            for w in swot.get("weaknesses", []):
                st.markdown(f"-- {w}")
        with c2:
            st.markdown("**Opportunities**")
            for o in swot.get("opportunities", []):
                st.markdown(f"-- {o}")
            st.markdown("**Threats**")
            for t in swot.get("threats", []):
                st.markdown(f"-- {t}")

    gtm = strat.get("gtm_strategy", {})
    if gtm:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">GO-TO-MARKET</div>',
            unsafe_allow_html=True,
        )
        if gtm.get("value_proposition"):
            st.markdown(f"**Value Proposition:** {gtm['value_proposition']}")
        if gtm.get("channels"):
            for ch in gtm["channels"]:
                st.markdown(
                    f"-- {ch['channel']}  (P{ch['priority']}, {ch.get('budget_allocation', 0) * 100:.0f}%)"
                )

    if strat.get("okrs"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(
            '<div class="swiss-card-header">OKRs</div>',
            unsafe_allow_html=True,
        )
        for okr in strat["okrs"]:
            st.markdown(f"**{okr['objective']}**")
            for kr in okr.get("key_results", []):
                st.markdown(f"-- {kr['metric']}: {kr['target']} {kr.get('unit', '')}")


def export_tab(plan_id):
    st.markdown(
        '<div class="swiss-card-header">EXPORT</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """<p class="swiss-body-text" style="margin-bottom:24px;">
        Download your plan in a professional format. PDF for presentations,
        DOCX for editing, XLSX for financial model manipulation.
        </p>""",
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            """<div style="border:1px solid #000;padding:20px;text-align:center;">
            <div style="font-size:2rem;font-weight:700;letter-spacing:-0.03em;">PDF</div>
            <div style="font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#737373;margin-top:4px;">PORTABLE DOCUMENT</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Download PDF", key="pdf_dl", use_container_width=True, type="primary"):
            export_plan(plan_id, "pdf")
    with c2:
        st.markdown(
            """<div style="border:1px solid #000;padding:20px;text-align:center;">
            <div style="font-size:2rem;font-weight:700;letter-spacing:-0.03em;">DOCX</div>
            <div style="font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#737373;margin-top:4px;">WORD DOCUMENT</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Download DOCX", key="docx_dl", use_container_width=True):
            export_plan(plan_id, "docx")
    with c3:
        st.markdown(
            """<div style="border:1px solid #000;padding:20px;text-align:center;">
            <div style="font-size:2rem;font-weight:700;letter-spacing:-0.03em;">XLSX</div>
            <div style="font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#737373;margin-top:4px;">EXCEL WORKBOOK</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Download XLSX", key="xlsx_dl", use_container_width=True):
            export_plan(plan_id, "xlsx")


if __name__ == "__main__":
    main()
