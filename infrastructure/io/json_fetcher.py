import json
import urllib.request
from typing import Any, Callable, TypeVar, List

T = TypeVar("T")


class JsonFetcher:
    def __init__(self, max_depth: int | None = None):
        """
        :param max_depth: Maximum nesting depth to parse. None means no limit.
        """
        self.max_depth = max_depth

    def fetch(self, source: str) -> Any:
        """Fetch JSON from a URL or local path and return a parsed object."""
        raw_text = self._load_source(source)
        data = json.loads(raw_text)
        return self._limit_depth(data, self.max_depth)

    def fetch_as(self, source: str, factory: Callable[[dict], T]) -> List[T]:
        """
        Fetch JSON and map it into a list of objects using a factory function.
        The factory must accept a dict and return an instance of T.

        Example:
            fetcher.fetch_as("refs.json", lambda d: TestReference(**d))
        """
        raw = self.fetch(source)
        if not isinstance(raw, list):
            raise ValueError("Expected JSON root to be a list for fetch_as()")
        return [factory(item) for item in raw]

    # ---------------- private helpers ----------------

    def _load_source(self, source: str) -> str:
        """Load text content from a URL or local file."""
        if self._is_url(source):
            with urllib.request.urlopen(source) as response:
                return response.read().decode("utf-8")
        else:
            with open(source, "r", encoding="utf-8") as f:
                return f.read()

    @staticmethod
    def _is_url(source: str) -> bool:
        return source.startswith("http://") or source.startswith("https://")

    def _limit_depth(self, data: Any, max_depth: int | None, current_depth: int = 0) -> Any:
        """Recursively trim data structure to max_depth if provided."""
        if max_depth is None:
            return data
        if current_depth >= max_depth:
            return None  # or truncate with `...`
        if isinstance(data, dict):
            return {k: self._limit_depth(v, max_depth, current_depth + 1) for k, v in data.items()}
        if isinstance(data, list):
            return [self._limit_depth(v, max_depth, current_depth + 1) for v in data]
        return data
