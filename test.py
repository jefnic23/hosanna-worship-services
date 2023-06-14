from bs4 import BeautifulSoup

from config import Settings
from models.reading import Reading
from services.document import WordDocument
from services.utils import clean_text

with open('test.html', 'rb') as f:
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


superscripts = get_superscripts(soup)
for br in soup.find_all('br'):
    br.replace_with('\n')
text = add_superscripts_to_text(
    '\n'.join([clean_text(ele) for ele in soup.get_text().splitlines() if ele]),
    superscripts
)

print(text)