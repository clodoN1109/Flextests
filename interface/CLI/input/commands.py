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
