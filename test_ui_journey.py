"""Streamlit AppTest journey: form submit -> confirmation -> Dashboard -> Plan Details.

Run:  python3 test_ui_journey.py
"""
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("frontend/streamlit_app.py", default_timeout=60)
at.run()
assert len(at.exception) == 0, at.exception

at.text_input[0].set_value("FinPilot AI")
at.text_area[0].set_value("AI copilot for finance teams")
at.selectbox[2].set_value("Idea")
at.selectbox[3].set_value("Pre-revenue")
at.number_input[0].set_value(0)
at.selectbox[5].set_value("Bootstrapped")
at.button[0].click()
at.run()
assert len(at.exception) == 0, at.exception
body = "".join(b.value for b in at.markdown)
assert "is ready" in body and "YEAR-1 REVENUE" in body
print("PASS  submit OK; confirmation with headline metrics")
assert at.radio[0].value == "Create Plan"
print("PASS  navigation stable after submit")

at.radio[0].set_value("Dashboard")
at.run()
assert len(at.exception) == 0, at.exception
body2 = "".join(b.value for b in at.markdown)
assert "FinPilot AI" in body2 and "RUNWAY" in body2.upper()
print("PASS  Dashboard lists plan with runway card")

at.radio[0].set_value("Plan Details")
at.run()
assert len(at.exception) == 0, at.exception
joined = " ".join(b.value for b in at.markdown).upper() + " " + " ".join(b.value for b in (list(at.success) + list(at.warning) + list(at.info))).upper()
assert "FINPILOT AI" in joined and "KEY METRICS" in joined
assert "YEAR-1 REVENUE" in joined
print(f"  (alerts captured by harness: {len(at.success) + len(at.warning) + len(at.info)} — st.warning not supported in this AppTest version)")
assert "SWOT" in joined and "OKR" in joined and "TAM" in joined
print("PASS  Plan Details: overview + financials + market + strategy all render")

print("ALL UI JOURNEY CHECKS PASSED")
