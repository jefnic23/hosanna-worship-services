from datetime import date

import pandas as pd

from models.hymn import Hymn
from services.settings import Settings


class Hymns:
    """Class for adding hymns to the service."""

    DF = pd.read_csv('data/hymnal.csv', index_col='Number')


    def __init__(self, settings: Settings) -> None:
        self.day: date = date.today()
        self._path: str = f'{settings.LOCAL_DIR}/services'
        self._hymns: list[Hymn] = []
    

    def add_hymn(self, hymn_number: int) -> Hymn:
        """Add hymn to service."""
        hymn = Hymns._get_hymn(hymn_number)
        new_hymn = Hymn(title=hymn['Title'], number=f'ELW {hymn_number}')
        self._hymns.append(new_hymn)
        return new_hymn


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
