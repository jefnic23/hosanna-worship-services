import os
from datetime import date

import pandas
import typer

from services.utils import get_sunday


def load_hymns() -> pandas.DataFrame:
    """Load hymns from csv file."""
    return pandas.read_csv('data/hymnal.csv', index_col='Hymn')


def get_hymn(hymn_number: int) -> object:
    """Get hymn by hymn number."""
    hymns = load_hymns()
    return hymns.loc[hymn_number]


def main():
    this_sunday = get_sunday(date.today())
    typer.echo(f'Welcome to Hosanna Worship Services for {this_sunday}')
    if not os.path.exists(f'services/{this_sunday}'):
        os.makedirs(f'services/{this_sunday}')
    hymns = []
    while True:
        hymn_number = typer.prompt('Enter hymn number')
        hymn = get_hymn(int(hymn_number))
        confirm = typer.confirm(
            f'{hymn["Title"]}\n\nIs this the hymn you want?'
        )
        if not confirm:
            continue
        hymns.append((hymn_number, hymn.Title))
        abort = typer.confirm('Another hymn?')
        if not abort:
            with open(f'services/{this_sunday}/hymns.txt', 'w') as f:
                for hymn in hymns:
                    f.write(f'{hymn[1]}\nELW {hymn[0]}\n')
                f.close()
            raise typer.Abort()


if __name__ == '__main__':
    typer.run(main)
