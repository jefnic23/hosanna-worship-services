import re
from itertools import chain, tee, zip_longest
from unicodedata import normalize
from PIL import Image, ImageDraw, ImageFont

MAX_WIDTH = 565
MAX_HEIGHT = 335


regular = ImageFont.truetype('%SystemRoot%\Fonts\segoeui.ttf', 24)
bold = ImageFont.truetype('%SystemRoot%\Fonts\segoeuib.ttf', 24)
draw = ImageDraw.Draw(Image.new('RGB', (MAX_WIDTH, MAX_HEIGHT)))


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


def get_parts(x, y):
    '''Gets the start and end of each part of the liturgy'''
    xy = pairwise(list(chain.from_iterable(zip(x, y))))
    return grouper(xy, 2)


def lookahead(iterable):
    """Pass through all values from the given iterable, augmented by the
    information if there are more values to come after the current one
    (True), or if it is the last value (False).
    """
    # Get an iterator and pull the first value.
    it = iter(iterable)
    last = next(it)
    # Run the iterator to exhaustion (starting from the second value).
    for val in it:
        # Report the *previous* value (more to come).
        yield last, True
        last = val
    # Report the last value.
    yield last, False


def get_superscripts(text):
    start, end = 0, len(text)
    superscripts = [[start]] + [[s.start(), s.end()] for s in re.finditer(r'(\d+:\d+)|\d+', text)] + [[end]]
    return list(chain(*superscripts))
    

def clean_text(text):
    cleaned = text.encode('utf-8').decode().replace(' | ', ' ').replace('- ', '').replace('  ', ' ').strip()
    return cleaned[:-1] if cleaned.endswith('R') else cleaned 
