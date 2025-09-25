from typing import List


class ResultsPlotData:
    def __init__(self, title = "", subtitle = "", variable_name = "", data: list[str | float | int | None] = None):
        self.title = title
        self.subtitle = subtitle
        self.variable_name = variable_name
        self.data = data

    def __repr__(self) -> str:
        preview_len = 6  # how many elements to preview
        data_preview = (
            ", ".join(map(str, self.data[:preview_len])) +
            ("..." if len(self.data) > preview_len else "")
        )
        return (
            f"ResultsPlotData("
            f"title='{self.title}', "
            f"subtitle='{self.subtitle}', "
            f"variable='{self.variable_name}', "
            f"data=[{data_preview}] (n={len(self.data)})"
            f")"
        )
