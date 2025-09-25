class SimulationStats:
    def __init__(
        self,
        duration: float = 0.0,
        max_memory: float = 0.0,
        min_memory: float = 0.0,
        mean_memory: float = 0.0,
    ):
        self.duration = duration
        self.max_memory = max_memory
        self.min_memory = min_memory
        self.mean_memory = mean_memory

    def __repr__(self) -> str:
        return (
            f"SimulationStats:"
            f"\n\t\t  Duration: {self.duration:.4f}s"
            f"\n\t\t  Min Memory: {self.min_memory:.2f}MB"
            f"\n\t\t  Max Memory: {self.max_memory:.2f}MB"
            f"\n\t\t  Mean Memory: {self.mean_memory:.2f}MB"
        )

    def get_value_by_name(self, name: str):
        """Return the value of the stat with the given name (case-insensitive)."""
        normalized = name.strip().lower().replace(" ", "_")
        mapping = {
            "duration": self.duration,
            "max_memory": self.max_memory,
            "min_memory": self.min_memory,
            "mean_memory": self.mean_memory,
        }
        if normalized not in mapping:
            raise ValueError(
                f"Unknown stat name '{name}'. "
                f"Valid options: {', '.join(mapping.keys())}"
            )
        return mapping[normalized]

