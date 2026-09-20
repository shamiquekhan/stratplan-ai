"""Verify the persistence behavior exactly as a user would experience it on the
deployed Streamlit Cloud app: create a plan in session 1, then simulate a page
reload (brand-new session, same store) and confirm everything is intact.

Run:  python3 test_reload_verification.py
"""
import os
import tempfile

# Isolated store so we don't touch any real plans_store.json
_tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
_tmp.close()
os.unlink(_tmp.name)
os.environ["STRATPLAN_STORE_PATH"] = _tmp.name

from streamlit.testing.v1 import AppTest


def fresh_session():
    """A brand-new AppTest = what a freshly-loaded browser page gets."""
    at = AppTest.from_file("frontend/streamlit_app.py", default_timeout=60)
    at.run()
    assert len(at.exception) == 0, at.exception
    return at


print("=== STEP 1: user creates a plan (session 1) ===")
s1 = fresh_session()
s1.text_input[0].set_value("Reload Survivor Co")
s1.text_area[0].set_value("Testing persistence across page reloads")
s1.selectbox[2].set_value("MVP")
s1.selectbox[5].set_value("Seed")
s1.button[0].click()
s1.run()
assert len(s1.exception) == 0
body = "".join(b.value for b in s1.markdown)
assert "is ready" in body
n = len(s1.session_state.plans)
print(f"PASS  plan created in session 1 (n={n})")

print("=== STEP 2: user reloads the page (session 2, same server store) ===")
s2 = fresh_session()
assert len(s2.session_state.plans) == n, (
    f"RELOAD FAILED: session 2 sees {len(s2.session_state.plans)} plans, expected {n}"
)
assert s2.session_state.plans[0]["plan"]["name"] == "Reload Survivor Co"
print("PASS  plans survive the reload: session 2 hydrates from the store")

print("=== STEP 3: reloaded user lands correctly ===")
at_radio = s2.radio[0].value
print(f"  nav after reload: {at_radio}")
s2.radio[0].set_value("Dashboard")
s2.run()
assert len(s2.exception) == 0
dash_body = "".join(b.value for b in s2.markdown)
assert "Reload Survivor Co" in dash_body, "plan missing on Dashboard after reload"
print("PASS  Dashboard shows the plan after reload")

s2.radio[0].set_value("Plan Details")
s2.run()
assert len(s2.exception) == 0
pd_body = " ".join(b.value for b in s2.markdown).upper()
assert "RELOAD SURVIVOR CO" in pd_body, "Plan Details did not auto-open after reload"
assert "KEY METRICS" in pd_body
print("PASS  Plan Details auto-opens the saved plan with key metrics")

print("=== STEP 4: no duplicates from repeated reloads ===")
s3 = fresh_session()
s4 = fresh_session()  # reload again, and again
assert len(s3.session_state.plans) == n, "duplicate plans after another reload"
assert len(s4.session_state.plans) == n, "duplicate plans after yet another reload"
print(f"PASS  repeated reloads hydrate the same {n} plan(s), no duplication")

print("=== STEP 5: create another plan after reload — IDs stay unique ===")
s4.radio[0].set_value("Create Plan")
s4.run()
s4.text_input[0].set_value("Second Wind")
s4.selectbox[2].set_value("Growth")
s4.button[0].click()
s4.run()
assert len(s4.exception) == 0
ids = [p["id"] for p in s4.session_state.plans]
assert len(ids) == len(set(ids)) == 2, f"ID collision: {ids}"
import json
with open(os.environ["STRATPLAN_STORE_PATH"]) as f:
    store = json.load(f)
assert len(store) == 2 and len({p["id"] for p in store}) == 2
print(f"PASS  post-reload creation works; store holds unique IDs {sorted(ids)}")

try:
    os.unlink(os.environ["STRATPLAN_STORE_PATH"])
except OSError:
    pass

print()
print("RELOAD VERIFICATION: ALL CHECKS PASSED")
print("Plans survive page reloads on the deployed app code.")
