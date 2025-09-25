from application.ports.i_repository import IRepository
from domain.simulation import Simulation
from domain.test import Test
from domain.test_criteria import TestCriteria
from domain.test_reference import TestReference
from infrastructure.io.json_fetcher import JsonFetcher


class App:

    def __init__(self, repository: IRepository):
        self.repository : IRepository      = repository

    def new_test(self, test_name: str, description: str = "", simulation_script:str = ""):
        new_test = Test(test_name, description, simulation_script)
        self.repository.save_test(new_test)

    def edit_test(self, current_test_name, new_test_name: str, description: str = "", simulation_script:str = ""):
        selected_test = self.get_test_by_name(current_test_name)
        self.repository.remove_test(selected_test)

        selected_test.name = new_test_name
        selected_test.description = description
        selected_test.simulation = Simulation(new_test_name, simulation_script, description)
        self.repository.save_test(selected_test)

    def delete_test(self, test_name):
        selected_test = self.get_test_by_name(test_name)
        self.repository.remove_test(selected_test)

    def get_tests_list(self):
        return self.repository.get_all_tests()

    def get_test_by_name(self, test_name: str):
        return self.repository.get_test_by_name(test_name)

    def run_test(self, test_name: str, number_of_repetitions: int) -> Test:
        selected_test = self.repository.get_test_by_name(test_name)
        selected_test.execute(number_of_repetitions)
        return selected_test

    def set_simulation(self, test_name, simulation_script: str):
        selected_test = self.repository.get_test_by_name(test_name)
        selected_test.simulation = Simulation(test_name, simulation_script, selected_test.description)
        self.repository.update_test(selected_test)

    def set_reference_source(self, test_name, reference_source: str):
        selected_test = self.repository.get_test_by_name(test_name)
        selected_test.reference_source = reference_source
        self.repository.update_test(selected_test)

    def update_reference(self, test_name: str, data_points: int | None = None):
        selected_test = self.repository.get_test_by_name(test_name)
        fetcher = JsonFetcher(max_depth=4)
        reference = fetcher.fetch_as(selected_test.reference_source, lambda d: TestReference(**d))
        selected_test.reference = reference[0:data_points] if (data_points is not None and len(reference) >= data_points) else reference
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

