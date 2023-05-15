from datetime import date

import pandas

from config import settings
from models.hymn import Hymn


class Hymns:
    """Class for adding hymns to the service."""


    LOCAL_DIR = settings.LOCAL_DIR
    DF = pandas.read_csv('data/hymnal.csv', index_col='Hymn')


    def __init__(self, day: date) -> None:
        self.day: date = day
        self.hymns: list[Hymn] = []
    

    def add_hymn(self, hymn_number: int) -> None:
        """Add hymn to service."""
        hymn = Hymns.get_hymn(hymn_number)
        self.hymns.append(Hymn(Number=hymn_number, Title=hymn.Title))
    

    def save_hymns(self, path: str = LOCAL_DIR) -> None:
        """Save hymns to file."""
        with open(f'{path}/services/{self.day}/hymns.txt', 'a') as f:
            for hymn in self.hymns:
                f.write(f'{hymn.Title}\nELW {hymn.Number}\n')
            f.close()


    @staticmethod
    def get_hymn(
        hymn_number: int, 
        df: pandas.DataFrame = DF
    ) -> object:
        """Get hymn by hymn number."""
        return df.loc[hymn_number]
