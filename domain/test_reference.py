from datetime import datetime

class TestReference:
    def __init__(
        self,
        result: str,
        parameters: dict[str, str] | None = None,
    ):
        self.result: str = result
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

    def get_param(self, key: str) -> str | None:
        """Retrieve a parameter value."""
        return self.parameters.get(key)

    def set_result(self, result: str) -> None:
        """Update the result value and timestamp."""
        self.result = result
        self._touch()

    def as_dict(self) -> dict[str, str]:
        """Export all parameters plus the result in a flat dict."""
        return {"result": self.result, **self.parameters}

    def __repr__(self) -> str:
        return (
            f"TestReference(\n"
            f"\tresult={self.result!r},\n"
            f"\tparameters={self.parameters!r},\n"
            f"\tcreated_at={self.created_at.isoformat()},\n"
            f"\tupdated_at={self.updated_at.isoformat()}\n"
            f")"
        )
