#!/usr/bin/env python3
"""Validate uplift-state.json against protocols/uplift-state.schema.json."""
import json, sys
try:
    import jsonschema
except ImportError:
    sys.exit("pip install jsonschema first")
schema = json.load(open(sys.argv[2]))
state = json.load(open(sys.argv[1]))
jsonschema.validate(state, schema)
print("STATE_OK")
