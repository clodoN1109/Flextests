from dataclasses import dataclass
from typing import Any

from dataclasses import dataclass
from typing import Any

@dataclass
class ReferenceRow:
    results: dict[str, str]          # now a dict, not a str
    parameters: dict[str, Any]

    def __getitem__(self, key: str):
        # Access values like row["area"], row["hypotenuse"], row["x"], etc.
        if key in self.results:      # check inside results dict
            return self.results[key]
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
            return ReferencesTable(["no test references"], [])

        # Collect all keys across results + parameters
        all_keys: set[str] = set()
        for ref in test.reference:
            if ref.results:
                all_keys.update(ref.results.keys())
            if ref.parameters:
                all_keys.update(ref.parameters.keys())

        headers = sorted(all_keys)

        rows: list[ReferenceRow] = []
        for ref in test.reference:
            row = ReferenceRow(
                results=ref.results or {},
                parameters=ref.parameters or {}
            )
            rows.append(row)

        return ReferencesTable(headers, rows)

