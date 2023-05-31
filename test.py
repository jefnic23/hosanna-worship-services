import re

from bs4 import BeautifulSoup

from services.utils import (clean_text, get_superscripts, grouper,
                            split_formatted_text)

with open('data/test.html', 'rb') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

superscripts = [
    superscript.get_text() for superscript in soup.find_all('sup', {'class': None})
]
for i, s in enumerate(superscripts):
    if ':' in s:
        superscripts[i] = f'{s}{superscripts[i + 1]}'
        superscripts.pop(i + 1)

text = '\n'.join([clean_text(ele) for ele in soup.get_text().splitlines()])

# replace superscripts in text with <sup> tags
for s in superscripts:
    m = re.search(s, text)
    print(m, s)
    if m:
        text = text.replace(s, f'<sup>{s}</sup>')

# superscripts = re.findall(r'<sup>(.*?)</sup>', text)

# print(text)


# spans = [
#     clean_text(span.get_text()) 
#     for span in soup.find_all('span', {'class': None}) 
#     if 'style' not in span.attrs
# ]

# text = []
# for span in spans:
#     if span in superscripts:
#         text.append(f'<sup>{span}</sup>')
#     else:
#         text.append(span)

# text = '\n'.join([' '.join(line) for line in grouper(text, 3)])
# superscripts = re.findall(r'<sup>(.*?)</sup>', text)
# text = text.replace('<sup>', '').replace('</sup>', '')

# for i, line in enumerate(text.splitlines()):
#     print([(s.start(), s.end()) for s in re.finditer(superscripts[i], line)])
