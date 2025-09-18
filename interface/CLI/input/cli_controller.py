from domain.test import Test
from interface.CLI.input.cli_parser import CLIParser
from interface.CLI.input.commands import *
from application.app import App
from infrastructure.persistence.json_repository import JsonRepository
from interface.CLI.output.cli_presenter import CLIPresenter
from interface.GUI.gui_launcher import GUI

class CLIController:

    def __init__(self):
        self.presenter = CLIPresenter()
        self.repository = JsonRepository()
        self.app = App(self.repository)

    def execute(self, command_name: str, options: List[str]):

        cmd = CLIParser.parse_as_command(command_name, options)

        if isinstance(cmd, CLIHelpCommand):
            cli_help_instructions = self.app.cli_help()
            self.presenter.text_block(cli_help_instructions)

        if isinstance(cmd, LaunchGUICommand):
            gui = GUI()
            gui.prepare(App(JsonRepository()), cmd.args)
            gui.launch()

        if isinstance(cmd, NewSimulationCommand):
            self.app.new_simulation(cmd.simulation_name, cmd.script_path, cmd.description)

        if isinstance(cmd, NewTestCommand):
            self.app.new_test(cmd.test_name, cmd.description)

        self._update_repository()

    def _update_repository(self):
        self.repository = JsonRepository()
        self.app = App(self.repository)
