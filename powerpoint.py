import os
import re

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_AUTO_SIZE, PP_PARAGRAPH_ALIGNMENT as PP_ALIGN
from pptx.dml.color import RGBColor


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


    def add_image(self):
        slide = self.prs.slides.add_slide(self._blank_layout)
        left = top = Inches(0)
        slide.shapes.add_picture(f'services/{self._day}/image.jpg', left, top, self.prs.slide_width, self.prs.slide_height)


    def add_confession(self, content_text, title_text='Confession and Forgiveness'):
        '''Add the confession to the presentation'''
        parts = [p.start() for p in re.finditer(r'P:', content_text)]
        first_part = content_text[:parts[1]].strip()
        second_part = content_text[parts[1]:parts[2]].strip()
        third_part = content_text[parts[2]:].strip()

        slide = self._add_slide_with_header(title_text)
        content = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
        tf = content.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        self._add_run(p, first_part.splitlines()[0])

        tf.add_paragraph()
        p = tf.paragraphs[1]
        self._add_run(p, first_part.splitlines()[1], bold=True)

        slide = self._add_slide_with_header(title_text)
        content = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
        tf = content.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        self._add_run(p, second_part.splitlines()[0])
        p.add_line_break()

        p = tf.add_paragraph()
        
        run = p.add_run()
        run.text = second_part.splitlines()[1]
        run.font.name = 'Segoe UI'
        run.font.bold = False
        run.font.size = Pt(18)

        for line in second_part.splitlines()[2:]:
            p = tf.add_paragraph()
            run = p.add_run()
            run.text = line
            run.font.name = 'Segoe UI'
            run.font.bold = True
            run.font.size = Pt(18)


    def add_prayer_of_the_day(self, content_text, title_text='Prayer of the Day'):
        '''Add the prayer of the day to the presentation'''
        slide = self._add_slide_with_header(title_text)

        content = slide.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
        tf = content.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.JUSTIFY
        run = p.add_run()
        run.text = content_text.splitlines()[0]
        run.font.name = 'Segoe UI'
        run.font.bold = True
        run.font.size = Pt(18)

        p = tf.add_paragraph()
        run = p.add_run()
        run.text = content_text.splitlines()[1]
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
    def _add_run(text_frame, text, font=DEFAULT_FONT, size=DEFAULT_FONTSIZE, bold=False):
        '''Add a run to a paragraph'''
        # check if text frame has only one paragraph, if not add one
        if len(text_frame.paragraphs) == 0:
            text_frame.add_paragraph()
        paragraph = text_frame.paragraphs[-1:]
        run = paragraph.add_run()
        run.text = text
        run.font.name = font
        run.font.bold = bold
        run.font.size = Pt(size)
    

    @staticmethod
    def _add_linebreak(paragraph):
        '''Add a linebreak to a paragraph'''
        paragraph.add_run().add_break()