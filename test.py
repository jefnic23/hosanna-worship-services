import re

from boltons.iterutils import split
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from models.reading import Reading
from services.powerpoint import PowerPoint
from services.sundaysandseasons import SundaysAndSeasons
from services.utils import clean_text, split_formatted_text

###############################

MAX_WIDTH: int = 565
MAX_HEIGHT: int = 335

REGULAR: FreeTypeFont = ImageFont.truetype('%SystemRoot%\Fonts\segoeui.ttf', 24)
BOLD: FreeTypeFont = ImageFont.truetype('%SystemRoot%\Fonts\segoeuib.ttf', 24)
ITALIC: FreeTypeFont = ImageFont.truetype('%SystemRoot%\Fonts\segoeuii.ttf', 24)
DRAW: ImageDraw.ImageDraw = ImageDraw.Draw(Image.new('RGB', (MAX_WIDTH, MAX_HEIGHT)))

# def get_height(
#     lines: str, 
#     draw: ImageDraw.ImageDraw, 
#     font: FreeTypeFont, 
#     max_height: int = MAX_HEIGHT
# ) -> list[str]:
#     '''Gets the height of a line of text and splits it if it's too long.'''
#     if PowerPoint.check_size(lines, draw, font)['height'] < max_height:
#         return [lines]

#     regex = re.search(r'<div>(.*?)</div>', lines, re.MULTILINE | re.DOTALL)
#     group = regex.group(1).strip().splitlines() if regex else None
#     slides = []
#     for line in lines.splitlines():
#         if re.match(r'<br>', line):
#             # If the line is a break, insert a new slide
#             slides += ['']
#             continue

#         if re.match(r'<div>', line) or re.match(r'</div>', line):
#             continue

#         height = PowerPoint.check_size(
#             '\n'.join(slides[-1:] + [line]), 
#             draw, 
#             font
#         )['height']
        
#         if regex is not None and line == group[0]:
#             # check if the call and response will fit on the current slide
#             height = PowerPoint.check_size(
#                 '\n'.join(slides[-1:] + [line] + [group[1]]),
#                 draw,
#                 font
#             )['height']
#             if height > max_height:
#                 slides += [line]
#             else:
#                 slides[-1:] = ['\n'.join(slides[-1:] + [line])]
#             continue

#         if height < max_height:
#             slides[-1:] = ['\n'.join(slides[-1:] + [line]).lstrip()]
#         else:
#             slides += [line]
#     return slides

def get_height(
    lines: str, 
    draw: ImageDraw.ImageDraw, 
    font: ImageFont.FreeTypeFont, 
    max_height: int = MAX_HEIGHT
) -> list[str]:
    '''Gets the height of a line of text and splits it if it's too long.'''
    if PowerPoint.check_size(lines, draw, font)['height'] < max_height:
        return [lines]

    # Split the input lines into chunks separated by '<div>' and '</div>'
    chunks = re.split(r'(<div>.*?</div>)', lines)
    
    # Initialize the list of slides
    slides = ['']
    
    for chunk in chunks:
        # Skip empty chunks
        if not chunk:
            continue
        
        if chunk.startswith('<div>'):
            # If it's a '<div>' tag, remove the tags and add it to the current slide
            slide_text = chunk[len('<div>'):-len('</div>')].replace('<div>', '').replace('</div>', '').strip() 
            slides[-1] += slide_text
        else:
            # If it's not a '<div>' tag, split it by line breaks
            chunk_lines = chunk.strip().splitlines()
            for line in chunk_lines:
                line = line.replace('<div>', '').replace('</div>', '').strip()  # Remove leading and trailing whitespace
                if PowerPoint.check_size('\n'.join([slides[-1], line]), draw, font)['height'] < max_height:
                    slides[-1] += '\n' + line
                else:
                    slides.append(line)
    
    return slides

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

text = reading.body

superscripts = re.findall(r'<sup>(.*?)</sup>', text)
regular_text, bold_text, italic_text = split_formatted_text(text.replace('<sup>', '').replace('</sup>', ''))
bold_lines = [line[1] for line in bold_text]
italic_lines = [line[1] for line in italic_text]
lines = [
    line[1] for line in sorted(regular_text + bold_text + italic_text, key=lambda x: x[0])
]
width_formatted_text = []
bold_formatted_text = []
italic_formatted_text = []
for line in lines:
    if line in bold_lines:
        bold_line = PowerPoint.get_width(line, DRAW, BOLD)
        width_formatted_text.append(bold_line)
        for l in bold_line.splitlines():
            bold_formatted_text.append(l)
    elif line in italic_lines:
        italic_line = PowerPoint.get_width(line, DRAW, ITALIC)
        width_formatted_text.append(italic_line)
        for l in italic_line.splitlines():
            italic_formatted_text.append(l)
    else:
        width_formatted_text.append(PowerPoint.get_width(line, DRAW, REGULAR))

width_formatted_text = '\n'.join(width_formatted_text)

slides = get_height(width_formatted_text, DRAW, REGULAR)

for slide in slides:
    print(slide)

