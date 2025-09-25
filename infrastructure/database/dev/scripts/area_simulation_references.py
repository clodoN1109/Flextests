import json

# Domain of the parameters
x_values = range(1, 11)  # 1 through 10
y_values = range(1, 11)

reference = []

for x in x_values:
    for y in y_values:
        result = x * y
        reference = {
            "result": str(result),  # keep result as string for consistency
            "parameters": {
                "x": str(x),
                "y": str(y)
            }
        }
        reference.append(reference)

# Output the entire reference set as JSON array
print(json.dumps(reference, indent=2))
