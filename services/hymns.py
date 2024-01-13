from datetime import date

import pandas as pd

from models.hymn import Hymn
from services.settings import Settings


class Hymns:
    """Class for adding hymns to the service."""

    DF = pd.read_csv('data/hymnal.csv')


    def __init__(self, settings: Settings) -> None:
        self.day: date = date.today()
        self._path: str = f'{settings.LOCAL_DIR}/services'
        self._hymns: list[Hymn] = []
    

    def add_hymn(self, hymn_number: int) -> Hymn:
        """Add hymn to service."""
        self._hymns.append(hymn := Hymns.lookup_hymn(hymn_number))
        return hymn
    
    
    def add_other_hymn(
        self,
        hymn_number: int,
        hymn_title: str,
        hymnal: str
    ) -> Hymn:
        self._hymns.append(hymn := Hymn(title=f'({hymnal}) {hymn_title}', number=hymn_number))
        return hymn
    
    
    def get_hymn(self, index: int) -> Hymn:
        """
        Get hymn by index.
        
        Returns
        -------
            Hymn: the requested hymn.
        """
        if index > len(self._hymns) or index < 1:
            raise IndexError(f"Please enter a number between 1 and {len(self._hymns)}")
        return self._hymns[index - 1]


    @staticmethod
    def lookup_hymn(
        hymn_number: int, 
        df: pd.DataFrame = DF
    ) -> Hymn:
        """
        Lookup hymn in hymnal.

        Args
        -------
            hymn_number (int) : the ELW hymn number.
            df (pd.DataFrame, optional) : the pandas DataFrame where the hymns are located. Defaults to DF.

        Returns
        -------
            Hymn : the title and number of the hymn.
        """
        try:
            return Hymn(**df.loc[df['number'] == hymn_number].to_dict('records')[0])
        except KeyError:
            print(f'Hymn {hymn_number} not found.')
