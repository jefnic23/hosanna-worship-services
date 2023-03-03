import os
import re

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_AUTO_SIZE, PP_PARAGRAPH_ALIGNMENT as PP_ALIGN
from pptx.dml.color import RGBColor

from utils import get_parts, get_width, get_height

from PIL import Image, ImageDraw, ImageFont

MAX_WIDTH = 566
MAX_HEIGHT = 336


regular = ImageFont.truetype('%SystemRoot%\Fonts\segoeui.ttf', 24)
bold = ImageFont.truetype('%SystemRoot%\Fonts\segoeuib.ttf', 24)
draw = ImageDraw.Draw(Image.new('RGB', (MAX_WIDTH, MAX_HEIGHT)))



class PowerPoint():
    '''Creates a PowerPoint presentation'''

    DEFAULT_FONT = 'Segoe UI'
    DEFAULT_FONTSIZE = 18
    
    def __init__(self, day):
        self._day = day
        self.prs = Presentation()

        self.prs.slide_width = Inches(6)
        self.prs.slide_height = Inches(4)

        self._section_layout = self.prs.slide_layouts[2]
        self._blank_layout = self.prs.slide_layouts[6]

        if os.path.exists(f'services/{self._day}/image.pptx'):
            self._get_image()

        if os.path.exists('liturgy/confession.txt'):
            self._confession = open('liturgy/confession.txt', 'r', encoding='utf-8').read()

        if os.path.exists('liturgy/prayer.txt'):
            self._prayer = open('liturgy/prayer.txt', 'r', encoding='utf-8').read()


    def add_image(self):
        slide = self.prs.slides.add_slide(self._blank_layout)
        left = top = Inches(0)
        slide.shapes.add_picture(f'services/{self._day}/image.jpg', left, top, self.prs.slide_width, self.prs.slide_height)


    def add_confession(self, title_text='Confession and Forgiveness'):
        '''Add the confession to the presentation'''
        pastor = [p.start() for p in re.finditer(r'P:', self._confession)]
        congregation = [c.start() for c in re.finditer(r'C:', self._confession)]

        for part in get_parts(pastor, congregation):
            if part[1] is None:
                p, c = self._confession[part[0][0]:part[0][1]].strip(), self._confession[part[0][1]:].strip()
            else:
                p, c = self._confession[part[0][0]:part[0][1]].strip(), self._confession[part[1][0]:part[1][1]].strip()
                
            width_formatted_text = []
            for line in p.splitlines():
                width_formatted_text.append(get_width(line, draw, regular))
                
            for line in c.splitlines():
                width_formatted_text.append(get_width(line, draw, bold))

            width_formatted_text = '\n'.join(width_formatted_text)

            slides = get_height(width_formatted_text, draw, regular)

            for slide in slides:
                s = self._add_slide_with_header(title_text)
                content = s.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
                tf = content.text_frame
                tf.word_wrap = True
                tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
                self._add_run(tf, slide)


    def add_prayer_of_the_day(self, title_text='Prayer of the Day'):
        '''Add the prayer of the day to the presentation'''
        slide = self._add_slide_with_header(title_text)

        content = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
        tf = content.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.JUSTIFY
        run = p.add_run()
        run.text = self._prayer.splitlines()[0]
        run.font.name = 'Segoe UI'
        run.font.bold = True
        run.font.size = Pt(18)

        p = tf.add_paragraph()
        run = p.add_run()
        run.text = self._prayer.splitlines()[1]
        run.font.name = 'Segoe UI'
        run.font.bold = True
        run.font.size = Pt(18)


    def save(self):
        '''Save the presentation'''
        self.prs.save(f'services/{self._day}/service.pptx')


    def _get_layouts(self):
        '''Get the layouts of the presentation'''
        for l in self.prs.slide_layouts:
            print(l.name)


    def _get_image(self):
        '''Add an image to the presentation'''
        prs = Presentation(f'services/{self._day}/image.pptx')
        slide = prs.slides[0]
        shape = slide.shapes[0]
        image = shape.image
        blob, ext = image.blob, image.ext
        with open(f'services/{self._day}/image.{ext}', 'wb') as f:
            f.write(blob)
    
        os.remove(f'services/{self._day}/image.pptx')


    def _add_slide_with_header(self, title_text):
        '''Add a slide with a header'''
        slide = self.prs.slides.add_slide(self._blank_layout)
        self._add_header(slide, title_text)
        return slide
    

    @staticmethod
    def _get_pastor(text):
        '''Returns the indices of the pastor's lines'''
        return [p.start() for p in re.finditer(r'P:', text)]


    @staticmethod
    def _get_congregation(text):
        '''Returns the indices of the congregation's lines'''
        return [c.start() for c in re.finditer(r'C:', text)]
    
    
    @staticmethod
    def _add_header(slide, header_text):
        '''Add a header to a slide'''
        header = slide.shapes.add_textbox(Inches(0), Inches(0), Inches(6), Inches(0))
        tf = header.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        run = p.add_run()
        run.text = header_text
        run.font.name = 'Segoe UI'
        run.font.bold = True
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(66, 133, 244)
    
    
    @staticmethod
    def _add_run(text_frame, text, font=DEFAULT_FONT, size=DEFAULT_FONTSIZE, bold=False, align=PP_ALIGN.LEFT):
        '''Add a run to a paragraph'''
        # check if text frame has only one paragraph, if not add one
        if len(text_frame.paragraphs) == 0:
            text_frame.add_paragraph()
        paragraph = text_frame.paragraphs[-1]
        paragraph.alignment = align
        run = paragraph.add_run()
        run.text = text
        run.font.name = font
        run.font.bold = bold
        run.font.size = Pt(size)
    

    @staticmethod
    def _add_linebreak(paragraph):
        '''Add a linebreak to a paragraph'''
        paragraph.add_run().add_break()