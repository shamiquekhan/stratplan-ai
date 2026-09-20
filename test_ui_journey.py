"""Streamlit AppTest journey: form submit -> confirmation -> Dashboard -> Plan Details,
plus JSON-store persistence (plans survive page reloads / new sessions).

Run:  python3 test_ui_journey.py
"""
import os
import sys
import tempfile
import json

# Route the app's JSON store to an isolated temp file so tests never touch
# the developer's real plans_store.json.
_tmp_store = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
_tmp_store.close()
os.unlink(_tmp_store.name)
os.environ["STRATPLAN_STORE_PATH"] = _tmp_store.name

from streamlit.testing.v1 import AppTest

def new_app():
    at = AppTest.from_file("frontend/streamlit_app.py", default_timeout=60)
    at.run()
    assert len(at.exception) == 0, at.exception
    return at

def fill_and_submit(at, name="FinPilot AI"):
    at.text_input[0].set_value(name)
    at.text_area[0].set_value("AI copilot for finance teams")
    at.selectbox[2].set_value("Idea")
    at.selectbox[3].set_value("Pre-revenue")
    at.number_input[0].set_value(0)
    at.selectbox[5].set_value("Bootstrapped")
    at.button[0].click()
    at.run()
    assert len(at.exception) == 0, at.exception

# --- Journey: create -> confirm -> dashboard -> details ------------------
at = new_app()
fill_and_submit(at)
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
joined = (
    " ".join(b.value for b in at.markdown).upper()
    + " "
    + " ".join(b.value for b in (list(at.success) + list(at.warning) + list(at.info))).upper()
)
assert "FINPILOT AI" in joined and "KEY METRICS" in joined
assert "YEAR-1 REVENUE" in joined
print(f"  (alerts captured by harness: {len(at.success) + len(at.warning) + len(at.info)})")
assert "SWOT" in joined and "OKR" in joined and "TAM" in joined
print("PASS  Plan Details: overview + financials + market + strategy all render")

# --- Persistence: plans survive a brand-new session (page reload) -------
assert os.path.exists(os.environ["STRATPLAN_STORE_PATH"]), "store file not created"
with open(os.environ["STRATPLAN_STORE_PATH"]) as f:
    stored = json.load(f)
assert len(stored) == 1 and stored[0]["plan"]["name"] == "FinPilot AI"
print("PASS  plan persisted to JSON store on disk")

at2 = new_app()  # fresh session = fresh browser hitting the deployed app
assert len(at2.session_state.plans) == 1, "plans should hydrate from store"
assert at2.session_state.plans[0]["plan"]["name"] == "FinPilot AI"
print("PASS  new session hydrates plans from store (survives reload)")

at2.radio[0].set_value("Dashboard")
at2.run()
assert len(at2.exception) == 0, at2.exception
assert "FinPilot AI" in "".join(b.value for b in at2.markdown)
print("PASS  reloaded session sees the plan on the Dashboard")

# Second plan from the new session: IDs must not collide
at2.radio[0].set_value("Create Plan")
at2.run()
fill_and_submit(at2, name="Second Plan")
assert at2.session_state.plans[-1]["id"] != at2.session_state.plans[0]["id"], "duplicate ID"
with open(os.environ["STRATPLAN_STORE_PATH"]) as f:
    stored = json.load(f)
assert len(stored) == 2 and len({p["id"] for p in stored}) == 2
print("PASS  cross-session ID handling: second plan saved with unique ID")

# --- Resilience: corrupt store must not crash the app -------------------
with open(os.environ["STRATPLAN_STORE_PATH"], "w") as f:
    f.write("{not valid json!!")
at3 = AppTest.from_file("frontend/streamlit_app.py", default_timeout=60)
at3.run()
assert len(at3.exception) == 0, at3.exception
assert at3.session_state.plans == []
print("PASS  corrupt store handled gracefully (backs up, starts fresh)")

try:
    os.unlink(os.environ["STRATPLAN_STORE_PATH"])
except OSError:
    pass
print("ALL JOURNEY + PERSISTENCE CHECKS PASSED")
