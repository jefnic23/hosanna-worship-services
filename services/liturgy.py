import os
from pathlib import Path


class Liturgy():
    '''Loads and stores the liturgy.'''

    DIR: str = 'D:/Documents/Hosanna/liturgy'


    def __init__(self, season: str):
        self._season = season
        self._files = Liturgy._open_files(season)


    @staticmethod
    def _open_files(season: str, dir: str = DIR):
        '''Open all the liturgy files.'''
        path = Path(dir, season)
        files = {}
        for file in os.listdir(path):
            if file.endswith('.txt'):
                files[Path(file).stem] = open(
                    f'{path}/{file}', 
                    'r', 
                    encoding='utf-8'
                ).read()
        return files
    

    def __getattr__(self, name):
        '''Return the liturgy file.'''
        if name in self._files:
            return self._files[name]
        raise AttributeError(f'{name} not found')
