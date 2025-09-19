import json
import random

# parameters: x and y are random integers between 1 and 10
params = {
    "x": random.randint(1, 10),
    "y": random.randint(1, 10),
}

# deterministic operation: result = x * y (always the same for given x,y)
result = params["x"] * params["y"]

# build the output in the expected format
output = {
    "result": str(result),  # convert to string to match your program’s expectation
    "parameters": {k: str(v) for k, v in params.items()}
}

print(json.dumps(output))
