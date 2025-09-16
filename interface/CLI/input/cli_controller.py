from interface.CLI.input.cli_parser import CLIParser
from interface.CLI.input.commands import *
from application.app import App
from infrastructure.persistence.json_repository import JsonRepository
from interface.GUI.gui_launcher import GUI

class CLIController:
    @staticmethod
    def execute(command_name: str, options: List[str]):

        cmd = CLIParser.parse_as_command(command_name, options)

        app = App(JsonRepository())

        if isinstance(cmd, CLIHelpCommand):
            cli_help_instructions = app.cli_help()
            print(cli_help_instructions)

        if isinstance(cmd, LaunchGUICommand):
            gui = GUI()
            gui.prepare(App(JsonRepository()), cmd.args)
            gui.launch()
