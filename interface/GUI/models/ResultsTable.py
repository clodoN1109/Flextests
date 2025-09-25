from dataclasses import dataclass
from typing import Any

@dataclass
class ResultRow:
    efficacy: str | None
    efficiency: str | None
    duration: float | None
    min_memory: float | None
    max_memory: float | None
    mean_memory: float | None
    result: str | None
    parameters: dict[str, Any]

    def __getitem__(self, key: str):
        # allows access like row["efficacy"] or row["alpha"]
        if key in {"efficacy", "efficiency", "duration", "min_memory", "max_memory", "mean_memory", "result"}:
            return getattr(self, key)
        return self.parameters.get(key, None)


class ResultsTable:
    def __init__(self, headers: list[str], rows: list[ResultRow]):
        self.headers = headers
        self.rows = rows

    def __repr__(self):
        # Pretty tabular representation
        header_line = " | ".join(self.headers)
        rows_str = "\n".join(
            " | ".join(str(row[h]) if row[h] is not None else "-" for h in self.headers)
            for row in self.rows
        )
        return f"ResultsTable:\n{header_line}\n{'-' * len(header_line)}\n{rows_str}"

    @staticmethod
    def get_results_table(completed_test: "Test") -> "ResultsTable":
        # Collect all possible parameter keys
        all_param_keys: set[str] = set()
        for result in completed_test.results:
            if result.simulation and result.simulation.parameters:
                all_param_keys.update(result.simulation.parameters.keys())

        base_headers = ["efficacy", "efficiency"]
        stats_headers = ["duration", "min_memory", "max_memory", "mean_memory", "result"]
        headers = base_headers + stats_headers + sorted(all_param_keys)

        rows: list[ResultRow] = []
        for result in completed_test.results:
            sim_result = result.simulation
            stats = sim_result.stats if sim_result else None

            row = ResultRow(
                efficacy=result.efficacy,
                efficiency=result.efficiency,
                duration=stats.duration if stats else None,
                min_memory=stats.min_memory if stats else None,
                max_memory=stats.max_memory if stats else None,
                mean_memory=stats.mean_memory if stats else None,
                result=sim_result.result if sim_result else None,
                parameters=sim_result.parameters if sim_result else {}
            )
            rows.append(row)

        return ResultsTable(headers, rows)
