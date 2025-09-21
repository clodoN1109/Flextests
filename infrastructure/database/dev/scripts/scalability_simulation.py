import json
import random
import sys

# Parse args
args = sys.argv[1:]  # skip script name
iteration = 1  # default if not provided
# Look for --iteration <n> flag style
for i, arg in enumerate(args):
    if arg in ("--iteration", "-iteration"):
        try:
            iteration = int(args[i + 1])
        except (IndexError, ValueError):
            pass
        break
    elif arg.startswith("--iteration="):
        try:
            iteration = int(arg.split("=", 1)[1])
        except ValueError:
            pass

# Generate parameters dynamically
params = {}
for i in range(1, iteration + 2):
    params[f"x{i}"] = random.randint(1, 10)

# Deterministic operation: sum of all values
result = 0
for v in params.values():
    result += v

# Build the output
output = {
    "result": str(result),  # keep it as string if that's expected
    "parameters": {k: str(v) for k, v in params.items()}
}

print(json.dumps(output))
