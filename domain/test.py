from typing import List

from domain.failed_result import FailedResult
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
        compliance_rate = self.stats.effective_and_efficient/self.stats.total if self.stats.total != 0 else 0
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
        result: TestResult = TestResult()

        # --- efficacy → check result against reference ---
        if reference:
            # try to find a matching reference by parameters
            matching_ref = next(
                (ref for ref in reference if ref.parameters == sim_result.parameters),
                None,
            )

            if matching_ref:
                # Compare each expected key/value pair
                for key, expected_value in matching_ref.results.items():
                    actual_value = sim_result.results.get(key)
                    if actual_value != expected_value:
                        result.failed_results.append(
                            FailedResult(key, str(actual_value), expected_value)
                        )

                result.efficacy = "passed" if not result.failed_results else "failed"
            else:
                # reference exists but no matching parameters
                result.efficacy = "failed"
                result.failed_results.append(
                    FailedResult(
                        key="parameters",
                        value=str(sim_result.parameters),
                        expected_value="matching reference parameters",
                    )
                )
        else:
            # no reference at all → mark as failed (not enough info to check)
            result.efficacy = "failed"
            result.failed_results.append(
                FailedResult(
                    key="reference",
                    value="None",
                    expected_value="at least one reference",
                )
            )

        # --- efficiency → check duration & memory ---
        if criteria:
            stats = sim_result.stats
            eff_failures: list[FailedResult] = []

            if criteria.duration is not None and stats.duration > criteria.duration:
                eff_failures.append(
                    FailedResult("duration", str(stats.duration), criteria.duration)
                )
            if criteria.max_memory is not None and stats.max_memory > criteria.max_memory:
                eff_failures.append(
                    FailedResult("max_memory", str(stats.max_memory), criteria.max_memory)
                )
            if criteria.mean_memory is not None and stats.mean_memory > criteria.mean_memory:
                eff_failures.append(
                    FailedResult("mean_memory", str(stats.mean_memory), criteria.mean_memory)
                )

            if eff_failures:
                result.efficiency = "failed"
                result.failed_results.extend(eff_failures)
            else:
                result.efficiency = "passed"
        else:
            result.efficiency = "passed"  # no criteria → auto-pass

        # Always keep a reference to the simulation
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



