"""Exit 0 if every path given parses as YAML, non-zero and a message otherwise.

Exists so workflow steps validating a file they just generated don't need
a `python3 -c "..."` one-liner -- fine on its own, but Tools/
check_workflow_safety.py's CHECK-2 gate (rightly) treats any later shell
lines in the same run: block as suspected un-terminated Python once it
sees that substring anywhere in the block, not just when the block is
actually multi-line.
"""

import sys

import yaml

for path in sys.argv[1:]:
    with open(path) as f:
        yaml.safe_load(f)
    print(f"{path}: OK")
