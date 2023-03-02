import re
from PIL import Image, ImageFont, ImageDraw

MAX_WIDTH = 566
MAX_HEIGHT = 331

regular = ImageFont.truetype('%SystemRoot%\Fonts\segoeui.ttf', 24)
bold = ImageFont.truetype('%SystemRoot%\Fonts\segoeuib.ttf', 24)
draw = ImageDraw.Draw(Image.new('RGB', (MAX_WIDTH, MAX_HEIGHT)))

with open('liturgy/confession.txt', 'r', encoding='utf-8') as f:
        confession = f.read()

parts = [p.start() for p in re.finditer(r'P:', confession)]
first_part = confession[:parts[1]].strip()
second_part = confession[parts[1]:parts[2]].strip()


def check_size(draw, line, font):
    return draw.multiline_textbbox((0, 0), line, font)


def get_width(line, draw, font, max_width=MAX_WIDTH):
    if check_size(draw, line, font)[2] < max_width:
        return line
    else:
        lines = []
        for word in line.split():
            if check_size(draw, ' '.join(lines[-1:] + [word]), font)[2] < max_width:
                lines[-1:] = [' '.join(lines[-1:] + [word])]
            else:
                lines += [word]

        return '\n'.join(lines)
    

if __name__ == '__main__':
    for line in second_part.splitlines():
        print(get_width(line, draw, regular))