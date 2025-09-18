from typing import Literal

class TestResult:
    def __init__(self):
        self.efficacy: Literal["passed", "failed"] | None = None
        self.efficiency: Literal["passed", "failed"] | None = None