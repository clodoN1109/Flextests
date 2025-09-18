class TestReferences:
    def __init__(self, references: dict[str, str] | None = None):
        # Ensure we always have a dict
        self._references: dict[str, str] = references or {}

    def add(self, key: str, value: str) -> None:
        """Add or update a reference entry."""
        if not key:
            raise ValueError("Reference key must be non-empty")
        self._references[key] = value

    def get(self, key: str) -> str | None:
        """Retrieve the expected reference value for a key."""
        return self._references.get(key)

    def as_dict(self) -> dict[str, str]:
        """Return a shallow copy of all references."""
        return dict(self._references)

    def __contains__(self, key: str) -> bool:
        return key in self._references

    def __repr__(self) -> str:
        return f"TestReferences({self._references})"