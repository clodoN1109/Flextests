from typing import Literal

from domain.simulation_result import SimulationResult


class TestResult:
    def __init__(self):
        self.efficacy: Literal["passed", "failed"] | None = None
        self.efficiency: Literal["passed", "failed"] | None = None
        self.simulation: SimulationResult | None = None

    def __repr__(self) -> str:
        return (
            f"TestResult(\n"
            f"\tefficacy={self.efficacy!r},\n"
            f"\tefficiency={self.efficiency!r},\n"
            f"\tsimulation={self.simulation.__repr__() if self.simulation else None}\n"
            f")"
        )