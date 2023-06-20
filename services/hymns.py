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
    
    
    def get_hymns(self) -> list[Hymn]:
        """Get list of hymns.
        
        Returns:
            list[Hymn]: the list of hymns.
        """
        return self._hymns


    @staticmethod
    def lookup_hymn(
        hymn_number: int, 
        df: pd.DataFrame = DF
    ) -> Hymn:
        """Lookup hymn in hymnal.

        Args:
            hymn_number (int): the ELW hymn number.
            df (pd.DataFrame, optional): the pandas DataFrame where the hymns are located. Defaults to DF.

        Returns:
            Hymn: the title and number of the hymn.
        """
        try:
            return Hymn(**df.loc[df['number'] == hymn_number].to_dict('records')[0])
        except KeyError:
            print(f'Hymn {hymn_number} not found.')
