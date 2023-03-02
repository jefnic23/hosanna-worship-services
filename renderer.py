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

def get_index(line, draw, font, max_width=MAX_WIDTH):
    # get the index of the last space before the max width
    # if there is no space, return the index of the first space after the max width
    return


def get_width(line, draw, font, max_width=MAX_WIDTH):
    # new_line = line.split()[0]
    # for i, word in enumerate(line.split()[1:]):
    #     size = check_size(draw, new_line + ' ' + word, font)
    #     if size[2] < max_width:
    #         new_line += ' ' + word
    #     else:
    #         new_line += '\n' + ' '.join(line.split()[i+1:])
    #         break
    
    # return new_line

    if check_size(draw, line, font)[2] < max_width:
        return line
    else:
        # recursively split the line
        return line[:]

if __name__ == '__main__':
    # line = second_part.splitlines()[3]
    # new_line = line.split()[0]
    # for word in line.split()[1:]:
    #     size = check_size(draw, new_line + ' ' + word, bold)
    #     if size[2] < MAX_WIDTH:
    #         new_line += ' ' + word
    #     else:
    #         print(new_line, check_size(draw, new_line, bold))
    #         break
    
    for line in first_part.splitlines():
        print(get_width(line, draw, regular))