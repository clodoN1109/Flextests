from dataclasses import dataclass
from typing import Any

@dataclass
class ReferenceRow:
    result: str
    parameters: dict[str, Any]

    def __getitem__(self, key: str):
        # Access fixed or parameter values like row["result"], row["alpha"], etc.
        if key == "result":
            return self.result
        return self.parameters.get(key, None)


class ReferencesTable:
    def __init__(self, headers: list[str], rows: list[ReferenceRow]):
        self.headers = headers
        self.rows = rows

    def __repr__(self):
        header_line = " | ".join(self.headers)
        rows_str = "\n".join(
            " | ".join(str(row[h]) if row[h] is not None else "-" for h in self.headers)
            for row in self.rows
        )
        return f"ReferencesTable:\n{header_line}\n{'-' * len(header_line)}\n{rows_str}"

    @staticmethod
    def get_references_table(test: "Test") -> "ReferencesTable":
        if not test.reference:
            return ReferencesTable(["result"], [])

        # Collect all parameter keys across references
        all_param_keys: set[str] = set()
        for ref in test.reference:
            if ref.parameters:
                all_param_keys.update(ref.parameters.keys())

        headers = ["result"] + sorted(all_param_keys)

        rows: list[ReferenceRow] = []
        for ref in test.reference:
            row = ReferenceRow(
                result=ref.result,
                parameters=ref.parameters or {}
            )
            rows.append(row)

        return ReferencesTable(headers, rows)
