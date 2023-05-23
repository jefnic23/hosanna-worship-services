from datetime import datetime
from tkinter import Tk, filedialog

import eel

from config import Settings, settings
from services.hymns import Hymns

hymns = Hymns()
# TODO: instantiate all services here


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
    print(settings.dict())
    
    
@eel.expose
def get_dir():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder = filedialog.askdirectory()
    return folder


@eel.expose
def set_date(date: str) -> None:
    hymns.day = datetime.strptime(date, '%Y-%m-%d').date()
    # TODO: set date for all services here
    print(hymns.day)


@eel.expose
def add_hymn(hymn_number: int) -> list[dict]:
    hymns.add_hymn(hymn_number)
    return [hymn.dict() for hymn in hymns._hymns]


def start_eel() -> None:
    '''Starts the Eel server.'''
    
    cmdline_args = [
        'brave-portable/brave-portable.exe', 
        '--app=http://localhost:8080/index.html'
    ]

    eel.init('web')
    eel.start(
        'index.html', 
        mode='custom',
        cmdline_args=cmdline_args,
        host='localhost',
        port=8080,
        size=(1600, 1200)
    )


if __name__ == '__main__':
    start_eel()
