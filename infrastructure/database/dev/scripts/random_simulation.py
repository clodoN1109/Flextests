import json
import random

params = {
    "x": str(random.randint(1, 10)),
    "y": str(random.randint(20, 30)),
    "z": str(random.randint(100, 200))
}

result = f"result_{random.randint(1,5)}"

output = {
    "result": result,
    "parameters": params
}

print(json.dumps(output))
