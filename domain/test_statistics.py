from typing import List
from domain.test_result import TestResult


class TestStats:
    def __init__(self, effective: int = 0, efficient: int = 0, both: int = 0, total: int = 0):
        self.effective = effective
        self.efficient = efficient
        self.effective_and_efficient = both
        self.total = total

    @classmethod
    def from_results(cls, results: list["TestResult"]) -> "TestStats":
        total = len(results)
        effective = sum(1 for r in results if r.efficacy == "passed")
        efficient = sum(1 for r in results if r.efficiency == "passed")
        both = sum(
            1 for r in results
            if r.efficacy == "passed" and r.efficiency == "passed"
        )
        return cls(effective, efficient, both, total)

    def to_dict(self) -> dict[str, int]:
        return {
            "total": self.total,
            "effective": self.effective,
            "efficient": self.efficient,
            "effective_and_efficient": self.effective_and_efficient,
        }

