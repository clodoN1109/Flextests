import math
import os
from typing import List, Dict
import datetime
import numpy as np
from application.ports.i_repository import IRepository
#from domain import ()

from infrastructure.environment.environment import Env


class App:

    def __init__(self, repository: IRepository):
        self.repository : IRepository      = repository

    def update_repository(self, repository: IRepository):
        self.repository: IRepository = repository

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

=====================================================
    """
        return help_text