import re

from boltons.iterutils import split
from bs4 import BeautifulSoup

from config import Settings
from services.powerpoint import PowerPoint
from services.utils import clean_text

with open('data/test.html', 'rb') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')


def get_superscripts(soup: BeautifulSoup) -> list[str]:
    '''Get the superscripts in a soup object'''
    superscripts = [
        s.get_text() for s in soup.find_all('sup', {'class': None})
    ]
    
    for i, s in enumerate(superscripts):
        if ':' in s:
            superscripts[i] = f'{s}{superscripts[i + 1]}'
            superscripts.pop(i + 1)
            
    return superscripts


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


bold_text = [clean_text(span.get_text()) for span in soup.find_all('strong')]
superscripts = get_superscripts(soup)
text = add_superscripts_to_text(
    '\n'.join([
        clean_text(span.get_text())
        for span in soup.find_all('span', {'class': None})
        if 'style' not in span.attrs 
    ]),
    superscripts
)

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

psalm = ''
for i, line in enumerate(split(formatted_text, lambda x: x is None)):
    if i % 2 == 0:
        psalm += f"{line[0]}{' '.join(line[1:])}"
    else:
        psalm += f"<b>{line[0]}{' '.join(line[1:])}</b>"
        
print(psalm)

# settings = Settings()
# ppt = PowerPoint(settings)
