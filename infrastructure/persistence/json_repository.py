import json
from pathlib import Path
from typing import List
from application.ports.i_repository import IRepository
from infrastructure.environment.environment import Env


class JsonRepository(IRepository):
    """Concrete repository using a JSON file."""

    def __init__(self):
        pass

