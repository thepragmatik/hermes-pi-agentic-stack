import json, subprocess, sys, pathlib
REPO = pathlib.Path(__file__).resolve().parents[1]
SCHEMA = REPO / "protocols/uplift-state.schema.json"
VALID = REPO / "protocols/examples/uplift-state.example.json"
def run(state_path):
    return subprocess.run([sys.executable, str(REPO / "tools/validate_state.py"),
                           str(state_path), str(SCHEMA)], capture_output=True, text=True)
def test_example_passes(tmp_path):
    assert run(VALID).stdout.strip() == "STATE_OK"
def test_mutated_state_fails(tmp_path):
    state = json.load(open(VALID)); state["version"] = "9.9"
    p = tmp_path / "bad.json"; p.write_text(json.dumps(state))
    r = run(p); assert r.returncode != 0
