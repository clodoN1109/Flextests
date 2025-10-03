from domain.simulation_statistics import SimulationStats


class SimulationResult:
    def __init__(self, stats: SimulationStats, results: dict[str, str] | None = None, parameters: dict[str, str] | None = None):
        self.parameters: dict[str, str] = parameters or {}
        self.results = results
        self.stats = stats

    def add_param(self, key: str, value: str) -> None:
        """Add or update a parameter."""
        self.parameters[key] = value

    def add_result_entry(self, key: str, value: str) -> None:
        """Add or update a parameter."""
        self.results[key] = value

    def get_param(self, key: str) -> str | None:
        """Retrieve a parameter value."""
        return self.parameters.get(key)

    def as_dict(self) -> dict[str, object]:
        """Return a serializable dict representation of the results."""
        return {
            "results": self.results,
            "parameters": dict(self.parameters),
            "stats": self.stats.as_dict() if hasattr(self.stats, "as_dict") else repr(self.stats),
        }

    def __repr__(self) -> str:
        return (
            f"SimulationResult(\n\tresult={self.results!r},"
            f"\n\tstats={self.stats.__repr__()}"
            f"\n\tparameters={self.parameters.__repr__()}\n)"
        )