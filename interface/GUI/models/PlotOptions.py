class PlotOptions:
    def __init__(self, selected_variable:str, plot_type:str, resolution:int):
        self.plot_type:str = plot_type
        self.selected_variable:str = selected_variable
        self.resolution:int = resolution