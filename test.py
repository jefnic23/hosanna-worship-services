import re

from bs4 import BeautifulSoup

from services.utils import (clean_text, get_superscripts, grouper,
                            split_formatted_text)

with open('data/test.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

superscripts = [
    superscript.get_text() for superscript in soup.find_all('sup', {'class': None})
]

spans = [
    clean_text(span.get_text()) 
    for span in soup.find_all('span', {'class': None}) 
    if 'style' not in span.attrs
]

text = []
for span in spans:
    if span in superscripts:
        text.append(f'<sup>{span}</sup>')
    else:
        text.append(span)

text = '\n'.join([' '.join(line) for line in grouper(text, 3)])
superscripts = re.findall(r'<sup>(.*?)</sup>', text)
text = text.replace('<sup>', '').replace('</sup>', '')

for i, sup in enumerate(superscripts):
    print([(s.start(), s.end()) for s in re.finditer(sup, text.splitlines()[i])])

# for span in spans:
#     print(f'<sup>{span}<sup>' if f'<sup>{span}<sup>' in superscripts else '')

# print('\n'.join([' '.join(line) for line in grouper(text, 3)]))
