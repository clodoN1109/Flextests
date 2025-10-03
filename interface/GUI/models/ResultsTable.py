from typing import Any, List

from dataclasses import dataclass
from typing import Any

from domain.failed_result import FailedResult

class HighlightedTableCell:
    def __init__(self, row: int, header: str, bg_color: str = "#554455") -> None:
        self.row = row
        self.header = header
        self.bg_color = bg_color

    def __repr__(self) -> str:
        return f"HighlightedTableCell(row={self.row}, header={self.header!r}, bg_color={self.bg_color!r})"

@dataclass
class ResultRow:
    efficacy: str | None
    efficiency: str | None
    duration: float | None
    min_memory: float | None
    max_memory: float | None
    mean_memory: float | None
    results: dict[str, str] | None      # <-- now a dict
    parameters: dict[str, Any]

    def __getitem__(self, key: str):
        # allows access like row["efficacy"], row["alpha"], row["area"], etc.
        if key in {"efficacy", "efficiency", "duration", "min_memory", "max_memory", "mean_memory"}:
            return getattr(self, key)
        if self.results and key in self.results:
            return self.results[key]
        return self.parameters.get(key, None)


class ResultsTable:
    def __init__(self, headers: list[str], rows: list[ResultRow], highlighted_cells: List[HighlightedTableCell]) -> None:
        self.headers = headers
        self.rows = rows
        self.red_cells: List[HighlightedTableCell] = highlighted_cells

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
        # Collect all possible keys across results + parameters
        all_keys: set[str] = set()
        for result in completed_test.results:
            sim_result = result.simulation
            if sim_result:
                if sim_result.results:
                    all_keys.update(sim_result.results.keys())
                if sim_result.parameters:
                    all_keys.update(sim_result.parameters.keys())

        base_headers = ["efficacy", "efficiency"]
        stats_headers = ["duration", "min_memory", "max_memory", "mean_memory"]
        headers = base_headers + stats_headers + sorted(all_keys)

        rows: list[ResultRow] = []
        failed_cells: list[HighlightedTableCell] = []

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
                results=sim_result.results if sim_result else {},
                parameters=sim_result.parameters if sim_result else {}
            )
            rows.append(row)

            failed_results: List[FailedResult] = result.failed_results
            for failure in failed_results:
                if row[failure.key] is not None:
                    failed_cells.append(HighlightedTableCell(len(rows)-1, failure.key, "#ff0000") )


        results_table = ResultsTable(headers, rows, failed_cells)
        return results_table
