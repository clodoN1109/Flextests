class FailedResult:
    def __init__(self, key: str, value: str, expected_value) -> None:
        self.key = key
        self.value = value
        self.expected_value = expected_value

    def __repr__(self) -> str:
        return f"FailedResult(key={self.key!r}, value={self.value!r}, expected_value={self.expected_value!r})"

