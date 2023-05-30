from bs4 import BeautifulSoup
from services.utils import clean_text, grouper, get_superscripts, split_formatted_text

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
r, b, i, s = split_formatted_text(text)
superscript_lines = [line[1] for line in s]
print(superscript_lines)

# for span in spans:
#     print(f'<sup>{span}<sup>' if f'<sup>{span}<sup>' in superscripts else '')

# print('\n'.join([' '.join(line) for line in grouper(text, 3)]))
