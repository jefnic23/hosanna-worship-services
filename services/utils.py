import calendar
import os
import re
from datetime import date, timedelta
from distutils.spawn import find_executable
from itertools import chain, pairwise, zip_longest
from typing import Iterable


def point_to_px(point: int) -> int:
    '''Converts a point size to a pixel size.'''
    return int(point * 96 / 72)


def inch_to_px(inch: int) -> int:
    '''Converts an inch size to a pixel size.'''
    return int(inch * 96)


def grouper(
    iterable: Iterable, 
    n: int, 
    fillvalue = None
) -> list[tuple]:
    '''Collect data into fixed-length groups.'''
    args = [iter(iterable)] * n
    return list(zip_longest(*args, fillvalue=fillvalue))


def get_parts(x: str, y: str) -> list[tuple]:
    '''Gets the start and end of each part of the liturgy.'''
    xy = pairwise(list(chain.from_iterable(zip(x, y))))
    return grouper(xy, 2)


def split_formatted_text(
    text: str
) -> tuple[list[tuple[int, str]], list[tuple[int, str]], list[tuple[int, str]]]:
    '''Splits a file into regular and bold text.'''
    bold_text: list[tuple[int, str]] = []
    italic_text: list[tuple[int, str]] = []
    regular_text: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines()):
        if re.match(r'<b>.*</b>', line):
            bold_text.append((
                line_number,
                line.replace('<b>', '').replace('</b>', '').strip()
            ))
        elif re.match(r'<i>.*</i>', line):
            italic_text.append((
                line_number, 
                line.replace('<i>', '').replace('</i>', '').strip()
            ))
        else:
            regular_text.append((line_number, line.strip()))
    return regular_text, bold_text, italic_text


def lookahead(iterable: Iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    for val in it:
        # Report the *previous* value (more to come).
        yield last, True
        last = val
    # Report the last value.
    yield last, False


def get_superscripts(
    superscripts: list[str],
    line: str
) -> list[tuple[int, int]]:
    """Gets the superscripts in a line of text.

    Args:
        superscripts (list[str]): List of superscripts to find.
        line (str): The line of text to search.

    Returns:
        list[tuple[int, int]]: List of tuples containing the start and end index of each superscript.
    """
    sups: re.Pattern = re.compile('|'.join(superscripts))
    superscripts_in_line = []
    if len(superscripts) != 0:
        for m in sups.finditer(line):
            superscripts_in_line.append((m.start(), m.end()))
    # for superscript in superscripts:
    #     for s in re.finditer(superscript, line):
            # if not any (s.start() < sup[1] for sup in superscripts_in_line):
                # superscripts_in_line.append((s.start(), s.end()))
    return superscripts_in_line
    

def clean_text(text: str) -> str:
    '''Normalizes text.'''
    cleaned = (
        text.encode('utf-8', errors='ignore').decode()
        .replace(' | ', ' ').replace('- ', '').replace('  ', ' ')
        .strip()
    )
    return cleaned[:-1].strip() if cleaned.endswith('R') else cleaned 


def exe_exists(exe: str) -> bool:
    '''Checks if an executable exists.'''
    return find_executable(exe) is not None


def create_directory(path: str) -> None:
    '''Creates a directory if it does not exist.'''
    if not os.path.exists(path):
        os.makedirs(path)


def get_sunday(delta: int = 0) -> date:
    '''Gets the date of the next Sunday.'''
    TODAY: date = date.today()
    SUNDAY: int = calendar.SUNDAY
    return TODAY + timedelta((SUNDAY - TODAY.weekday()) % 7) + timedelta(weeks=delta)
