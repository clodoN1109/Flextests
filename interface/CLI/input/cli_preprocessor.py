from pathlib import Path
from typing import Self
import unicodedata


class InputPreProcessor:

    def __init__(self, initial_value):
        self._value = initial_value

    def get_result(self):
        return self._value

    def normalize(self, is_path: bool = False) -> Self:
        self._value = unicodedata.normalize("NFC", self._value).strip()
        if is_path:
            self._value = str(Path(self._value))
        return self