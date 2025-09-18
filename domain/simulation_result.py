from domain.simulation_output import SimulationOutput
from domain.simulation_statistics import SimulationStats


class SimulationResult:
    def __init__(self, stats: SimulationStats, output: SimulationOutput):
        self.stats = stats
        self.output = output