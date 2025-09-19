from domain.test_criteria import TestCriteria
from domain.test_reference import TestReference
from domain.test_result import TestResult
from domain.test_statistics import TestStats
from domain.simulation import Simulation, SimulationResult


class Test:
    def __init__(self, test_name: str, description: str = ""):
        self.name = test_name
        self.description = description
        self.simulation: Simulation | None = None
        self.criteria: TestCriteria | None = None
        self.references: list[TestReference] | None = None
        self.results: list[TestResult] = []

    def execute(self, times: int) -> "TestStats":
        """Run the simulation multiple times and evaluate results."""
        if not self.simulation:
            raise RuntimeError("No simulation assigned to this test")

        for _ in range(times):
            self.simulation.run()

        sim_results: list[SimulationResult] = self.simulation.results
        self.results = [
            self.evaluate(sim_result, self.criteria, self.references)
            for sim_result in sim_results
        ]
        return TestStats.from_results(self.results)

    def get_results(self) -> list["TestResult"]:
        """Return the list of test results."""
        if not self.results:
            raise RuntimeError("No results available. Did you run execute()?")
        return self.results

    def get_stats(self) -> "TestStats":
        """Return aggregated test statistics."""
        if not self.results:
            raise RuntimeError("No results available. Did you run execute()?")
        return TestStats.from_results(self.results)

    @staticmethod
    def evaluate(
        sim_result: "SimulationResult",
        criteria: "TestCriteria | None" = None,
        references: list["TestReference"] | None = None,
    ) -> "TestResult":
        """Evaluate a single simulation result against references and criteria."""
        result = TestResult()

        # --- efficacy → check result against references ---
        if references:
            # find a matching reference by parameters
            matching_ref = next(
                (ref for ref in references if ref.parameters == sim_result.parameters),
                None,
            )

            if matching_ref:
                if str(sim_result.result) == str(matching_ref.result):
                    result.efficacy = "passed"
                else:
                    result.efficacy = "failed"
            else:
                # reference exists, but no matching parameters
                result.efficacy = "failed"
        else:
            # no references → auto-pass
            result.efficacy = "passed"

        # --- efficiency → check duration & memory ---
        if criteria:
            stats = sim_result.stats
            conditions = [
                criteria.duration is None or stats.duration <= criteria.duration,
                criteria.max_memory is None or stats.max_memory <= criteria.max_memory,
                criteria.mean_memory is None or stats.mean_memory <= criteria.mean_memory,
            ]
            result.efficiency = "passed" if all(conditions) else "failed"
        else:
            result.efficiency = "passed"  # no criteria → auto-pass

        return result





