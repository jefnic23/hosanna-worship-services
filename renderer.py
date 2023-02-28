from PIL import ImageFont

MAX_WIDTH = 566
MAX_HEIGHT = 331

regular = ImageFont.truetype('%SystemRoot%\Fonts\segoeui.ttf', 18)
bold = ImageFont.truetype('%SystemRoot%\Fonts\segoeuib.ttf', 18)

line = 'C: we confess to you our faults and failings. Too often we neglect and do not trust your holy word; we take for ourselves instead of giving to others; we cause hurt though you call us to heal; we choose fear over compassion. Forgive us, renew us, and lead us, as we seek to follow in your way of life. Amen.'

def check_size(font, line):
    return font.getsize(line)

if __name__ == '__main__':
    size = 0
    index = 0
    while size < MAX_WIDTH:
        size = check_size(regular, line[:index])[0]
        if size >= MAX_WIDTH:
            print(index)
            break
        index+=1