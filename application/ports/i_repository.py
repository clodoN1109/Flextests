from abc import ABC, abstractmethod
from typing import Optional, List
from domain.test import Test
from interface.GUI.gui_config import GUIConfig


class IRepository(ABC):

    @abstractmethod
    def save_test(self, test: Test) -> None:
        """Persist a new Test (with simulation reference and criteria)."""
        pass

    @abstractmethod
    def get_test_by_name(self, name: str) -> Optional[Test]:
        """Retrieve a Test by name, or None if not found."""
        pass

    def get_all_tests(self) -> List[Test]:
        """Retrieve all tests, rebuilding Simulation, TestCriteria, and TestReference list if present."""

    @abstractmethod
    def update_test(self, test: "Test") -> None:
        pass

    @abstractmethod
    def remove_test(self, test: "Test") -> None:
        pass

    def save_gui_config(self, config: "GUIConfig") -> None:
        """Save GUI configuration to file."""

    def load_gui_config(self) -> "GUIConfig":
        """Load GUI configuration from file. Creates file with defaults if missing/invalid."""