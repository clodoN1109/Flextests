import json
from pathlib import Path
from typing import Optional
from application.ports.i_repository import IJsonRepository
from domain.simulation import Simulation
from domain.test import Test, TestCriteria
from infrastructure.environment.environment import Env


class JsonRepository(IJsonRepository):
    """Concrete repository for persisting simulations and tests into JSON files."""

    def __init__(self):
        self.data_dir: Path = Env.get_data_dir()
        self.sim_file: Path = self.data_dir.joinpath("simulations.json")
        self.test_file: Path = self.data_dir.joinpath("tests.json")

    # ---------------- Simulations ----------------

    def save_new_simulation(self, new_sim: Simulation) -> None:
        """Save only the simulation's name, script path, and description."""
        sim_entry = {
            "name": new_sim.name,
            "script_path": new_sim.script_path,
            "description": new_sim.description,
        }

        data = self._load_json(self.sim_file)
        data.append(sim_entry)
        self._save_json(self.sim_file, data)

    def get_simulation_by_name(self, name: str) -> Optional[Simulation]:
        """Retrieve a Simulation by name."""
        data = self._load_json(self.sim_file)

        for entry in data:
            if entry.get("name") == name:
                return Simulation(
                    name=entry["name"],
                    script_path=entry["script_path"],
                    description=entry.get("description", ""),
                )
        return None

    # ---------------- Tests ----------------

    def save_new_test(self, test: Test) -> None:
        """Save a Test with its simulation reference, criteria, and references."""
        test_entry = {
            "name": test.name,
            "description": test.description,
            "simulation": {
                "name": test.simulation.name,
                "script_path": test.simulation.script_path,
                "description": test.simulation.description,
            } if test.simulation else None,
            "criteria": {
                "duration": test.criteria.duration,
                "max_memory": test.criteria.max_memory,
                "mean_memory": test.criteria.mean_memory,
            } if test.criteria else None,
            "references": (
                test.references.values if test.references else None
            ),
        }

        data = self._load_json(self.test_file)
        data.append(test_entry)
        self._save_json(self.test_file, data)

    def get_test_by_name(self, name: str) -> Optional[Test]:
        """Retrieve a Test by name, rebuilding Simulation, TestCriteria, and TestReferences if present."""
        data = self._load_json(self.test_file)

        for entry in data:
            if entry.get("name") == name:
                # --- rebuild Simulation ---
                sim_data = entry.get("simulation")
                simulation = (
                    Simulation(
                        name=sim_data["name"],
                        script_path=sim_data["script_path"],
                        description=sim_data.get("description", ""),
                    )
                    if sim_data
                    else None
                )

                # --- rebuild TestCriteria ---
                crit_data = entry.get("criteria")
                criteria = (
                    TestCriteria(
                        duration=crit_data.get("duration"),
                        max_memory=crit_data.get("max_memory"),
                        mean_memory=crit_data.get("mean_memory"),
                    )
                    if crit_data
                    else None
                )

                # --- rebuild TestReferences ---
                ref_data = entry.get("references")
                references = TestReferences(ref_data) if ref_data else None

                # --- assemble Test ---
                test = Test(
                    test_name=entry["name"],
                    description=entry.get("description", ""),
                )
                test.simulation = simulation
                test.criteria = criteria
                test.references = references
                return test

        return None

    # ---------------- Helpers ----------------

    @staticmethod
    def _load_json(file_path: Path) -> list:
        if file_path.exists():
            with file_path.open("r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    @staticmethod
    def _save_json(file_path: Path, data: list) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
