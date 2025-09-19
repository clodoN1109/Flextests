from typing import List

from interface.CLI.input.commands import *


class CLIParser:
    @staticmethod
    def parse_as_command(command_name: str, args: List[str]) -> Command:
        return {
            "help"                  : CLIHelpCommand,
            "gui"                   : LaunchGUICommand,
            "new-test"              : NewTestCommand,
            "new-sim"               : NewSimulationCommand,
            "set-sim"               : SetSimulationCommand,
            "run-sim"               : RunSimulationCommand,
            "set-ref"               : SetReferencesCommand,
            "set-criterion"         : SetCriterionCommand,
            "run-test"              : RunTestCommand,


        }[command_name](args)