from domain.simulation_result import SimulationResult
from domain.simulation_statistics import SimulationStats
import os
import sys
import time
import json
import shutil
import psutil
import subprocess
from typing import List

class Simulation:
    # -----------------------------------------------------------------------------
    # Simulation script JSON output format:
    #
    # Each simulation script must print a JSON object with exactly two keys:
    #   1. "result"     → a string representing the main outcome of the simulation
    #   2. "parameters" → a dictionary of parameter names (strings) and their
    #                      corresponding values (strings) used in this simulation
    #
    # Example of valid output:
    # {
    #     "result": "result_3",
    #     "parameters": {
    #         "x": "7",
    #         "y": "25",
    #         "z": "150"
    #     }
    # }
    #
    # The program will parse this JSON to create a SimulationResult object.
    # -----------------------------------------------------------------------------
    def __init__(self, name: str, script_path: str, description: str = ""):
        self.name = name
        self.script_path = script_path
        self.description = description
        self.results: List[SimulationResult] = []

    def run(self, iteration:int = 1):
        result: SimulationResult = self._run_script(self.script_path, True, iteration=iteration)
        self.results.append(result)

    def get_plot_data(self, stats_name: str):
        stats = [result.stats for result in self.results if result.stats is not None]
        selected_stats_var = [getattr(item, stats_name) for item in stats if hasattr(item, stats_name)]
        return selected_stats_var

    @staticmethod
    def _run_script(script_path: str, capture_output: bool, **params) -> "SimulationResult":
        ext = os.path.splitext(script_path)[1].lower()

        # Find Python interpreter if frozen
        if getattr(sys, "frozen", False):
            python_exec = shutil.which("python") or shutil.which("python3")
            if not python_exec:
                raise RuntimeError("Python interpreter not found in PATH.")
        else:
            python_exec = sys.executable

        interpreters = {
            ".py": [python_exec],
            ".ps1": ["pwsh", "-ExecutionPolicy", "Bypass", "-File"],
            ".sh": ["bash"],
            ".bat": None,
            ".rb": ["ruby"],
        }

        if ext not in interpreters:
            raise RuntimeError(f"Unsupported script type: {ext}")

        cmd = interpreters[ext]
        if cmd is None:
            cmdline = [script_path]
        else:
            if shutil.which(cmd[0]) is None:
                raise RuntimeError(f"Interpreter not found: {cmd[0]}")
            cmdline = cmd + [script_path]

        # Normalize args
        args = Simulation._format_args(ext, params)
        cmdline = cmdline + args

        start = time.perf_counter()
        proc = subprocess.Popen(
            cmdline,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True,
        )
        ps_proc = psutil.Process(proc.pid)

        mem_samples = []
        try:
            while True:
                if proc.poll() is not None:  # finished
                    break
                try:
                    mem_info = ps_proc.memory_info()
                    mem_samples.append(mem_info.rss / (1024 * 1024))  # MB
                except psutil.NoSuchProcess:
                    break
                time.sleep(0.05)
        finally:
            stdout, stderr = proc.communicate()
            duration = time.perf_counter() - start

        if proc.returncode != 0:
            raise RuntimeError(f"Script failed with exit code {proc.returncode}:\n{stderr}")

        # --- compute stats ---
        if mem_samples:
            min_mem = min(mem_samples)
            max_mem = max(mem_samples)
            mean_mem = sum(mem_samples) / len(mem_samples)
        else:
            min_mem = max_mem = mean_mem = 0.0

        stats = SimulationStats(
            duration=duration,
            min_memory=min_mem,
            max_memory=max_mem,
            mean_memory=mean_mem,
        )

        # --- parse output into result + parameters ---
        result = ""
        parameters: dict[str, str] = {}

        if capture_output and stdout:
            text = stdout.strip()
            try:
                data = json.loads(text)
                if not isinstance(data, dict):
                    raise ValueError("JSON output must be an object")

                # --- new expected format ---
                if "result" in data and "parameters" in data:
                    result = str(data["result"]).strip()
                    if not isinstance(data["parameters"], dict):
                        raise ValueError("'parameters' must be a dictionary")
                    parameters = {str(k): str(v) for k, v in data["parameters"].items()}
                # --- fallback: single key=value pair ---
                elif len(data) == 1:
                    key, value = next(iter(data.items()))
                    result = str(value).strip()
                    parameters = {str(key).strip(): str(value).strip()}
                else:
                    raise ValueError(
                        "JSON output must be either {'result':..., 'parameters': {...}} or a single key-value pair"
                    )

            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Expected JSON output, got: {text}"
                ) from e

        return SimulationResult(stats=stats, result=result, parameters=parameters)

    @staticmethod
    def _format_args(ext: str, params: dict) -> list[str]:
        """
        Normalize argument syntax depending on script type.
        """
        if not params:
            return []

        if ext in (".py", ".rb"):
            # Python & Ruby => --flag value
            args = []
            for k, v in params.items():
                args.append(f"--{k}")
                args.append(str(v))
            return args

        elif ext == ".ps1":
            # PowerShell => -Flag value
            args = []
            for k, v in params.items():
                args.append(f"-{k}")
                args.append(str(v))
            return args

        elif ext in (".sh", ".bat"):
            # Shell & Batch => positional arguments
            return [str(v) for v in params.values()]

        else:
            raise RuntimeError(f"Unsupported script type: {ext}")


