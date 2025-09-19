from abc import ABC, abstractmethod
from typing import Optional
from domain.simulation import Simulation
from domain.test import Test


class IJsonRepository(ABC):

    @abstractmethod
    def save_new_simulation(self, new_sim: Simulation) -> None:
        """Persist a new Simulation (only metadata, not results)."""
        pass

    @abstractmethod
    def get_simulation_by_name(self, name: str) -> Optional[Simulation]:
        """Retrieve a Simulation by name, or None if not found."""
        pass

    @abstractmethod
    def save_test(self, test: Test) -> None:
        """Persist a new Test (with simulation reference and criteria)."""
        pass

    @abstractmethod
    def get_test_by_name(self, name: str) -> Optional[Test]:
        """Retrieve a Test by name, or None if not found."""
        pass

    @abstractmethod
    def update_test(self, test: "Test") -> None:
        pass

    @abstractmethod
    def remove_test(self, test: "Test") -> None:
        pass