from domain.test_statistics import TestStats


class ResultsSummaryTable:
    def __init__(self, test_stats:TestStats):
        self.sample_size         = test_stats.total
        self.effective_instances = test_stats.effective
        self.efficient_instances = test_stats.efficient
        self.compliance          = test_stats.compliance_rate