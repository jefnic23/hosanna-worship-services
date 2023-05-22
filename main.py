from datetime import datetime

import eel
from config import settings

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
        size=(1280, 720)
    )


if __name__ == '__main__':
    start_eel()
