import calendar
import os
import re
from datetime import date, timedelta
from distutils.spawn import find_executable
from itertools import chain, tee, zip_longest
from typing import Iterable


def point_to_px(point: int) -> int:
    '''Converts a point size to a pixel size.'''
    return int(point * 96 / 72)


def inch_to_px(inch: int) -> int:
    '''Converts an inch size to a pixel size.'''
    return int(inch * 96)


def pairwise(iterable: Iterable) -> list[tuple]:
    '''s -> (s0,s1), (s1,s2), (s2, s3), ...'''
    a, b = tee(iterable)
    next(b, None)
    return list(zip(a, b))


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


def split_regular_bold_text(
    text: str
) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    '''Splits a file into regular and bold text.'''
    regular_text = []
    bold_text = []
    line_number = 0
    for line in text.splitlines():
        if re.match(r'<b>.*</b>', line):
            bold_text.append((
                line_number,
                line.replace('<b>', '').replace('</b>', '').strip()
            ))
        else:
            regular_text.append((line_number, line.strip()))
        line_number += 1
    return regular_text, bold_text


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


def get_superscripts(text: str) -> list[tuple[int, int]]:
    '''Gets the superscripts in a string.'''
    # TODO: some superscripts have lower case letters, which are not captured
    return [(s.start(), s.end()) for s in re.finditer(r'(\d+:\d+)|\d+', text)]
    

def clean_text(text: str) -> str:
    '''Normalizes text.'''
    cleaned = (
        text.encode('utf-8').decode()
        .replace(' | ', ' ').replace('- ', '').replace('  ', ' ')
        .strip()
    )
    return cleaned[:-1] if cleaned.endswith('R') else cleaned 


def get_sunday(
    today: date = date.today(), 
    delta: int = 0
) -> date:
    '''Gets the date of the next Sunday.'''
    SUNDAY = calendar.SUNDAY
    return today + timedelta((SUNDAY - today.weekday()) % 7) + timedelta(weeks=delta)


def exe_exists(exe: str) -> bool:
    '''Checks if an executable exists.'''
    return find_executable(exe) is not None


def create_directory(path: str) -> None:
    '''Creates a directory if it does not exist.'''
    if not os.path.exists(path):
        os.makedirs(path)
