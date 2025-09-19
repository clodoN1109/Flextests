from dataclasses import dataclass
from typing import List


@dataclass
class Command:
    """Base class for CLI commands."""
    name: str
    args: List[str]

@dataclass
class CLIHelpCommand(Command):

    @classmethod
    def command_name(cls) -> str:
        return "help"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args

@dataclass
class LaunchGUICommand(Command):

    @classmethod
    def command_name(cls) -> str:
        return "gui"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args

@dataclass
class NewTestCommand(Command):

    @classmethod
    def command_name(cls) -> str:
        return "new-test"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args
        cls.test_name = args[0]
        cls.description = args[1]

@dataclass
class NewSimulationCommand(Command):

    @classmethod
    def command_name(cls) -> str:
        return "new-sim"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args
        cls.simulation_name = args[0]
        cls.script_path     = args[1]
        cls.description     = args[2]

@dataclass
class SetSimulationCommand(Command):

    @classmethod
    def command_name(cls) -> str:
        return "set-sim"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args
        cls.test_name       = args[0]
        cls.simulation_name = args[1]

@dataclass
class RunSimulationCommand(Command):

    @classmethod
    def command_name(cls) -> str:
        return "run-sim"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args
        cls.simulation_name = args[0]

@dataclass
class RunTestCommand(Command):

    @classmethod
    def command_name(cls) -> str:
        return "run-test"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args
        cls.test_name = args[0]
        cls.repetitions = int(args[1]) if len(args)>1 else 1


@dataclass
class SetCriterionCommand(Command):

    @classmethod
    def command_name(cls) -> str:
        return "set-criterion"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args
        cls.test_name       = args[0]
        cls.criterion_name  = args[1]
        cls.criterion_value = args[2]

@dataclass
class SetReferencesCommand(Command):
    # -----------------------------------------------------------------------------
    # Test reference source (reference_source):
    #
    # The `reference_source` argument must point to either a URL or a local json
    # that provides a JSON list of reference elements. Each element must be a JSON
    # object with the following structure:
    #
    # {
    #     "result": "string representing expected outcome",
    #     "parameters": {
    #         "param_name_1": "param_value_1",
    #         "param_name_2": "param_value_2",
    #         ...
    #     }
    # }
    #
    # Example:
    # [
    #     {
    #         "result": "result_1",
    #         "parameters": {
    #             "x": "3",
    #             "y": "25",
    #             "z": "150"
    #         }
    #     },
    #     {
    #         "result": "result_2",
    #         "parameters": {
    #             "x": "5",
    #             "y": "28",
    #             "z": "180"
    #         }
    #     }
    # ]
    #
    # Each object in the list will be used to build a TestReference:
    #   - `result` maps to TestReference.result
    #   - `parameters` maps to TestReference.parameters
    # This allows automated evaluation of simulation results against known references.
    # -----------------------------------------------------------------------------

    @classmethod
    def command_name(cls) -> str:
        return "set-ref"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args
        cls.test_name            = args[0]
        cls.reference_source     = args[1] if len(args) > 1 else None
        cls.number_of_references = int(args[2]) if len(args) > 2 else 5
