from datetime import datetime

class TestReference:
    def __init__(
        self,
        results: dict[str, str] | None = None,
        parameters: dict[str, str] | None = None,
    ):
        self.results: dict[str, str] = results
        self.parameters: dict[str, str] = parameters or {}

        # --- timestamps ---
        now = datetime.utcnow()
        self.created_at: datetime = now
        self.updated_at: datetime = now

    def _touch(self) -> None:
        """Update the timestamp whenever the object changes."""
        self.updated_at = datetime.utcnow()

    def add_param(self, key: str, value: str) -> None:
        """Add or update a parameter."""
        self.parameters[key] = value
        self._touch()

    def add_result(self, key: str, value: str) -> None:
        """Add or update a parameter."""
        self.results[key] = value
        self._touch()

    def get_param(self, key: str) -> str | None:
        """Retrieve a parameter value."""
        return self.parameters.get(key)

    def set_results(self, results: dict[str, str]) -> None:
        """Update the results value and timestamp."""
        self.results = results
        self._touch()

    def as_dict(self) -> dict[str, str]:
        return {**self.parameters, **self.results}

    def __repr__(self) -> str:
        return (
            f"TestReference(\n"
            f"\tresults={self.results!r},\n"
            f"\tparameters={self.parameters!r},\n"
            f"\tcreated_at={self.created_at.isoformat()},\n"
            f"\tupdated_at={self.updated_at.isoformat()}\n"
            f")"
        )
