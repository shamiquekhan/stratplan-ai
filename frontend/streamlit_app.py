import streamlit as st
import time
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List

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

.stApp { background: var(--white) !important; }

section[data-testid="stSidebar"] {
    background: var(--black) !important;
    border-right: 1px solid var(--black) !important;
}

section[data-testid="stSidebar"] header {
    background: var(--black) !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarHeader"],
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] > div:first-child {
    background: var(--black) !important;
}

section[data-testid="stSidebar"] button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid #333 !important;
    color: var(--white) !important;
}

section[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: #222 !important;
}

section[data-testid="stSidebar"] * { color: var(--white) !important; }

[data-testid="stSidebarCollapseButton"] {
    display: none !important;
}

[data-testid="stSidebarCollapseButton"] svg {
    display: none !important;
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

section[data-testid="stSidebar"] .stRadio label:hover { background: #222 !important; }
section[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] { background: transparent !important; }

section[data-testid="stSidebar"] [data-baseweb="icon"] {
    color: var(--white) !important;
}

section[data-testid="stSidebar"] [data-baseweb="icon"] svg {
    fill: var(--white) !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.04em !important;
    line-height: 0.92 !important;
    color: var(--black) !important;
    margin: 0 !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4,
section[data-testid="stSidebar"] h5,
section[data-testid="stSidebar"] h6,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
    color: var(--white) !important;
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

hr { border: none !important; border-top: 1px solid var(--black) !important; margin: 2rem 0 !important; }

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

.stButton > button:hover { background: var(--black) !important; color: var(--white) !important; }

.stButton > button[kind="primary"],
.stButton > button[data-baseweb="button"] {
    background: var(--accent) !important;
    color: var(--white) !important;
    border-color: var(--accent) !important;
}

.stButton > button[kind="primary"]:hover { background: var(--accent-hover) !important; }

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

.stSelectbox div[data-baseweb="select"] span { color: var(--black) !important; }

div[data-baseweb="select-dropdown"] { border: 1px solid var(--black) !important; border-radius: 0 !important; }

div[data-baseweb="select-option"] {
    color: var(--black) !important;
    background: var(--white) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

div[data-baseweb="select-option"]:hover,
div[data-baseweb="select-option"]:focus { background: var(--gray-100) !important; color: var(--black) !important; }

div[data-baseweb="select-option"][aria-selected="true"] { background: var(--black) !important; color: var(--white) !important; }

ul[role="listbox"] li { color: var(--black) !important; background: var(--white) !important; }
ul[role="listbox"] li:hover { background: var(--gray-100) !important; }
div[data-baseweb="menu"] div { color: var(--black) !important; }

section.main label, section.main [data-testid="stWidgetLabel"],
div[data-testid="stWidgetLabel"] label,
section.main [data-baseweb="form"] label,
section.main form label,
section.main div[data-baseweb="input"] label,
section.main div[data-baseweb="select"] label,
section.main div[data-baseweb="textarea"] label,
section.main [data-testid="stTextInput"] label,
section.main [data-testid="stTextArea"] label,
section.main [data-testid="stSelectbox"] label,
section.main [data-testid="stNumberInput"] label {
    color: var(--black) !important;
    font-weight: 600 !important;
    font-size: 10px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

.stTabs [data-baseweb="tab-list"] { gap: 0 !important; border-bottom: 1px solid var(--black) !important; }

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

.stTabs [aria-selected="true"] { color: var(--black) !important; border-bottom: 2px solid var(--black) !important; font-weight: 700 !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

.stDataFrame { border: 1px solid var(--black) !important; border-radius: 0 !important; }

.stDataFrame th {
    background: var(--black) !important;
    color: var(--white) !important;
    font-size: 9px !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

.stDataFrame td { font-family: 'JetBrains Mono', monospace !important; font-size: 12px !important; }
.stExpander { border: 1px solid var(--black) !important; border-radius: 0 !important; }
.stDownloadButton button { border-radius: 0 !important; border: 1px solid var(--black) !important; }

.stProgress > div > div { background: var(--accent) !important; border-radius: 0 !important; }
.stProgress > div { border-radius: 0 !important; border: 1px solid var(--black) !important; }

code, .stCode { font-family: 'JetBrains Mono', monospace !important; font-size: 12px !important; }
.stAlert { border-radius: 0 !important; border: 1px solid var(--black) !important; }

.swiss-section { margin-bottom: 3rem; }
.swiss-label { font-size: 9px; letter-spacing: 0.25em; text-transform: uppercase; color: var(--gray-400); font-weight: 500; margin-bottom: 4px; }
.swiss-accent { color: var(--accent); }
.swiss-body-text { font-size: 0.9rem; line-height: 1.7; color: var(--gray-600); max-width: 640px; }
</style>
""", unsafe_allow_html=True)


# --- FINANCIAL ENGINE (embedded) ---

class FinancialEngine:
    def build_projections(self, assumptions: Dict[str, float], starting_revenue: float = 0, months: int = 36) -> Dict[str, Any]:
        revenue_growth = assumptions.get("revenue_growth_rate", 0.15)
        gross_margin = assumptions.get("gross_margin", 0.60)
        opex_ratio = assumptions.get("operating_expense_ratio", 0.50)
        tax_rate = assumptions.get("tax_rate", 0.21)
        interest_rate = assumptions.get("interest_rate", 0.05)
        depreciation_rate = assumptions.get("depreciation_rate", 0.10)
        wc_days = assumptions.get("working_capital_days", 30)
        capex_pct = assumptions.get("capex_percentage_of_revenue", 0.05)

        monthly_growth = (1 + revenue_growth) ** (1/12) - 1

        pnl, cashflow, balance_sheet = [], [], []
        cash_balance = starting_revenue * 0.5
        current_assets = cash_balance
        fixed_assets = starting_revenue * 2
        current_liabilities = 0
        longterm_liabilities = starting_revenue * 0.5
        equity = current_assets + fixed_assets - current_liabilities - longterm_liabilities
        retained_earnings = 0

        for month in range(1, months + 1):
            period_label = self._get_period_label(month)
            revenue = starting_revenue if month == 1 else pnl[-1]["revenue"] * (1 + monthly_growth)
            cogs = revenue * (1 - gross_margin)
            gross_profit = revenue - cogs
            operating_expenses = revenue * opex_ratio
            ebitda = gross_profit - operating_expenses
            depreciation = fixed_assets * depreciation_rate / 12
            interest = longterm_liabilities * interest_rate / 12
            ebt = ebitda - depreciation - interest
            tax = max(0, ebt * tax_rate)
            net_income = ebt - tax
            retained_earnings += net_income

            pnl.append({"period": period_label, "revenue": round(revenue, 2), "cogs": round(cogs, 2), "gross_profit": round(gross_profit, 2), "operating_expenses": round(operating_expenses, 2), "ebitda": round(ebitda, 2), "depreciation": round(depreciation, 2), "interest": round(interest, 2), "tax": round(tax, 2), "net_income": round(net_income, 2)})

            wc_change = (revenue * wc_days / 365) - (current_assets - cash_balance)
            capex = revenue * capex_pct / 12
            cf_operating = net_income + depreciation - wc_change
            cf_investing = -capex
            net_cash_flow = cf_operating + cf_investing
            cash_balance += net_cash_flow
            current_assets = cash_balance + (revenue * wc_days / 365)
            fixed_assets += capex - depreciation
            total_assets = current_assets + fixed_assets
            current_liabilities = revenue * 0.1
            equity = total_assets - current_liabilities - longterm_liabilities

            cashflow.append({"period": period_label, "operating": round(cf_operating, 2), "investing": round(cf_investing, 2), "financing": 0, "net_cash_flow": round(net_cash_flow, 2), "cash_balance": round(cash_balance, 2)})
            balance_sheet.append({"period": period_label, "current_assets": round(current_assets, 2), "fixed_assets": round(fixed_assets, 2), "total_assets": round(total_assets, 2), "current_liabilities": round(current_liabilities, 2), "longterm_liabilities": round(longterm_liabilities, 2), "total_liabilities": round(current_liabilities + longterm_liabilities, 2), "equity": round(equity, 2)})

        final_cash = cashflow[-1]["cash_balance"]
        monthly_burn = abs(min(cf["net_cash_flow"] for cf in cashflow))
        runway = final_cash / monthly_burn if monthly_burn > 0 else 0
        break_even_month = None
        for i, row in enumerate(pnl):
            if row["net_income"] > 0:
                break_even_month = i + 1
                break

        return {"assumptions": assumptions, "pnl": pnl, "cash_flow": cashflow, "balance_sheet": balance_sheet, "key_metrics": {"runway_months": round(runway, 1), "break_even_month": break_even_month, "ltv_cac_ratio": 3.0, "payback_period_months": 12, "final_cash": round(final_cash, 2), "total_revenue_3yr": round(sum(r["revenue"] for r in pnl), 2)}}

    def _get_period_label(self, month: int) -> str:
        if month % 12 == 0: return f"Year {month // 12}"
        elif month % 3 == 0: return f"Q{(month - 1) // 3 + 1} Y{(month - 1) // 12 + 1}"
        return f"Month {month}"


# --- AGENT FUNCTIONS (embedded, mock mode) ---

def generate_plan_summary(plan: Dict, user_inputs: Dict) -> str:
    return f"""# {plan.get('name', 'Business Plan')} - Executive Summary

## Company Overview
{plan.get('name', 'Our Company')} is a {plan.get('company_size', 'SME')} in the {plan.get('industry', 'technology')} industry, operating on a {plan.get('frequency', 'quarterly')} planning cycle.

## Mission & Vision
To deliver innovative {user_inputs.get('business_model', 'subscription')} solutions that empower {user_inputs.get('target_customer', 'B2B customers')} to achieve their goals through cutting-edge technology and exceptional service.

## Market Opportunity
Addressing a significant market gap in {plan.get('industry', 'the industry')}, we target {user_inputs.get('target_customer', 'SMBs')} with a differentiated approach focused on {user_inputs.get('differentiation', 'superior user experience and competitive pricing')}.

## Financial Highlights
- Current Revenue: ${user_inputs.get('current_revenue', 0):,.0f}
- Projected 3-Year Revenue Growth: 150-200%
- Target Gross Margin: 70%+
- Break-even: Month 18-24

## Key Strategies
1. Product-Led Growth: Self-serve onboarding and viral features
2. Content & SEO: Thought leadership to drive organic acquisition
3. Strategic Partnerships: Integration with complementary platforms
4. Customer Success: Dedicated support for enterprise accounts

## Funding & Milestones
- Status: {user_inputs.get('funding_status', 'Bootstrapped')}
- Next Milestone: Product-Market Fit (Month 6)
- Series A Target: $100k ARR with 3x YoY growth"""


def generate_market_analysis(plan: Dict, user_inputs: Dict) -> Dict:
    industry = plan.get("industry", "SaaS")
    base_tam = {"SaaS": 5000000000, "FinTech": 3000000000, "HealthTech": 2000000000, "E-commerce": 8000000000}.get(industry, 1000000000)
    return {
        "tam": base_tam, "sam": base_tam // 10, "som": base_tam // 100, "market_growth_rate": 0.15,
        "key_trends": ["AI/ML integration", "Vertical specialization", "PLG motion", "Usage-based pricing"],
        "target_segments": [
            {"segment": "SMB (50-500 employees)", "size": base_tam // 50, "growth_rate": 0.18, "characteristics": ["Budget-conscious", "Need simplicity", "Fast decision cycles"]},
            {"segment": "Mid-market (500-2000)", "size": base_tam // 20, "growth_rate": 0.12, "characteristics": ["Integration needs", "Security requirements", "Longer sales cycles"]}
        ],
        "industry_benchmarks": {"avg_revenue_per_employee": 250000, "avg_gross_margin": 0.75, "avg_operating_margin": 0.20, "typical_cac": 800, "typical_ltv": 12000},
        "macro_indicators": {"gdp_growth": 0.025, "inflation_rate": 0.03, "interest_rate": 0.05, "unemployment_rate": 0.04, "consumer_confidence": 102},
        "market_drivers": ["Digital transformation", "Remote work adoption", "API economy growth"],
        "market_barriers": ["High switching costs", "Data privacy regulations", "Talent shortage"]
    }


def generate_competitor_analysis(plan: Dict, user_inputs: Dict) -> Dict:
    industry = plan.get("industry", "SaaS")
    return {
        "competitors": [
            {"name": "Competitor A", "website": "https://competitor-a.com", "description": f"Leading {industry} platform", "pricing_model": "subscription", "pricing_tiers": [{"name": "Starter", "price": 49}, {"name": "Pro", "price": 149}, {"name": "Enterprise", "price": 499}], "key_features": ["Advanced reporting", "Team collaboration", "Integrations", "Custom workflows", "SSO/SAML"], "tech_stack": ["React", "Node.js", "PostgreSQL"], "positioning": "Complete platform for scaling teams", "funding_stage": "series_c", "employee_count": 450, "estimated_revenue": 85000000},
            {"name": "Competitor B", "website": "https://competitor-b.com", "description": f"Modern {industry} tool", "pricing_model": "freemium", "pricing_tiers": [{"name": "Free", "price": 0}, {"name": "Pro", "price": 29}], "key_features": ["Real-time collaboration", "Mobile app", "Automation", "Templates"], "tech_stack": ["Vue.js", "Go", "Redis"], "positioning": "Fast, simple, affordable", "funding_stage": "series_a", "employee_count": 80, "estimated_revenue": 8000000},
            {"name": "Competitor C", "website": "https://competitor-c.com", "description": f"Specialized {industry} solution", "pricing_model": "per_use", "pricing_tiers": [{"name": "Pay-per-use", "price": 0.10}], "key_features": ["Industry workflows", "Compliance built-in", "White-label"], "tech_stack": ["Angular", "Java", "AWS"], "positioning": "Vertical expertise, compliance-first", "funding_stage": "bootstrapped", "employee_count": 120, "estimated_revenue": 25000000}
        ],
        "competitive_matrix": {"criteria": ["Price", "Features", "Ease of Use", "Support", "Integrations"], "scores": {"Our Company": [5, 4, 5, 4, 4], "Competitor A": [2, 5, 3, 4, 5], "Competitor B": [4, 3, 5, 3, 3], "Competitor C": [3, 4, 2, 5, 2]}},
        "positioning_map": {"x_axis": "Price", "y_axis": "Features", "positions": {"Our Company": [0.7, 0.75], "Competitor A": [0.9, 0.9], "Competitor B": [0.2, 0.4], "Competitor C": [0.5, 0.6]}},
        "competitive_advantages": ["Best price-to-value ratio", "Superior UX/onboarding", "Flexible pricing", "Modern tech stack"],
        "threats": ["Competitor A's market dominance", "Competitor B's free tier", "New AI-native entrants"]
    }


def generate_strategy(plan: Dict, user_inputs: Dict) -> Dict:
    industry = plan.get("industry", "SaaS")
    return {
        "swot": {
            "strengths": [f"Modern {industry} architecture with API-first design", "Superior user experience and fast onboarding", "Flexible pricing that scales with customer growth", "Strong founding team with domain expertise"],
            "weaknesses": ["Limited brand recognition in early market", "Small team constrains parallel development", "No enterprise sales motion yet"],
            "opportunities": ["Growing demand for AI-enhanced automation", "Vertical expansion into adjacent markets", "Partnership channel with system integrators"],
            "threats": ["Well-funded competitors adding similar features", "Economic downturn reducing B2B budgets", "Platform risk from major cloud providers"]
        },
        "pestle": {
            "political": ["Increased government scrutiny on data sovereignty"],
            "economic": ["Rising interest rates increase cost of capital", "Enterprise software spend growing despite headwinds"],
            "social": ["Remote/hybrid work driving collaboration tool adoption"],
            "technological": ["LLM commoditization enabling AI features at low cost"],
            "legal": ["GDPR/CCPA compliance as baseline requirement"],
            "environmental": ["Carbon-neutral cloud hosting as differentiator"]
        },
        "gtm_strategy": {
            "value_proposition": f"The only {industry} platform combining enterprise-grade power with consumer-grade simplicity",
            "target_customer": "Growth-stage B2B companies (50-500 employees)",
            "pricing_strategy": "Three-tier value-based pricing with usage-based overages",
            "channels": [
                {"channel": "Content & SEO", "priority": "high", "budget_allocation": 0.35, "expected_cac": 300, "timeline": "Q1-Q4"},
                {"channel": "Product-Led Growth", "priority": "high", "budget_allocation": 0.25, "expected_cac": 150, "timeline": "Q1-Q4"},
                {"channel": "Strategic Partnerships", "priority": "high", "budget_allocation": 0.20, "expected_cac": 400, "timeline": "Q2-Q4"},
                {"channel": "Paid Search", "priority": "medium", "budget_allocation": 0.15, "expected_cac": 800, "timeline": "Q2-Q4"}
            ],
            "launch_sequence": [
                {"phase": "Foundation", "activities": ["Website redesign", "Content engine", "Free tier launch"], "timeline": "Month 1-2"},
                {"phase": "Growth", "activities": ["Partner program", "Paid campaigns", "Case studies"], "timeline": "Month 3-6"},
                {"phase": "Scale", "activities": ["Enterprise sales hire", "ABM campaigns", "International SEO"], "timeline": "Month 7-12"}
            ]
        },
        "okrs": [
            {"objective": "Achieve Product-Market Fit", "key_results": [{"metric": "NPS", "target": 50, "current": 0, "unit": "score"}, {"metric": "Monthly Churn", "target": 3, "current": 15, "unit": "%"}, {"metric": "Activation Rate (Day 7)", "target": 60, "current": 25, "unit": "%"}], "owner": "Product", "timeline": "Q1-Q2"},
            {"objective": "Build Scalable GTM Engine", "key_results": [{"metric": "CAC Payback", "target": 8, "current": 24, "unit": "months"}, {"metric": "Pipeline from Partnerships", "target": 30, "current": 0, "unit": "%"}, {"metric": "Organic Traffic", "target": 50000, "current": 2000, "unit": "visits/mo"}], "owner": "Marketing", "timeline": "Q2-Q4"},
            {"objective": "Prepare for Series A", "key_results": [{"metric": "ARR", "target": 500000, "current": 50000, "unit": "$"}, {"metric": "Net Revenue Retention", "target": 110, "current": 85, "unit": "%"}, {"metric": "Team Size", "target": 15, "current": 5, "unit": "count"}], "owner": "CEO", "timeline": "Q3-Q4"}
        ],
        "milestones": [
            {"milestone": "MVP Launch + Free Tier", "target_date": "2024-02-01", "dependencies": [], "success_criteria": "100 active free users"},
            {"milestone": "Product-Market Fit Signals", "target_date": "2024-05-01", "dependencies": ["MVP Launch"], "success_criteria": "NPS > 40, Churn < 5%"},
            {"milestone": "Partner Program Live", "target_date": "2024-07-01", "dependencies": ["PMF Signals"], "success_criteria": "5 certified partners"},
            {"milestone": "Series A Fundraise", "target_date": "2024-11-01", "dependencies": ["Partner Program"], "success_criteria": "$500k ARR, 3x YoY growth"}
        ],
        "risk_assessment": [
            {"risk": "Major competitor launches AI-native product", "likelihood": "high", "impact": "high", "mitigation": "Accelerate AI roadmap; build data moat"},
            {"risk": "Economic recession extends sales cycles", "likelihood": "medium", "impact": "high", "mitigation": "Emphasize ROI messaging; extend free tier"},
            {"risk": "Key talent poached by Big Tech", "likelihood": "medium", "impact": "medium", "mitigation": "Equity refresh; interesting challenges; remote-first"}
        ]
    }


def get_default_assumptions(plan: Dict, user_inputs: Dict) -> Dict[str, float]:
    stage = user_inputs.get("stage", "early")
    stage_defaults = {
        "idea": {"revenue_growth_rate": 0.25, "gross_margin": 0.55, "operating_expense_ratio": 0.70},
        "mvp": {"revenue_growth_rate": 0.35, "gross_margin": 0.60, "operating_expense_ratio": 0.60},
        "early_traction": {"revenue_growth_rate": 0.40, "gross_margin": 0.65, "operating_expense_ratio": 0.50},
        "growth": {"revenue_growth_rate": 0.30, "gross_margin": 0.70, "operating_expense_ratio": 0.40},
        "scale": {"revenue_growth_rate": 0.20, "gross_margin": 0.75, "operating_expense_ratio": 0.35},
    }
    s = stage_defaults.get(stage, stage_defaults["early"])
    return {"revenue_growth_rate": s["revenue_growth_rate"], "gross_margin": s["gross_margin"], "operating_expense_ratio": s["operating_expense_ratio"], "tax_rate": 0.21, "interest_rate": 0.05, "depreciation_rate": 0.10, "working_capital_days": 30, "capex_percentage_of_revenue": 0.05, "churn_rate": 0.05, "cac": 1000}


# --- UI HELPERS ---

def swiss_section(label, heading):
    st.markdown(f"""<div class="swiss-section"><div class="swiss-label">{label}</div><h2 style="font-size:2rem;font-weight:700;letter-spacing:-0.04em;line-height:0.92;">{heading}<span class="swiss-accent">.</span></h2></div>""", unsafe_allow_html=True)

def swiss_metric_card(label, value):
    return f"""<div style="border:1px solid #000;padding:20px;min-height:100px;"><div style="font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#737373;font-weight:500;margin-bottom:8px;">{label}</div><div style="font-size:1.8rem;font-weight:700;letter-spacing:-0.03em;">{value}</div></div>"""


# --- MAIN APP ---

def main():
    if "plans" not in st.session_state:
        st.session_state.plans = []
    if "current_plan_id" not in st.session_state:
        st.session_state.current_plan_id = None

    with st.sidebar:
        st.markdown("""<div style="padding:8px 0 24px 0;"><div style="font-size:1.4rem;font-weight:700;letter-spacing:-0.04em;line-height:0.92;color:#FFFFFF !important;">STRATPLAN<span style="color:#FF0000 !important;">.</span></div><div style="font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#FFFFFF !important;margin-top:4px;">AI PLANNING SYSTEM</div></div>""", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("""<div style="display:flex;align-items:center;gap:8px;"><div style="width:6px;height:6px;background:#00FF00;border-radius:50%;"></div><span style="font-size:10px;letter-spacing:0.15em;text-transform:uppercase;font-weight:500;color:#FFFFFF !important;">SYSTEM ONLINE</span></div>""", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        page = st.radio("Navigation", ["Create Plan", "Dashboard", "Plan Details"], label_visibility="collapsed")

    if page == "Create Plan":
        create_plan_page()
    elif page == "Dashboard":
        dashboard_page()
    elif page == "Plan Details":
        plan_details_page()


def create_plan_page():
    swiss_section("01", "CREATE PLAN")
    st.markdown("""<p class="swiss-body-text">Six AI agents research, model, and write your plan. You get an investor-ready document with financial projections, market data, competitor intelligence, and execution tracking.</p>""", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    with st.form("plan_form"):
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            st.markdown('<div class="swiss-label">IDENTITY</div>', unsafe_allow_html=True)
            name = st.text_input("Plan Name", placeholder="Q3 2024 Growth Plan")
            description = st.text_area("Description", placeholder="Brief description...", height=68)
            frequency = st.selectbox("Frequency", ["Monthly", "Quarterly", "Yearly"])
        with c2:
            st.markdown('<div class="swiss-label">BUSINESS</div>', unsafe_allow_html=True)
            industry = st.selectbox("Industry", ["SaaS", "FinTech", "HealthTech", "E-commerce", "Marketplace", "EdTech", "PropTech", "Logistics", "Manufacturing", "Professional Services", "Consumer App", "B2B Services", "Other"])
            stage = st.selectbox("Company Stage", ["Idea", "MVP", "Early Traction", "Growth", "Scale"])
            company_size = st.selectbox("Company Size", ["Pre-revenue", "$0-100k", "$100k-1M", "$1M-10M", "$10M+"])
        with c3:
            st.markdown('<div class="swiss-label">CONTEXT</div>', unsafe_allow_html=True)
            target_customer = st.text_input("Target Customer", placeholder="B2B SaaS 50-500")
            business_model = st.selectbox("Business Model", ["Subscription", "Marketplace", "E-commerce", "Freemium", "License", "Services", "Other"])
            current_revenue = st.number_input("Current Revenue ($)", min_value=0, value=0, step=1000)

        st.markdown("<hr>", unsafe_allow_html=True)
        c4, c5 = st.columns(2)
        with c4:
            st.markdown('<div class="swiss-label">STRATEGY</div>', unsafe_allow_html=True)
            differentiation = st.text_area("Key Differentiation", placeholder="What makes you unique?", height=68)
            competitors = st.text_area("Competitor URLs", placeholder="https://comp1.com, https://comp2.com", height=68)
        with c5:
            st.markdown('<div class="swiss-label">GO-TO-MARKET</div>', unsafe_allow_html=True)
            funding_status = st.selectbox("Funding Status", ["Bootstrapped", "Pre-Seed", "Seed", "Series A", "Series B+"])
            gtm_preference = st.selectbox("GTM Preference", ["No preference", "Content & SEO", "Paid Ads", "Outbound Sales", "Partnerships", "Product-Led Growth"])
            geography = st.text_input("Target Geography", value="US")

        st.markdown("<hr>", unsafe_allow_html=True)
        submitted = st.form_submit_button("GENERATE PLAN", type="primary", use_container_width=True)

        if submitted:
            if not name:
                st.error("Plan name is required")
                return

            plan_data = {"name": name, "description": description, "frequency": frequency.lower(), "industry": industry, "company_size": company_size, "revenue_range": company_size}
            user_inputs = {"stage": stage.lower().replace(" ", "_"), "target_customer": target_customer, "business_model": business_model.lower(), "differentiation": differentiation, "competitors": competitors, "funding_status": funding_status.lower().replace(" ", "_"), "gtm_preference": gtm_preference.lower().replace(" & ", "_").replace(" ", "_"), "current_revenue": current_revenue, "geography": geography}

            progress_bar = st.progress(0)
            status_text = st.empty()
            agents = [("plan_generator", "Generating executive summary..."), ("financial_agent", "Building financial model..."), ("market_research", "Researching TAM/SAM/SOM..."), ("competitor_agent", "Analyzing competitors..."), ("strategy_agent", "Creating strategy and OKRs..."), ("execution_agent", "Building execution tracker...")]
            for i, (a, msg) in enumerate(agents):
                status_text.markdown(f"""<div style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#737373;">{msg}</div>""", unsafe_allow_html=True)
                progress_bar.progress((i + 1) / len(agents))
                time.sleep(0.3)

            engine = FinancialEngine()
            assumptions = get_default_assumptions(plan_data, user_inputs)
            financial_data = engine.build_projections(assumptions, user_inputs.get("current_revenue", 0))

            plan_result = {
                "id": len(st.session_state.plans) + 1,
                "plan": plan_data,
                "user_inputs": user_inputs,
                "generated_plan": generate_plan_summary(plan_data, user_inputs),
                "financial_projections": financial_data,
                "market_analysis": generate_market_analysis(plan_data, user_inputs),
                "competitor_analysis": generate_competitor_analysis(plan_data, user_inputs),
                "strategy": generate_strategy(plan_data, user_inputs),
                "status": "active",
                "created_at": datetime.now().isoformat()
            }
            st.session_state.plans.append(plan_result)
            st.session_state.current_plan_id = plan_result["id"]

            progress_bar.empty()
            status_text.empty()
            st.markdown(f"""<div style="border:1px solid #000;padding:24px;margin-top:16px;"><div style="font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#737373;margin-bottom:8px;">PLAN GENERATED</div><div style="font-size:1.2rem;font-weight:700;letter-spacing:-0.03em;">Plan {plan_result['id']} created successfully.</div></div>""", unsafe_allow_html=True)


def dashboard_page():
    swiss_section("02", "PLANS")
    st.markdown("<hr>", unsafe_allow_html=True)
    plans = st.session_state.plans
    if not plans:
        st.markdown("""<div style="text-align:center;padding:80px 0;"><div style="font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#A3A3A3;margin-bottom:12px;">EMPTY</div><div style="font-size:1.1rem;font-weight:600;color:#000;">No plans yet. Create your first plan.</div></div>""", unsafe_allow_html=True)
        return

    for plan in plans:
        c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 1])
        with c1:
            st.markdown(f"""<div style="font-size:1.1rem;font-weight:700;letter-spacing:-0.02em;">{plan['plan']['name']}</div><div style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#737373;margin-top:4px;">{plan['plan']['frequency'].title()}  /  {plan['plan'].get('industry', '--')}  /  {plan['status'].title()}</div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(swiss_metric_card("Industry", plan['plan'].get("industry", "N/A")), unsafe_allow_html=True)
        with c3:
            st.markdown(swiss_metric_card("Status", plan["status"].title()), unsafe_allow_html=True)
        with c4:
            if st.button("VIEW", key=f"view_{plan['id']}", use_container_width=True):
                st.session_state.current_plan_id = plan["id"]
                st.rerun()
        st.markdown("<hr>", unsafe_allow_html=True)


def plan_details_page():
    plan_id = st.session_state.current_plan_id
    if not plan_id:
        st.markdown("""<div style="text-align:center;padding:80px 0;"><div style="font-size:9px;letter-spacing:0.25em;text-transform:uppercase;color:#A3A3A3;margin-bottom:12px;">NO PLAN SELECTED</div><div style="font-size:1.1rem;font-weight:600;color:#000;">Select a plan from Dashboard.</div></div>""", unsafe_allow_html=True)
        return

    plan = next((p for p in st.session_state.plans if p["id"] == plan_id), None)
    if not plan:
        st.error("Plan not found")
        return

    swiss_section("03", plan["plan"]["name"].upper())
    st.markdown(f"""<div style="font-size:11px;letter-spacing:0.1em;text-transform:uppercase;color:#737373;margin-bottom:2rem;">{plan['plan']['frequency'].title()}  /  {plan['plan'].get('industry', '--')}  /  {plan['status'].title()}</div>""", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["OVERVIEW", "FINANCIALS", "MARKET", "COMPETITORS", "STRATEGY"])
    with tab1: overview_tab(plan)
    with tab2: financials_tab(plan)
    with tab3: market_tab(plan)
    with tab4: competitors_tab(plan)
    with tab5: strategy_tab(plan)


def overview_tab(plan):
    st.markdown('<div class="swiss-label">EXECUTIVE SUMMARY</div>', unsafe_allow_html=True)
    summary = plan.get("generated_plan", "")
    for p in summary.split("\n\n"):
        if p.strip():
            st.markdown(f"""<p class="swiss-body-text">{p.strip()}</p>""", unsafe_allow_html=True)

    fin = plan.get("financial_projections", {})
    assumptions = fin.get("assumptions", {})
    key_metrics = fin.get("key_metrics", {})

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="swiss-label">KEY METRICS</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(swiss_metric_card("Revenue Growth", f"{assumptions.get('revenue_growth_rate', 0) * 100:.0f}%"), unsafe_allow_html=True)
    with c2: st.markdown(swiss_metric_card("Gross Margin", f"{assumptions.get('gross_margin', 0) * 100:.0f}%"), unsafe_allow_html=True)
    with c3: st.markdown(swiss_metric_card("Runway", f"{key_metrics.get('runway_months', 0)} mo"), unsafe_allow_html=True)
    with c4: st.markdown(swiss_metric_card("Break-even", f"Mo {key_metrics.get('break_even_month', '--')}"), unsafe_allow_html=True)

    if plan.get("strategy", {}).get("okrs"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">TOP OBJECTIVES</div>', unsafe_allow_html=True)
        for okr in plan["strategy"]["okrs"][:3]:
            st.markdown(f"""<div style="border:1px solid #000;padding:20px;margin-bottom:1px;"><div style="font-weight:700;font-size:0.95rem;margin-bottom:8px;">{okr['objective']}</div><div style="font-size:0.85rem;color:#525252;">{"".join(f'<div style="margin-top:4px;">-- {kr["metric"]}: {kr["target"]} {kr.get("unit","")}</div>' for kr in okr.get("key_results", [])[:2])}</div></div>""", unsafe_allow_html=True)


def financials_tab(plan):
    fin = plan.get("financial_projections", {})
    pnl = fin.get("pnl", [])
    cashflow = fin.get("cash_flow", [])
    balance = fin.get("balance_sheet", [])
    assumptions = fin.get("assumptions", {})

    def safe_chart(df, x_col, y_cols):
        if df.empty or x_col not in df.columns: return False
        available_y = [c for c in y_cols if c in df.columns]
        if not available_y: return False
        try: st.line_chart(df.set_index(x_col)[available_y]); return True
        except: return False

    if pnl:
        df = pd.DataFrame(pnl)
        st.markdown('<div class="swiss-label">P&L PROJECTION</div>', unsafe_allow_html=True)
        safe_chart(df, "period", ["revenue", "gross_profit", "ebitda", "net_income"])
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">CASH FLOW</div>', unsafe_allow_html=True)
        df_cf = pd.DataFrame(cashflow)
        safe_chart(df_cf, "period", ["operating", "investing", "net_cash_flow"])
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">BALANCE SHEET</div>', unsafe_allow_html=True)
        df_bs = pd.DataFrame(balance)
        safe_chart(df_bs, "period", ["total_assets", "total_liabilities", "equity"])
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">P&L TABLE</div>', unsafe_allow_html=True)
        table_cols = ["period", "revenue", "cogs", "gross_profit", "operating_expenses", "ebitda", "net_income"]
        available_cols = [c for c in table_cols if c in df.columns]
        if available_cols: st.dataframe(df[available_cols], use_container_width=True)
    else:
        st.info("No financial projection data available")

    if assumptions:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">ASSUMPTIONS</div>', unsafe_allow_html=True)
        st.json(assumptions)


def market_tab(plan):
    market = plan.get("market_analysis", {})
    if not market: st.info("No market data"); return
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(swiss_metric_card("TAM", f"${market.get('tam', 0):,.0f}"), unsafe_allow_html=True)
    with c2: st.markdown(swiss_metric_card("SAM", f"${market.get('sam', 0):,.0f}"), unsafe_allow_html=True)
    with c3: st.markdown(swiss_metric_card("SOM", f"${market.get('som', 0):,.0f}"), unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(swiss_metric_card("Market Growth", f"{market.get('market_growth_rate', 0) * 100:.1f}%"), unsafe_allow_html=True)
    if market.get("key_trends"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">KEY TRENDS</div>', unsafe_allow_html=True)
        for t in market["key_trends"]: st.markdown(f"""<div style="padding:12px 0;border-bottom:1px solid #E5E5E5;font-size:0.9rem;">-- {t}</div>""", unsafe_allow_html=True)
    if market.get("target_segments"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">SEGMENTS</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(market["target_segments"]), use_container_width=True)


def competitors_tab(plan):
    comp = plan.get("competitor_analysis", {})
    competitors = comp.get("competitors", [])
    matrix = comp.get("competitive_matrix", {})
    if not competitors: st.info("No competitor data"); return
    st.markdown('<div class="swiss-label">COMPETITOR PROFILES</div>', unsafe_allow_html=True)
    for c in competitors:
        with st.expander(c["name"]):
            a, b = st.columns(2)
            with a:
                st.markdown(f"**Website:** {c.get('website', '--')}")
                st.markdown(f"**Pricing:** {c.get('pricing_model', '--')}")
                st.markdown(f"**Stage:** {c.get('funding_stage', '--')}")
            with b:
                st.markdown("**Key Features**")
                for f in c.get("key_features", [])[:5]: st.markdown(f"-- {f}")
    if matrix.get("criteria") and matrix.get("scores"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">COMPETITIVE MATRIX</div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(matrix["scores"], index=matrix["criteria"]).T, use_container_width=True)


def strategy_tab(plan):
    strat = plan.get("strategy", {})
    if not strat: st.info("No strategy data"); return
    swot = strat.get("swot", {})
    if swot:
        st.markdown('<div class="swiss-label">SWOT ANALYSIS</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Strengths**")
            for s in swot.get("strengths", []): st.markdown(f"-- {s}")
            st.markdown("**Weaknesses**")
            for w in swot.get("weaknesses", []): st.markdown(f"-- {w}")
        with c2:
            st.markdown("**Opportunities**")
            for o in swot.get("opportunities", []): st.markdown(f"-- {o}")
            st.markdown("**Threats**")
            for t in swot.get("threats", []): st.markdown(f"-- {t}")
    gtm = strat.get("gtm_strategy", {})
    if gtm:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">GO-TO-MARKET</div>', unsafe_allow_html=True)
        if gtm.get("value_proposition"): st.markdown(f"**Value Proposition:** {gtm['value_proposition']}")
        if gtm.get("channels"):
            for ch in gtm["channels"]: st.markdown(f"-- {ch['channel']}  (P{ch['priority']}, {ch.get('budget_allocation', 0) * 100:.0f}%)")
    if strat.get("okrs"):
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="swiss-label">OKRs</div>', unsafe_allow_html=True)
        for okr in strat["okrs"]:
            st.markdown(f"**{okr['objective']}**")
            for kr in okr.get("key_results", []): st.markdown(f"-- {kr['metric']}: {kr['target']} {kr.get('unit', '')}")


if __name__ == "__main__":
    main()
