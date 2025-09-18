import json
from typing import List
import os
import sys
import time
import shutil
import psutil
import subprocess
from domain.simulation_output import SimulationOutput
from domain.simulation_result import SimulationResult
from domain.simulation_statistics import SimulationStats

class Simulation:
    def __init__(self, name: str, script_path: str, description: str = ""):
        self.name = name
        self.script_path = script_path
        self.description = description
        self.results: List[SimulationResult] = []

    def run(self):
        result: SimulationResult = self._run_script(self.script_path, True)
        self.results.append(result)

    @staticmethod
    def _run_script(script_path: str, capture_output: bool) -> SimulationResult:
        ext = os.path.splitext(script_path)[1].lower()

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

        # Compute stats
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

        # If capturing, wrap stdout into SimulationOutput
        output = None
        if capture_output and stdout:
            text = stdout.strip()
            # --- case 1: key=value format ---
            if "=" in text and not text.startswith("{"):
                key, value = text.split("=", 1)
                output = SimulationOutput(key.strip(), value.strip())

            # --- case 2: JSON format (single key-value) ---
            else:
                try:
                    data = json.loads(text)
                    if not isinstance(data, dict) or len(data) != 1:
                        raise ValueError("JSON output must be an object with exactly one key-value pair")
                    key, value = next(iter(data.items()))
                    output = SimulationOutput(str(key).strip(), str(value).strip())
                except json.JSONDecodeError as e:
                    raise ValueError(
                        f"Expected 'key=value' or single-pair JSON format in script output, got: {text}"
                    ) from e

        return SimulationResult(stats=stats, output=output)





