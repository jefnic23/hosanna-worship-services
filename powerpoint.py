import os

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_AUTO_SIZE, MSO_ANCHOR, PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE


class PowerPoint():
    def __init__(self, day):
        self._day = day
        self.prs = Presentation()

        self.prs.slide_width = Inches(6)
        self.prs.slide_height = Inches(4)

        self._title_layout = self.prs.slide_layouts[0]
        self._title_content_layout = self.prs.slide_layouts[1]
        self._section_layout = self.prs.slide_layouts[2]
        self._blank_layout = self.prs.slide_layouts[6]

        if os.path.exists(f'services/{self._day}/image.pptx'):
            self._get_image()


    def add_image(self):
        '''Add an image to the presentation'''
        slide = self.prs.slides.add_slide(self._blank_layout)
        left = top = Inches(0)
        slide.shapes.add_picture(f'services/{self._day}/image.jpg', left, top, self.prs.slide_width, self.prs.slide_height)


    def add_title_content_slide(self, title_text, content_text):
        '''Add a slide to the presentation'''
        slide = self.prs.slides.add_slide(self._blank_layout)
        title = slide.shapes.add_textbox(Inches(0.0), Inches(0.0), Inches(6), Inches(0))
        tf = title.text_frame
        tf.text = title_text
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT

        content = slide.shapes.add_textbox(Inches(0.25), Inches(0.5), Inches(5), Inches(2))
        tf = content.text_frame
        tf.text = content_text
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT


    def save(self):
        '''Save the presentation'''
        self.prs.save(f'services/{self._day}/service.pptx')


    def _get_layouts(self):
        '''Get the layouts of the presentation'''
        for l in self.prs.slide_layouts:
            print(l.name)


    def _get_image(self):
        '''Get the image from the first slide'''
        prs = Presentation(f'services/{self._day}/image.pptx')
        slide = prs.slides[0]
        shape = slide.shapes[0]
        image = shape.image
        blob, ext = image.blob, image.ext
        with open(f'services/{self._day}/image.{ext}', 'wb') as f:
            f.write(blob)
    
        os.remove(f'services/{self._day}/image.pptx')