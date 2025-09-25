import json
from pathlib import Path
from typing import Optional, List, Any
from application.ports.i_repository import IRepository
from domain.simulation import Simulation
from domain.test import Test, TestCriteria
from domain.test_reference import TestReference
from infrastructure.environment.environment import Env
from interface.GUI.gui_config import GUIConfig


class Repository(IRepository):
    """Concrete repository for persisting simulations and tests into JSON files."""

    def __init__(self):
        self.data_dir: Path = Env.get_data_dir()
        self.test_file: Path = self.data_dir.joinpath("tests.json")
        self.gui_config_file: Path = self.data_dir.joinpath("gui_config.json")

    # ---------------- Configurations ----------------

    def save_gui_config(self, config: "GUIConfig") -> None:
        """Save GUI configuration to file."""
        self.gui_config_file.parent.mkdir(parents=True, exist_ok=True)
        with self.gui_config_file.open("w", encoding="utf-8") as f:
            json.dump(config.__dict__, f, indent=2, ensure_ascii=False)

    def load_gui_config(self) -> "GUIConfig":
        """Load GUI configuration from file. Creates file with defaults if missing/invalid."""
        if not self.gui_config_file.exists():
            default_config = GUIConfig()
            self.save_gui_config(default_config)
            return default_config

        try:
            with self.gui_config_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            # If file is corrupt, reset to defaults
            default_config = GUIConfig()
            self.save_gui_config(default_config)
            return default_config

        if not isinstance(data, dict):
            # Unexpected structure → reset to defaults
            default_config = GUIConfig()
            self.save_gui_config(default_config)
            return default_config

        cfg = GUIConfig()
        for key, value in data.items():
            if hasattr(cfg, key):
                setattr(cfg, key, value)
        return cfg

    # ---------------- Tests ----------------

    def save_test(self, test: Test) -> None:
        """Save a Test with its simulation reference, criteria, and reference."""
        test_entry = {
            "name": test.name,
            "description": test.description,
            "simulation": {
                "name": test.simulation.name,
                "script_path": test.simulation.script_path,
                "description": test.simulation.description,
            } if test.simulation else None,
            "criteria": {
                "duration": test.criteria.duration if test.criteria else "",
                "max_memory": test.criteria.max_memory if test.criteria else "",
                "mean_memory": test.criteria.mean_memory if test.criteria else "",
                "compliance_rate": test.criteria.compliance_rate if test.criteria else "",
            },
            "reference_source": test.reference_source,
            "reference": [
                {
                    "parameters": ref.parameters,
                    "result": ref.result,
                }
                for ref in (test.reference or [])
            ],
        }

        data = self._load_json(self.test_file)
        data.append(test_entry)
        self._save_json(self.test_file, data)

    def get_all_tests(self) -> List[Test]:
        """Retrieve all tests, rebuilding Simulation, TestCriteria, and TestReference list if present."""
        data = self._load_json(self.test_file)
        all_tests: List[Test] = []

        for entry in data:
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
                    compliance_rate=crit_data.get("compliance_rate"),
                )
                if crit_data
                else None
            )
            # --- rebuild reference source ---
            ref_source_data = entry.get("reference_source", [])
            reference_source = ref_source_data[0] if ref_source_data else None

            # --- rebuild TestReference ---
            ref_data = entry.get("reference", [])
            reference = [
                TestReference(
                    parameters=ref.get("parameters", {}),
                    result=ref.get("result", None),
                )
                for ref in ref_data
            ]

            # --- assemble Test ---
            test = Test(
                test_name=entry["name"],
                description=entry.get("description", ""),
            )
            test.simulation = simulation
            test.criteria = criteria
            test.reference_source = reference_source
            test.reference = reference

            all_tests.append(test)

        return all_tests

    def get_test_by_name(self, name: str) -> Optional[Test]:
        """Retrieve a Test by name, rebuilding Simulation, TestCriteria, and TestReference list if present."""
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
                        compliance_rate=crit_data.get("compliance_rate"),
                    )
                    if crit_data
                    else None
                )

                # --- rebuild reference source ---
                ref_source_data = entry.get("reference_source", [])
                reference_source = ref_source_data if ref_source_data else None

                # --- rebuild TestReference ---
                ref_data = entry.get("reference", [])
                reference = [
                    TestReference(
                        parameters=ref.get("parameters", {}),
                        result=ref.get("result", None),
                    )
                    for ref in ref_data
                ]

                # --- assemble Test ---
                test = Test(
                    test_name=entry["name"],
                    description=entry.get("description", ""),
                )
                test.simulation = simulation
                test.criteria = criteria
                test.reference_source = reference_source
                test.reference = reference
                return test

        return None

    def update_test(self, test: "Test") -> None:
        """Update an existing test by removing the old entry and saving the new one."""
        data = self._load_json(self.test_file)
        # Remove any existing entry with the same name
        new_data = [entry for entry in data if entry.get("name") != test.name]

        if len(new_data) == len(data):
            raise ValueError(f"Test with name '{test.name}' not found for update.")

        # Save the updated test using the existing save_test logic
        self._save_json(self.test_file, new_data)  # first save the data without the old test
        self.save_test(test)  # now append the updated test

    def remove_test(self, test: "Test") -> None:
        """Remove a test entry by its name."""
        data = self._load_json(self.test_file)
        new_data = [entry for entry in data if entry.get("name") != test.name]

        if len(new_data) == len(data):
            raise ValueError(f"Test with name '{test.name}' not found for removal.")

        self._save_json(self.test_file, new_data)

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
