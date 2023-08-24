import re

from boltons.iterutils import split
from bs4 import BeautifulSoup

from models.reading import Reading
from services.utils import clean_text


def _get_superscripts(soup: BeautifulSoup) -> list[str]:
    '''Get the superscripts in a soup object'''
    superscripts = [
        s.get_text() for s in soup.find_all('sup', {'class': None})
    ]
    
    for i, s in enumerate(superscripts):
        if ':' in s:
            superscripts[i] = f'{s}{superscripts[i + 1]}'
            superscripts.pop(i + 1)
            
    return superscripts

def _add_superscripts(text: str, superscripts: list) -> str:
    """Finds the superscripts in a text string and surrounds them with the html 
    superscript tag, which is later used to format the text in the powerpoint slides.

    Args:
        text (str): The line of text to search for superscripts.
        superscripts (list): The list of superscripts to search for.

    Returns:
        str: The original text with <sup></sup> tags surrounding the superscripts.
    """
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

def _remove_whitespace(text: str) -> str:
    '''Remove whitespace between superscripts and text'''
    return re.sub(r'(?<=<\/sup>)\s+', '', text)

###############################

with open('test.html', 'rb') as f:
    psalm = BeautifulSoup(f.read(), 'html.parser')


for br in psalm.find_all('br'):
    br.replace_with('\n')
superscripts = _get_superscripts(psalm)
text = _add_superscripts(
    '\n'.join([
        clean_text(span.get_text())
        for span in psalm.find_all('span', {'class': None}) 
        if span.get_text() and 'style' not in span.attrs 
    ]),
    superscripts
)

bold_text = [clean_text(strong.get_text()) for strong in psalm.find_all('strong')]
formatted_text = []
for i, line in enumerate(text.splitlines()):
    if line.replace('<sup>', '').replace('</sup>', '') in superscripts:
        try:
            if text.splitlines()[i+1] in bold_text or text.splitlines()[i-1] in bold_text and i != 0:
                formatted_text.append(None)
        except IndexError:
            pass
        formatted_text.append(line) 
    else:
        formatted_text.append(line)

body = []
for i, line in enumerate(split(formatted_text, lambda x: x is None)):
    if line:
        new_line = _remove_whitespace(f"{line[0]}{' '.join(line[1:])}")
        if i % 2 == 0:
            body.append(new_line)
        else:
            body.append(f"<b>{new_line}</b>")

reading = Reading(
    title = "Psalm",
    body = '\n'.join(body)
)

print(reading.title, reading.body)