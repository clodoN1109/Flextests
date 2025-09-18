from domain.test_criteria import TestCriteria
from domain.test_references import TestReferences
from domain.test_result import TestResult
from domain.test_statistics import TestStats
from domain.simulation import Simulation, SimulationResult


class Test:
    def __init__(self, test_name: str, description: str = ""):
        self.name = test_name
        self.description = description
        self.simulation: Simulation | None = None
        self.criteria: TestCriteria | None = None
        self.references: TestReferences | None = None
        self.results: list[TestResult] = []

    def execute(self, times: int) -> "TestStats":
        """Run the simulation multiple times and evaluate results."""
        if not self.simulation:
            raise RuntimeError("No simulation assigned to this test")

        for _ in range(times):
            self.simulation.run()

        sim_results: list[SimulationResult] = self.simulation.results
        self.results = [self.evaluate(sim_result, self.criteria, self.references) for sim_result in sim_results]
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
            criteria: "TestCriteria | None",
            references: "TestReferences | None"
    ) -> "TestResult":
        """Evaluate a single simulation result against the criteria and references."""
        result = TestResult()

        # --- efficacy → check output against references ---
        if references and sim_result.output is not None:
            expected_value = references.get(sim_result.output.key)
            if expected_value is not None and str(sim_result.output.value) == str(expected_value):
                result.efficacy = "passed"
            else:
                result.efficacy = "failed"
        elif references and sim_result.output is None:
            # the references exist but no output → fail
            result.efficacy = "failed"
        else:
            result.efficacy = "passed"  # no references → auto-pass

        # --- efficiency → check duration & memory ---
        if criteria:
            stats = sim_result.stats
            efficient = True

            if criteria.duration is not None and stats.duration > criteria.duration:
                efficient = False
            if criteria.max_memory is not None and stats.max_memory > criteria.max_memory:
                efficient = False
            if criteria.mean_memory is not None and stats.mean_memory > criteria.mean_memory:
                efficient = False

            result.efficiency = "passed" if efficient else "failed"
        else:
            # no performance criteria → auto-pass efficiency
            result.efficiency = "passed"

        return result









