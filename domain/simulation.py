import time
from typing import List
import psutil
from domain.simulation_result import SimulationResult
from domain.simulation_statistics import SimulationStats
from infrastructure.io.json_fetcher import JsonFetcher


class Simulation:
    # -----------------------------------------------------------------------------
    # Simulation script JSON output format:
    #
    # Each simulation script must print a JSON object with exactly two keys:
    #   1. "result"     → a dictionary of names (strings) and their
    #                     corresponding values representing the outcomes of the simulation
    #   2. "parameters" → a dictionary of parameter names (strings) and their
    #                     corresponding values (strings) used in this simulation
    #
    # Example of valid output:
    # {
    #     "parameters": {
    #         "a": "71",
    #         "b": "25",
    #     },
    #     "results": {
    #         "area": "71",
    #         "diagonal": "25",
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

    def run(self, iteration: int = 1):
        result: SimulationResult = self._run_script(self.script_path, True)
        self.results.append(result)

    @staticmethod
    def _run_script(script_path: str, capture_output: bool = True) -> "SimulationResult":
        fetcher = JsonFetcher()  # can pass max_depth if you wants
        # Spawn process via fetcher so interpreter selection is centralized
        proc = fetcher.spawn_process(script_path, capture_output=capture_output)
        ps_proc = psutil.Process(proc.pid)

        mem_samples = []
        start = time.perf_counter()
        try:
            while True:
                if proc.poll() is not None:
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

        # compute memory stats
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

        # parse JSON output using JsonFetcher helper
        results: dict[str, str] = {}
        parameters: dict[str, str] = {}

        if capture_output and stdout:
            data = fetcher.parse_json(stdout)

            if not isinstance(data, dict):
                raise ValueError("JSON output must be an object")

            if "results" in data and "parameters" in data:
                if not isinstance(data["results"], dict):
                    raise ValueError("'results' must be a dictionary")
                results = {str(k): str(v) for k, v in data["results"].items()}
                if not isinstance(data["parameters"], dict):
                    raise ValueError("'parameters' must be a dictionary")
                parameters = {str(k): str(v) for k, v in data["parameters"].items()}
            else:
                raise ValueError(
                    "JSON output must be either {'results':..., 'parameters': {...}} or a single key-value pair"
                )

        return SimulationResult(stats=stats, results=results, parameters=parameters)
