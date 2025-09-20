from application.ports.i_repository import IRepository
from domain.simulation import Simulation
from domain.simulation_result import SimulationResult
from domain.test import Test
from domain.test_criteria import TestCriteria
from domain.test_reference import TestReference
from infrastructure.io.json_fetcher import JsonFetcher


class App:

    def __init__(self, repository: IRepository):
        self.repository : IRepository      = repository

    def new_simulation(self, simulation_name: str, script_path: str, description: str = ""):
        new_sim = Simulation(simulation_name, script_path, description)
        self.repository.save_new_simulation(new_sim)

    def run_simulation(self, simulation_name: str) -> SimulationResult:
        selected_sim  = self.repository.get_simulation_by_name(simulation_name)
        selected_sim.run()
        return selected_sim.results[-1]

    def new_test(self, test_name: str, description: str = ""):
        new_test = Test(test_name, description)
        self.repository.save_test(new_test)

    def set_simulation(self, test_name, simulation_name: str):
        selected_sim  = self.repository.get_simulation_by_name(simulation_name)
        selected_test = self.repository.get_test_by_name(test_name)
        selected_test.simulation = selected_sim
        self.repository.update_test(selected_test)

    def set_references_from_simulation(self, test_name: str, number_of_references: int = 5):
        selected_test = self.repository.get_test_by_name(test_name)
        for _ in range(number_of_references):
            selected_test.simulation.run()
        selected_test.references = [TestReference(sim_result.result, sim_result.parameters)
                                    for sim_result in selected_test.simulation.results]
        self.repository.update_test(selected_test)

    def set_references_from_source(self, test_name: str, reference_source: str):
        selected_test = self.repository.get_test_by_name(test_name)
        selected_test.references = JsonFetcher(max_depth=4).fetch_as(reference_source, lambda d: TestReference(**d))
        self.repository.update_test(selected_test)

    def set_criterion(self, test_name: str, criterion_name: str, criterion_value: str):
        selected_test = self.repository.get_test_by_name(test_name)
        if selected_test.criteria is None:
            selected_test.criteria = TestCriteria()

        # ensure only valid attributes can be set
        if hasattr(selected_test.criteria, criterion_name):
            # cast criterion_value to float or None if appropriate
            value = float(criterion_value) if criterion_value is not None else None
            setattr(selected_test.criteria, criterion_name, value)
        else:
            raise AttributeError(f"Invalid criterion name: {criterion_name}")

        self.repository.update_test(selected_test)

    def run_test(self, test_name: str, number_of_repetitions: int):
        selected_test = self.repository.get_test_by_name(test_name)
        selected_test.execute(number_of_repetitions)

        print(selected_test.simulation.get_plot_data("duration"))

        return selected_test.report()