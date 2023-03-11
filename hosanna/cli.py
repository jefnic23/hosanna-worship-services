import os
from datetime import date, timedelta

import art
import typer

from hosanna import __app_name__, __author__, __version__
from hosanna.document import WordDocument
from hosanna.powerpoint import PowerPoint
from hosanna.sundaysandseasons import SundaysAndSeasons
from hosanna.utils import get_sunday

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f'{__app_name__} v{__version__}')
        raise typer.Exit()
    

@app.callback()
def main(
    version: bool = typer.Option(
        None,
        '--version',
        '-v',
        callback=_version_callback,
        is_eager=True,
        help='Show version and exit.',
    ),
):
    pass

if __name__ == '__main__':
    # TODO: prompt to install libreoffice if it doesn't exist
    # https://www.libreoffice.org/download/download-libreoffice/

    # TODO: prompt to add hymns if they don't exist

    TODAY = date.today()
    this_sunday = get_sunday(TODAY)

    # sas = SundaysAndSeasons(this_sunday)
    # sas.login()
    # sas.get_readings_and_slide()
    # sas.logoff()

    # if not os.path.exists(f'services/{this_sunday}'):
    #     os.makedirs(f'services/{this_sunday}')

    # with open(f'services/{this_sunday}/prayer.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.prayer)

    # with open(f'services/{this_sunday}/first-reading.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.first_reading)

    # with open(f'services/{this_sunday}/psalm.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.psalm)

    # with open(f'services/{this_sunday}/second-reading.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.second_reading)

    # with open(f'services/{this_sunday}/gospel.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.gospel)

    # with open(f'services/{this_sunday}/intercession.txt', 'w', encoding='utf-8') as f:
    #     f.write(f'{sas.intercession[0]}\n{sas.intercession[1]}')

    # ppt = PowerPoint(this_sunday)
    # ppt.add_image()
    # ppt.add_call_and_response('Confession and Forgiveness', ppt._confession)
    # ppt.add_hymn()
    # ppt.add_call_and_response('Greeting', ppt._greeting)
    # ppt.add_congregation_text('Kyrie', ppt._kyrie)
    # ppt.add_congregation_text('Prayer of the Day', ppt._prayer)
    # ppt.add_reading('First Reading', ppt._first_reading)
    # ppt.add_psalm()
    # ppt.add_reading('Second Reading', ppt._second_reading)
    # ppt.add_congregation_text('Gospel Acclamation', ppt._gospel_acclamation)
    # ppt.add_gospel()
    # ppt.add_title_slide('Sermon')
    # ppt.add_hymn()
    # ppt.add_congregation_text('Apostle\'s Creed', ppt._creed)
    # ppt.add_intercessions()
    # ppt.add_dialogue()
    # ppt.add_congregation_text('Holy, holy, holy', ppt._hosanna)
    # ppt.add_call_and_response('Communion Dialogue', ppt._communion_dialogue)
    # ppt.add_congregation_text('Lord\'s Prayer', ppt._lords_prayer)
    # ppt.add_title_slide('Communion')
    # ppt.add_congregation_text('Communion Hymn', ppt._communion_hymn)
    # ppt.add_call_and_response('Prayer after Communion', ppt._prayer_after_communion)
    # ppt.add_call_and_response('Benediction', ppt._benediction)
    # ppt.add_hymn()
    # ppt.add_call_and_response('Dismissal', ppt._dismissal)
    # ppt.add_image()
    # ppt.save()
    
    doc = WordDocument(this_sunday)
    doc.add_reading(doc._first_reading)
    doc.add_psalm(doc._psalm)
    doc.add_reading(doc._second_reading)
    doc.save()