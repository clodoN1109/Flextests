from domain.test_criteria import TestCriteria
from domain.test_reference import TestReference
from domain.test_result import TestResult
from domain.test_statistics import TestStats
from domain.simulation import Simulation, SimulationResult


class Test:
    def __init__(self, test_name: str, description: str = "", simulation_script: str = "", reference_source: str = ""):
        self.name = test_name
        self.description = description
        self.simulation:Simulation = Simulation(test_name, simulation_script, description)
        self.criteria: TestCriteria | None = None
        self.reference_source: str | None = None
        self.reference: list[TestReference] | None = None
        self.results: list[TestResult] = []
        self.stats: TestStats | None = None
        self.final_result: str | None = None

    def execute(self, times: int):
        """Run the simulation multiple times and evaluate results."""
        if not self.simulation:
            raise RuntimeError("No simulation assigned to this test")

        for i in range(times):
            self.simulation.run(i)

        sim_results: list[SimulationResult] = self.simulation.results
        self.results = [
            self.evaluate(sim_result, self.criteria, self.reference)
            for sim_result in sim_results
        ]
        self.stats = TestStats.from_results(self.results)
        compliance_rate = self.stats.effective_and_efficient/self.stats.total
        if float(compliance_rate) < self.criteria.compliance_rate:
            self.final_result = "failed"
        else:
            self.final_result = "passed"

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

    def get_stats_variable_data(self, variable_name: str):
        data = [result.simulation.stats.get_value_by_name(variable_name) for result in self.results]

    @staticmethod
    def evaluate(
        sim_result: "SimulationResult",
        criteria: "TestCriteria | None" = None,
        reference: list["TestReference"] | None = None,
    ) -> "TestResult":
        """Evaluate a single simulation result against reference and criteria."""
        result = TestResult()

        # --- efficacy → check result against reference ---
        if reference:
            # find a matching reference by parameters
            matching_ref = next(
                (ref for ref in reference if ref.parameters == sim_result.parameters),
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
            # no reference → auto-pass
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

        result.simulation = sim_result
        return result

    def report(self) -> str:
        indent = "    "

        # Criteria formatting
        if self.criteria:
            criteria_lines = [
                f"{indent}- duration       : {self.criteria.duration}",
                f"{indent}- max_memory     : {self.criteria.max_memory}",
                f"{indent}- mean_memory    : {self.criteria.mean_memory}",
                f"{indent}- compliance_rate: {self.criteria.compliance_rate}",
            ]
            criteria_str = "\n".join(criteria_lines)
        else:
            criteria_str = f"{indent}(no criteria)"

        # Stats formatting
        if self.stats:
            stats_lines = [
                f"{indent}- effective             : {self.stats.effective}",
                f"{indent}- efficient             : {self.stats.efficient}",
                f"{indent}- effective & efficient : {self.stats.effective_and_efficient}",
                f"{indent}- total                 : {self.stats.total}",
                f"{indent}- compliance rate       : {self.stats.compliance_rate}",
            ]
            stats_str = "\n".join(stats_lines)
        else:
            stats_str = f"{indent}(no stats)"

        return (
            f"Test: {self.name}\n"
            f"Description:\n{indent}{self.description or '(none)'}\n"
            f"Criteria:\n{criteria_str}\n"
            f"Stats:\n{stats_str}\n"
            f"Final Result:\n{indent}{self.final_result or '(not set)'}"
        )

    def __repr__(self):
        return self.report()



