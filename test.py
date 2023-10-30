import re

from boltons.iterutils import split
from bs4 import BeautifulSoup

from models.reading import Reading
from services.sundaysandseasons import SundaysAndSeasons
from services.utils import clean_text

###############################

with open('test.html', 'rb') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

regex = re.compile(r'Psalm:')

parent = soup.find('h3', string=regex)
title = parent.get_text().split('Psalm: ')[1]
psalm = parent.find_next_sibling().find_next_sibling()

for br in psalm.find_all('br'):
    br.replace_with('\n')
superscripts = SundaysAndSeasons._get_superscripts(psalm)
text = SundaysAndSeasons._add_superscripts(
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
        new_line = SundaysAndSeasons._remove_whitespace(f"{line[0]}{' '.join(line[1:])}")
        if i % 2 == 0:
            body.append(f'<div>{new_line}</div>')
        else:
            body.append(f'<div><b>{new_line}</b></div>')

reading = Reading(
    title = title,
    body = '\n'.join(body)
)

for line in body:
    print(line)