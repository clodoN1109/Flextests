from application.ports.i_repository import IJsonRepository
from domain.simulation import Simulation
from domain.simulation_result import SimulationResult
from domain.test import Test
from domain.test_reference import TestReference


class App:

    def __init__(self, repository: IJsonRepository):
        self.repository : IJsonRepository      = repository

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

    def set_criterion(self, criterion_name, criterion_value):
        pass

    @staticmethod
    def cli_help() -> str:
        """Prints an organized description of how to use the CLI interface."""

        help_text = """
=====================================================
                FLEXTESTS CLI HELP
=====================================================

Available Commands:


- help
   - Displays this help message.
   
-gui
    - Launches the GUI.

=====================================================
    """
        return help_text