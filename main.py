import os
from datetime import datetime
from tkinter import Tk, filedialog

import eel

from services.document import WordDocument
from services.dropbox import Dropbox
from services.hymns import Hymns
from services.liturgy import Liturgy
from services.powerpoint import PowerPoint
from services.settings import Settings
from services.sundaysandseasons import SundaysAndSeasons

settings = Settings()
doc = WordDocument(settings)
dbx = Dropbox(settings)
hymns = Hymns(settings)
lit = Liturgy(settings)
ppt = PowerPoint(settings)
sas = SundaysAndSeasons(settings)


@eel.expose
def print_something(x: str) -> None:
    print(x)


@eel.expose
def get_settings() -> dict:
    '''Get all settings.'''
    return settings.dict()


@eel.expose
def update_settings(new_settings: dict) -> None:
    '''Update settings.'''
    is_valid = Settings(**new_settings)
    if not is_valid:
        print(is_valid.errors())
    settings.update_settings(new_settings)
    settings.save_settings()


@eel.expose
def list_liturgies() -> list[str]:
    '''List all liturgies.'''
    if not os.path.exists(f'{settings.LOCAL_DIR}/liturgy'):
        os.mkdir(f'{settings.LOCAL_DIR}/liturgy')

    return [
        dir for dir in os.listdir(f'{settings.LOCAL_DIR}/liturgy') 
        if os.path.isdir(f'{settings.LOCAL_DIR}/liturgy/{dir}') 
    ]

    
@eel.expose
def get_dir():
    '''Get directory for file storage.'''
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder = filedialog.askdirectory(initialdir=settings.LOCAL_DIR)
    return folder


@eel.expose
def set_date(date: str) -> None:
    '''Set date for all services.'''
    day = datetime.strptime(date, '%Y-%m-%d').date()

    doc.day = day
    dbx.day = day
    hymns.day = day
    ppt.day = day
    sas.day = day


@eel.expose
def add_hymn(hymn_number: int) -> list[dict]:
    '''Add a hymn to the list of hymns.'''
    hymns.add_hymn(hymn_number)
    return [hymn.dict() for hymn in hymns._hymns]


def start_eel(develop: bool) -> None:
    '''Starts the Eel server.'''

    if develop:
        directory = 'ui/src'
        app = None
        page = {'port': 8080}
    else:
        directory = 'web'
        app = 'chrome'
        page = 'index.html'

    eel_kwargs = dict(
        app_mode=True,
        host='localhost',
        port=8080,
        size=(1600, 1200)
    )

    eel.init(directory, ['.ts', '.js', '.html'])
    eel.start(
        page = page, 
        mode = app,
        **eel_kwargs
    )


if __name__ == '__main__':
    import sys

    start_eel(develop = '--develop' in sys.argv)
