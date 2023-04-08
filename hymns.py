import pandas
import typer


def load_hymns() -> pandas.DataFrame:
    """Load hymns from csv file."""
    return pandas.read_csv('data/hymnal.csv', index_col='Hymn')


def get_hymn(hymn_number: int) -> object:
    """Get hymn by hymn number."""
    hymns = load_hymns()
    return hymns.loc[hymn_number]


def main():
    while True:
        hymn_number = typer.prompt('Enter hymn number')
        hymn = get_hymn(int(hymn_number))
        print(f'{hymn["Title"]}\nELW {hymn_number}')
        typer.confirm('Another hymn?', abort=True)


if __name__ == '__main__':
    typer.run(main)
