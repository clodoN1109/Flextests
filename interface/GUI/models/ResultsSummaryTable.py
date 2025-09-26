from domain.test_statistics import TestStats


class ResultsSummaryTable:
    def __init__(self, test_stats:TestStats):
        self.sample_size:int     = test_stats.total
        self.effective_instances:int = test_stats.effective
        self.efficient_instances:int = test_stats.efficient
        self.compliance:float        = test_stats.compliance_rate