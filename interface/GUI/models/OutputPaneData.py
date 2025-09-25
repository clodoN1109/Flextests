from interface.GUI.models.ReferencesTable import ReferencesTable
from interface.GUI.models.ResultsPlotData import ResultsPlotData
from interface.GUI.models.ResultsSummaryTable import ResultsSummaryTable
from interface.GUI.models.ResultsTable import ResultsTable


class OutputPaneData:
    def __init__(self, test_description:str,
                 references_table_data:ReferencesTable,
                 results_summary_data:ResultsSummaryTable,
                 results_table_data: ResultsTable,
                 plot_data:ResultsPlotData):
        self.test_description = test_description
        self.references_table_data = references_table_data
        self.results_summary_data = results_summary_data
        self.results_table_data = results_table_data
        self.plot_data = plot_data
