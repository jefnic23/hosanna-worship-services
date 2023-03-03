import re
from itertools import chain, tee, zip_longest

from PIL import Image, ImageDraw, ImageFont

MAX_WIDTH = 566
MAX_HEIGHT = 336


regular = ImageFont.truetype('%SystemRoot%\Fonts\segoeui.ttf', 24)
bold = ImageFont.truetype('%SystemRoot%\Fonts\segoeuib.ttf', 24)
draw = ImageDraw.Draw(Image.new('RGB', (MAX_WIDTH, MAX_HEIGHT)))


with open('liturgy/confession.txt', 'r', encoding='utf-8') as f:
    confession = f.read()


pastor = [p.start() for p in re.finditer(r'P:', confession)]
congregation = [c.start() for c in re.finditer(r'C:', confession)]



def point_to_px(point):
    '''Converts a point size to a pixel size'''
    return int(point * 96 / 72)


def inch_to_px(inch):
    '''Converts an inch size to a pixel size'''
    return int(inch * 96)


def check_size(draw, line, font):
    '''Checks the size of a line of text'''
    size = draw.multiline_textbbox((0, 0), line, font)
    return {'width': size[2], 'height': size[3]}


def get_width(line, draw, font, max_width=MAX_WIDTH):
    '''Gets the width of a line of text and splits it if it's too long'''
    if check_size(draw, line, font)['width'] < max_width:
        return line
    else:
        lines = []
        for word in line.split():
            if check_size(draw, ' '.join(lines[-1:] + [word]), font)['width'] < max_width:
                lines[-1:] = [' '.join(lines[-1:] + [word])]
            else:
                lines += [word]

        return '\n'.join(lines)
    

def get_height(lines, draw, font, max_height=MAX_HEIGHT):
    '''Gets the height of a line of text and splits it if it's too long'''
    if check_size(draw, lines, font)['height'] < max_height:
        return [lines]
    else:
        slides = []
        for line in lines.splitlines():
            if check_size(draw, '\n'.join(slides[-1:] + [line]), font)['height'] < max_height:
                slides[-1:] = ['\n'.join(slides[-1:] + [line])]
            else:
                slides += [line]

        return slides
    

def get_slides(lines, draw, regular=regular):
    width_formatted_text = []
    for line in lines.splitlines():
        width_formatted_text.append(get_width(line, draw, regular))
    width_formatted_text = '\n'.join(width_formatted_text)

    return get_height(width_formatted_text, draw, regular)


def pairwise(iterable):
    '''s -> (s0,s1), (s1,s2), (s2, s3), ...'''
    a, b = tee(iterable)
    next(b, None)
    return list(zip(a, b))


def grouper(iterable, n, fillvalue=None):
    '''Collect data into fixed-length chunks or blocks'''
    args = [iter(iterable)] * n
    return list(zip_longest(*args, fillvalue=fillvalue))


def get_parts(pastor, congregation):
    '''Gets the start and end of each part of the liturgy'''
    parts = pairwise(list(chain.from_iterable(zip(pastor, congregation))))
    return grouper(parts, 2)
    

if __name__ == '__main__':
    # print(second_part)
    # print(get_slides(second_part, draw, regular))

    # first_part = content_text[:parts[1]].strip()
    # second_part = content_text[parts[1]:parts[2]].strip()
    # third_part = content_text[parts[2]:].strip()

    for part in get_parts(pastor, congregation):
        if part[1] is None:
            p, c = confession[part[0][0]:part[0][1]].strip(), confession[part[0][1]:].strip()
        else:
            p, c = confession[part[0][0]:part[0][1]].strip(), confession[part[1][0]:part[1][1]].strip()
            
        width_formatted_text = []
        for line in p.splitlines():
            width_formatted_text.append(get_width(line, draw, regular))
            
        for line in c.splitlines():
            width_formatted_text.append(get_width(line, draw, bold))

        width_formatted_text = '\n'.join(width_formatted_text)

        slides = get_height(width_formatted_text, draw, regular)

        for slide in slides:
            for line in slide.splitlines():
                print(line in p, line in c)
