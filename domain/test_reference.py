class TestReference:
    def __init__(
        self,
        result: str,
        parameters: dict[str, str] | None = None,
    ):

        self.result: str = result
        self.parameters: dict[str, str] = parameters or {}

    def add_param(self, key: str, value: str) -> None:
        """Add or update a parameter."""
        self.parameters[key] = value

    def get_param(self, key: str) -> str | None:
        """Retrieve a parameter value."""
        return self.parameters.get(key)

    def as_dict(self) -> dict[str, str]:
        """Export all parameters plus the result in a flat dict."""
        return {"result": self.result, **self.parameters}

    def __repr__(self) -> str:
        return (
            f"\nTestReference"
            f"\n\tresult={self.result!r}, "
            f"\n\tparameters={self.parameters!r})"
        )
