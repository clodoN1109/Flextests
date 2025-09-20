from interface.CLI.input.cli_help import CLIHelp
from interface.CLI.input.cli_parser import CLIParser
from interface.CLI.input.commands import *
from application.app import App
from infrastructure.persistence.json_repository import Repository
from interface.CLI.output.cli_presenter import CLIPresenter
from interface.GUI.gui_launcher import GUI

class CLIController:

    def __init__(self):
        self.presenter = CLIPresenter()
        self.repository = Repository()
        self.app = App(self.repository)

    def execute(self, command_name: str, options: List[str]):

        cmd = CLIParser.parse_as_command(command_name, options)

        if isinstance(cmd, CLIHelpCommand):
            cli_help_instructions = CLIHelp.cli_help()
            self.presenter.text_block(cli_help_instructions)

        if isinstance(cmd, LaunchGUICommand):
            gui = GUI()
            gui.prepare(App(Repository()), cmd.args)
            gui.launch()

        if isinstance(cmd, NewSimulationCommand):
            self.app.new_simulation(cmd.simulation_name, cmd.script_path, cmd.description)

        if isinstance(cmd, SetSimulationCommand):
            self.app.set_simulation(cmd.test_name, cmd.simulation_name)

        if isinstance(cmd, RunSimulationCommand):
            results = self.app.run_simulation(cmd.simulation_name)
            self.presenter.text_block(results)

        if isinstance(cmd, RunTestCommand):
            results = self.app.run_test(cmd.test_name, cmd.repetitions)
            self.presenter.text_block(results)

        if isinstance(cmd, NewTestCommand):
            self.app.new_test(cmd.test_name, cmd.description)

        if isinstance(cmd, SetCriterionCommand):
            self.app.set_criterion(cmd.test_name, cmd.criterion_name, cmd.criterion_value)

        if isinstance(cmd, SetReferencesCommand):
            if cmd.reference_source is None or cmd.reference_source == "":
                self.app.set_references_from_simulation(cmd.test_name, cmd.number_of_references)
            else:
                self.app.set_references_from_source(cmd.test_name, cmd.reference_source)

        self._update_repository()

    def _update_repository(self):
        self.repository = Repository()
        self.app = App(self.repository)
