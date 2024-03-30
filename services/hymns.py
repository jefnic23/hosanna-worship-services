from datetime import date

import pandas as pd

from models.hymn import Hymn
from services.settings import Settings


class Hymns:
    """Class for adding hymns to the service."""


    def __init__(self, settings: Settings) -> None:
        self.day: date = date.today()
        self._path: str = f'{settings.LOCAL_DIR}/services'
        self._df: pd.DataFrame = pd.read_csv('data/hymnal.csv')
    
    
    def get_hymn(self, hymn_number: int) -> Hymn:
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
            return Hymn(**self._df.loc[self._df['number'] == hymn_number].to_dict('records')[0])
        except KeyError:
            print(f'Hymn {hymn_number} not found.')
    

    def get_other_hymn(
        self,
        hymn_number: int,
        hymn_title: str,
        hymnal: str
    ) -> Hymn:
        return Hymn(title=f'({hymnal}) {hymn_title}', number=hymn_number)
