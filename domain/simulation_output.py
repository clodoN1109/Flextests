class SimulationOutput:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def __eq__(self, other) -> bool:
        return self.key == other.key and self.value == other.value