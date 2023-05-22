from datetime import date

import pandas
import redis
import csv

from config import settings
from models.hymn import Hymn


class Hymns:
    """Class for adding hymns to the service."""


    LOCAL_DIR = settings.LOCAL_DIR
    DF = pandas.read_csv('data/hymnal.csv', index_col='Hymn')
    R = redis.Redis()


    def __init__(self) -> None:
        self.day: date = date.today()
        self._hymns: list[Hymn] = []
        
        self._load_hymns()
    

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
            
            
    def _load_hymns(self) -> None:
        with open('data/hymnal.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.R.set(row['Hymn'], row['Title'])


    @staticmethod
    def _get_hymn(
        hymn_number: int, 
        r: redis.Redis = R
    ) -> object:
        """Get hymn by hymn number."""
        try:
            return r.get(str(hymn_number))
        except KeyError:
            print(f'Hymn {hymn_number} not found.')
