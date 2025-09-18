from application.ports.i_repository import IJsonRepository
from domain.simulation import Simulation
from domain.test import Test


class App:

    def __init__(self, repository: IJsonRepository):
        self.repository : IJsonRepository      = repository

    def new_simulation(self, simulation_name: str, script_path: str, description: str = ""):
        new_sim = Simulation(simulation_name, script_path, description)
        self.repository.save_new_simulation(new_sim)

    def new_test(self, test_name: str, description: str = ""):
        new_test = Test(test_name, description)
        self.repository.save_new_test(new_test)

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