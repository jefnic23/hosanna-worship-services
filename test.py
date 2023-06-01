import re

from bs4 import BeautifulSoup
import bs4

from services.utils import (clean_text, get_superscripts, grouper,
                            split_formatted_text)

with open('data/test.html', 'rb') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')


# get superscripts from soup
superscripts = [
    superscript.get_text() for superscript in soup.find_all('sup', {'class': None})
]
for i, s in enumerate(superscripts):
    if ':' in s:
        superscripts[i] = f'{s}{superscripts[i + 1]}'
        superscripts.pop(i + 1)

# get text from soup
text = '\n'.join([clean_text(ele) for ele in soup.get_text().splitlines()])

def find_superscript(text: str, superscript: str, start: int = 0):
    '''Find the start and end index of a superscript in a string'''
    length = len(superscript)
    index = text.find(superscript, start)
    return index, index + length


def add_superscripts_to_text(text: str, superscripts: list) -> str:
    def find_superscript(text: str, superscript: str, start: int = 0):
        '''Find the start and end index of a superscript in a string'''
        length = len(superscript)
        index = text.find(superscript, start)
        return index, index + length

    start = 0
    new_text = ""
    for superscript in superscripts:
        indeces = find_superscript(text, superscript, start)
        new_text += text[start:indeces[0]] + f'<sup>{superscript}</sup>'
        start = indeces[1]
    new_text += text[start:]
    return new_text

print(add_superscripts_to_text(text, superscripts))

