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
hymns = Hymns()
lit = Liturgy(settings)
ppt = PowerPoint(settings)
sas = SundaysAndSeasons(settings)


@eel.expose
def print_something(x: str) -> None:
    print(x)


@eel.expose
def get_settings() -> dict:
    """Get all settings."""
    return settings.dict()


@eel.expose
def update_settings(new_settings: dict) -> None:
    """Update settings."""
    is_valid = Settings(**new_settings)
    if not is_valid:
        print(is_valid.errors())
    settings.update_settings(new_settings)
    settings.save_settings()


@eel.expose
def list_liturgies() -> list[str]:
    """List all liturgies."""
    return lit.list_seasons()


@eel.expose
def list_liturgical_files(season: str) -> list[str]:
    lit.load_files(season)
    return lit.list_files(season)


@eel.expose
def get_liturgical_file(filename: str) -> str:
    return lit.get_file(filename)


@eel.expose
def set_dir() -> str:
    """Set directory for file storage."""
    root = Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    folder = filedialog.askdirectory(initialdir=settings.LOCAL_DIR)
    return folder


@eel.expose
def set_date(date: str) -> None:
    """
    Sets the date for each service.

    Parameters
    ----------
    date : str
        date string in the format YYYY-MM-DD
    """
    day = datetime.strptime(date, "%Y-%m-%d").date()

    dbx.day = day
    doc.day = day
    ppt.day = day
    sas.day = day


@eel.expose
def get_hymn(hymn_number: int) -> dict[str, str]:
    """Adds a hymn to the service.

    Args
    -------
        hymn_number (int) : ELW hymn number.

    Returns
    -------
        dict[str, str] : dict representation of hymn containing the hymn number and title.
    """
    return hymns.get_hymn(hymn_number).dict()


if __name__ == "__main__":
    directory = "web"
    eel.init(directory, [".ts", ".js", ".html"])

    eel_kwargs = dict(
        mode="portable",
        app_mode=True,
        host="localhost",
        port=8080,
        size=(1600, 1200)
    )
    eel.start("index.html", **eel_kwargs)
