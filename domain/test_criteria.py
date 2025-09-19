class TestCriteria:
    def __init__(
        self,
        duration        : float | None = None,
        max_memory      : float | None = None,
        mean_memory     : float | None = None,
        compliance_rate : float | None = None,
    ):
        self.duration = duration
        self.max_memory = max_memory
        self.mean_memory = mean_memory
        self.compliance_rate = compliance_rate

    def __repr__(self) -> str:
        return (
            f"TestCriteria(duration={self.duration}, "
            f"max_memory={self.max_memory}, mean_memory={self.mean_memory}, compliance_rate={self.compliance_rate})"
        )