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
        cls.args = args[1:]

@dataclass
class LaunchGUICommand(Command):

    @classmethod
    def command_name(cls) -> str:
        return "gui"

    @classmethod
    def __init__(cls, args: list[str]):
        cls.name = cls.command_name()
        cls.args = args[1:]