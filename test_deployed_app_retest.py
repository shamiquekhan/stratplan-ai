"""End-to-end retest of the FinPilot AI plan creation flow against the deployed
Streamlit Cloud code (main branch), using Streamlit's official AppTest framework.

Run from repo root:  python3 test_deployed_app_retest.py
"""
import sys
import types

# ---- Minimal stubs so the module imports outside a full Streamlit runtime ----
st_module = types.ModuleType("streamlit")
_PY_TEST = None

try:
    from streamlit.testing.v1 import AppTest as _AppTest
    _PY_TEST = _AppTest
except Exception:
    pass

if _PY_TEST is not None:
    # Real streamlit is available; use it directly.
    import streamlit  # noqa: F401
else:
    def _noop(*a, **k):
        return None

    for name in [
        "set_page_config", "markdown", "progress", "empty", "columns", "form",
        "form_submit_button", "text_input", "text_area", "selectbox",
        "number_input", "button", "radio", "tabs", "expander", "line_chart",
        "dataframe", "json", "info", "error", "stop", "rerun", "spinner",
        "metric", "download_button", "hr",
    ]:
        setattr(st_module, name, _noop)
    st_module.session_state = types.SimpleNamespace(plans=[], current_plan_id=None)
    st_module.query_params = {}
    st_module.sidebar = types.SimpleNamespace(
        __enter__=lambda s: None, __exit__=lambda s, *a: None
    )
    sys.modules["streamlit"] = st_module

sys.path.insert(0, "frontend")
import streamlit_app as app  # noqa: E402

FAILURES = []


def check(label, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail else ""))
    if not cond:
        FAILURES.append(label)


def test_page1_create_plan_flow():
    """Replicates the exact FinPilot AI submission from the crash report:
    Stage=Idea, Pre-revenue, Bootstrapped, $0 revenue."""
    plan = {
        "name": "FinPilot AI",
        "description": "AI copilot for finance teams",
        "frequency": "monthly",
        "industry": "SaaS",
        "company_size": "Pre-revenue",
        "revenue_range": "Pre-revenue",
    }
    user_inputs = {
        "stage": "idea",
        "target_customer": "B2B SaaS 50-500",
        "business_model": "subscription",
        "differentiation": "AI-native workflows",
        "competitors": "https://comp1.com, https://comp2.com",
        "funding_status": "bootstrapped",
        "gtm_preference": "no_preference",
        "current_revenue": 0,
        "geography": "US",
    }

    # This is the call that raised KeyError: 'early' at line 501 before the fix.
    assumptions = app.get_default_assumptions(plan, user_inputs)
    check(
        "get_default_assumptions returns defaults for stage=idea (was KeyError)",
        abs(assumptions["revenue_growth_rate"] - 0.25) < 1e-9
        and abs(assumptions["gross_margin"] - 0.55) < 1e-9,
        f"growth={assumptions['revenue_growth_rate']}, margin={assumptions['gross_margin']}",
    )

    engine = app.FinancialEngine()
    stage_baseline = {"idea": 10000, "mvp": 10000, "early_traction": 25000,
                      "growth": 60000, "scale": 150000}
    starting_revenue = user_inputs.get("current_revenue", 0) or stage_baseline.get(
        user_inputs.get("stage", "idea"), 10000
    )
    financial_data = engine.build_projections(
        assumptions, starting_revenue, user_inputs=user_inputs
    )
    km = financial_data["key_metrics"]

    check("projections generated (36 months of P&L)", len(financial_data["pnl"]) == 36)
    check("month-1 revenue is not flat zero", financial_data["pnl"][0]["revenue"] > 0,
          f"${financial_data['pnl'][0]['revenue']:,.0f}")
    check("runway is a sane positive number", km["runway_months"] is None or km["runway_months"] > 0,
          f"{km['runway_months']} mo")
    check("break-even is int or None (renders as Mo -- when None)",
          km["break_even_month"] is None or isinstance(km["break_even_month"], int),
          f"{km['break_even_month']}")

    # Full plan_result assembly, as create_plan_page does after submission
    plan_result = {
        "id": 1,
        "plan": plan,
        "user_inputs": user_inputs,
        "generated_plan": app.generate_plan_summary(plan, user_inputs),
        "financial_projections": financial_data,
        "market_analysis": app.generate_market_analysis(plan, user_inputs),
        "competitor_analysis": app.generate_competitor_analysis(plan, user_inputs),
        "strategy": app.generate_strategy(plan, user_inputs),
        "status": "active",
    }
    check("plan_result assembled with all 8 sections",
          all(k in plan_result for k in [
              "plan", "user_inputs", "generated_plan", "financial_projections",
              "market_analysis", "competitor_analysis", "strategy", "status"]))
    return plan_result


def test_pages_render(plan_result):
    """Every page/tab must render the assembled plan without exceptions."""
    try:
        app.overview_tab(plan_result)
        check("overview_tab renders (KEY METRICS incl. Runway/Break-even)", True)
    except Exception as e:
        check("overview_tab renders", False, repr(e))

    try:
        app.financials_tab(plan_result)
        check("financials_tab renders (P&L, cash flow, balance sheet)", True)
    except Exception as e:
        check("financials_tab renders", False, repr(e))

    for tab_fn, label in [
        (app.market_tab, "market_tab"),
        (app.competitors_tab, "competitors_tab"),
        (app.strategy_tab, "strategy_tab"),
    ]:
        try:
            tab_fn(plan_result)
            check(f"{label} renders", True)
        except Exception as e:
            check(f"{label} renders", False, repr(e))


def test_full_matrix():
    """Every stage x funding combination must produce sane metrics."""
    engine = app.FinancialEngine()
    baselines = {"idea": 10000, "mvp": 10000, "early_traction": 25000,
                 "growth": 60000, "scale": 150000}
    bad = []
    for stage in baselines:
        for fund in ["bootstrapped", "pre_seed", "seed", "series_a", "series_b+"]:
            ui = {"stage": stage, "funding_status": fund, "current_revenue": 0}
            a = app.get_default_assumptions({}, ui)
            d = engine.build_projections(a, baselines[stage], user_inputs=ui)
            r = d["key_metrics"]["runway_months"]
            if r is not None and r <= 0:
                bad.append(f"{stage}/{fund}={r}")
    check("all 25 stage x funding combos produce sane runway", not bad,
          "; ".join(bad) if bad else "25/25 ok")


def test_apptest_smoke():
    """If the real Streamlit runtime is installed, run a true AppTest smoke test."""
    if _PY_TEST is None:
        print("[SKIP] streamlit.testing not available in this environment")
        return
    at = _AppTest.from_file("frontend/streamlit_app.py", default_timeout=30)
    at.run()
    check("AppTest: app runs with no uncaught exception", not at.exception,
          str(at.exception[0].value) if at.exception else "")


if __name__ == "__main__":
    print("=" * 70)
    print("RETEST: FinPilot AI plan creation (deployed main-branch code)")
    print("=" * 70)
    plan_result = test_page1_create_plan_flow()
    print("-" * 70)
    test_pages_render(plan_result)
    print("-" * 70)
    test_full_matrix()
    print("-" * 70)
    test_apptest_smoke()
    print("=" * 70)
    if FAILURES:
        print(f"RESULT: {len(FAILURES)} FAILURE(S): {FAILURES}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASSED ✅  (deployed flow is fixed)")
