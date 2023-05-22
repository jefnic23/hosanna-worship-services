from datetime import date

import pandas as pd

from config import settings
from models.hymn import Hymn


class Hymns:
    """Class for adding hymns to the service."""


    LOCAL_DIR = settings.LOCAL_DIR
    DF = pd.read_csv('data/hymnal.csv', index_col='Number')


    def __init__(self) -> None:
        self.day: date = date.today()
        self._hymns: list[Hymn] = []
    

    def add_hymn(self, hymn_number: int) -> None:
        """Add hymn to service."""
        hymn = Hymns._get_hymn(hymn_number)
        self._hymns.append(
            Hymn(Number=hymn_number, Title=hymn.Title) # type: ignore
        )
    

    def save_hymns(self, path: str = LOCAL_DIR) -> None:
        """Save hymns to file."""
        with open(f'{path}/hosanna/services/{self.day}/hymns.txt', 'a') as f:
            for hymn in self._hymns:
                f.write(f'{hymn.Title}\nELW {hymn.Number}\n')
            f.close()


    @staticmethod
    def _get_hymn(
        hymn_number: int, 
        df: pd.DataFrame = DF
    ) -> object:
        """Get hymn by hymn number."""
        try:
            return df.loc[hymn_number]
        except KeyError:
            print(f'Hymn {hymn_number} not found.')
