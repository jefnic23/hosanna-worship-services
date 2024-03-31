import os
from pathlib import Path

from services.settings import Settings


class Liturgy:
    """
    A class to handle the liturgy files.
    """

    def __init__(self, settings: Settings):
        self._files: dict[str, str] = ({},)
        self._path: str = f"{settings.LOCAL_DIR}/liturgy"

    def __getattr__(self, name: str) -> str:
        """
        Return the liturgy file, e.g. liturgy.creed
        """
        if name in self._files:
            return self._files[name]
        raise AttributeError(f"{name} not found")

    def __dir__(self) -> list[str]:
        """
        List all the liturgy files, e.g. dir(liturgy)
        """
        return list(self._files.keys())

    def list_seasons(self) -> list[str]:
        """
        List all liturgical seasons.
        """
        if not os.path.exists(self._path):
            os.mkdir(self._path)

        return [
            dir
            for dir in os.listdir(self._path)
            if os.path.isdir(f"{self._path}/{dir}")
        ]

    def list_files(self, season: str) -> list[str]:
        """
        List files for a liturgical season.
        """
        return [file for file in os.listdir(f"{self._path}/{season}")]

    def load_files(self, season: str) -> None:
        """
        Open all the liturgy files for a given season.
        """
        path = Path(self._path, season)
        files = {}
        for file in os.listdir(path):
            if file.endswith(".txt"):
                files[Path(file).stem] = open(
                    f"{path}/{file}", "r", encoding="utf-8"
                ).read()
        self._files = files
