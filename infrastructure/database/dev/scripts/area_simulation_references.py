import json

# Domain of the parameters
x_values = range(1, 11)
y_values = range(1, 11)

reference_list = []

for x in x_values:
    for y in y_values:
        item = {
            "result": str(x * y),
            "parameters": {"x": str(x), "y": str(y)}
        }
        reference_list.append(item)

# Output as JSON array
print(json.dumps(reference_list, indent=2))

