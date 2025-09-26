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
            gui.prepare(App(Repository()), self.repository.load_gui_config())
            gui.launch()

        if isinstance(cmd, SetSimulationCommand):
            self.app.set_simulation(cmd.test_name, cmd.simulation_name)

        if isinstance(cmd, RunTestCommand):
            results = self.app.run_test(cmd.test_name, cmd.repetitions)
            self.presenter.text_block(results)

        if isinstance(cmd, NewTestCommand):
            self.app.new_test(cmd.test_name, cmd.description, cmd.simulation_script)

        if isinstance(cmd, ListTestsCommand):
            test_list =  self.repository.get_all_tests()
            names_list =  [test.name for test in test_list]
            self.presenter.text_block(names_list)

        if isinstance(cmd, SetCriterionCommand):
            self.app.set_criterion(cmd.test_name, cmd.criterion_name, cmd.criterion_value)

        if isinstance(cmd, UpdateReferenceCommand):
                self.app.update_reference(cmd.test_name, cmd.data_points)

        self._update_repository()

    def _update_repository(self):
        self.repository = Repository()
        self.app = App(self.repository)
