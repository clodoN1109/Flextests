import json
import random
import math

# parameters: x and y are random integers between 1 and 10
params = {
    "x": random.randint(1, 10),
    "y": random.randint(1, 10),
}

# correct deterministic operations
correct_area = params["x"] * params["y"]
correct_hypotenuse = math.sqrt(params["x"]**2 + params["y"]**2)

# randomly decide which results to corrupt
# 0 = all correct, 1 = wrong area, 2 = wrong hypotenuse, 3 = both wrong
error_mode = random.choice([0, 1, 2, 3])

# inject errors
if error_mode == 0:
    area = correct_area
    hypotenuse = correct_hypotenuse
elif error_mode == 1:
    area = correct_area + random.randint(1, 5)   # wrong area
    hypotenuse = correct_hypotenuse
elif error_mode == 2:
    area = correct_area
    hypotenuse = correct_hypotenuse + random.uniform(1, 5)  # wrong hypotenuse
else:  # 3 = both wrong
    area = correct_area + random.randint(1, 5)
    hypotenuse = correct_hypotenuse + random.uniform(1, 5)

# build the output in the expected format
output = {
    "results": {
        "area": str(area),
        "hypotenuse": str(round(hypotenuse, 2))  # rounded for readability
    },
    "parameters": {k: str(v) for k, v in params.items()}
}

print(json.dumps(output))

