import os
import re
from datetime import date
from itertools import chain
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE, MSO_VERTICAL_ANCHOR
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT as PP_ALIGN
from pptx.slide import Slide
from pptx.text.text import _Paragraph
from pptx.util import Inches, Pt

from services.utils import (
    get_superscripts,
    grouper,
    lookahead,
    pairwise,
    split_regular_bold_text,
)


class PowerPoint():
    '''A class for creating a PowerPoint presentation.'''
    DEFAULT_FONT = 'Segoe UI'
    DEFAULT_FONTSIZE = 18
    MAX_WIDTH = 565
    MAX_HEIGHT = 335
    
    REGULAR = ImageFont.truetype('%SystemRoot%\Fonts\segoeui.ttf', 24)
    BOLD = ImageFont.truetype('%SystemRoot%\Fonts\segoeuib.ttf', 24)
    DRAW = ImageDraw.Draw(Image.new('RGB', (MAX_WIDTH, MAX_HEIGHT)))
    
    def __init__(
        self, 
        day: date,
        path: Path = Path('D:/Documents/Hosanna/services') 
    ):
        self._day = day
        self._path = path
        self.prs = Presentation()
        self.prs.slide_width = Inches(6)
        self.prs.slide_height = Inches(4)
        self._section_layout = self.prs.slide_layouts[2]
        self._blank_layout = self.prs.slide_layouts[6]

        if os.path.exists(f'{path}/{day}/image.pptx'):
            self._get_image()

        if os.path.exists(f'{path}/{day}/hymns.txt'):
            self._hymns = self._load_hymns()


    def add_title_slide(self, text: str) -> None:
        '''Add a title slide to the presentation/'''
        slide = self.prs.slides.add_slide(self._blank_layout)
        content = slide.shapes.add_textbox(Inches(0), Inches(0), Inches(6), Inches(4))
        tf = content.text_frame
        
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        self._add_run(p, text, bold=True, size=24)


    def add_image(self) -> None:
        '''Add an image to the presentation.'''
        slide = self.prs.slides.add_slide(self._blank_layout)
        left = top = Inches(0)
        slide.shapes.add_picture(f'{self._path}/{self._day}/image.jpg', left, top, self.prs.slide_width, self.prs.slide_height)


    def add_congregation_text(
            self, 
            title: str, 
            text: str,
            draw: ImageDraw = DRAW,
            bold: ImageFont = BOLD,
            regular: ImageFont = REGULAR
        ) -> None:
        '''Add bold text to be read by the congregation to the presentation.'''
        width_formatted_text = []
        for line in text.splitlines():
            width_formatted_text.append(PowerPoint.get_width(line, draw, bold))

        width_formatted_text = '\n'.join(width_formatted_text)

        slides = PowerPoint.get_height(width_formatted_text, draw, regular)

        for slide in slides:
            s = self._add_slide_with_header(title)
            content = s.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
            tf = content.text_frame
            tf.auto_size = MSO_AUTO_SIZE.NONE
            p = tf.paragraphs[0]
            for line, has_more in lookahead(slide.splitlines()):
                self._add_run(p, line, bold=True, has_more=has_more)


    def add_hymn(self) -> None:
        '''Add a hymn to the presentation.'''
        slide = self.prs.slides.add_slide(self._blank_layout)
        content = slide.shapes.add_textbox(Inches(0), Inches(0), Inches(6), Inches(4))
        tf = content.text_frame
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
        for line, has_more in lookahead(self._hymns.pop(0)):
            paragraph = tf.paragraphs[0]
            paragraph.alignment = PP_ALIGN.CENTER
            self._add_run(paragraph, line, bold=True, italic=True if has_more else False, size=24, has_more=has_more)


    def add_reading(
            self, 
            title_text: str, 
            text: str,
            draw: ImageDraw = DRAW,
            regular: ImageFont = REGULAR
        ) -> None:
        '''Add a reading to the presentation.'''
        title = text.splitlines()[0]
        reading = text.splitlines()[1:]

        self.add_title_slide(title)

        width_formatted_text = []
        for line in reading:
            width_formatted_text.append(PowerPoint.get_width(line, draw, regular))

        width_formatted_text = '\n'.join(width_formatted_text)

        slides = PowerPoint.get_height(width_formatted_text, draw, regular)

        for slide, is_not_last in lookahead(slides):
            s = self._add_slide_with_header(title_text)
            content = s.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
            tf = content.text_frame
            tf.auto_size = MSO_AUTO_SIZE.NONE
            paragraph = tf.paragraphs[0]
            for line, has_more in lookahead(slide.splitlines()):
                superscripts = get_superscripts(line)
                if superscripts:
                    for start, end in superscripts:
                        self._add_run(paragraph, line[:start])
                        self._add_run(paragraph, line[start:end], superscript=True)
                        self._add_run(paragraph, line[end:], has_more=has_more)
                else:
                    if not is_not_last and not has_more:
                        self._add_run(paragraph, line, bold=True)
                    else:
                        self._add_run(paragraph, line, has_more=has_more)


    def add_psalm(
            self, 
            text: str, 
            draw: ImageDraw = DRAW, 
            bold: ImageFont = BOLD, 
            regular: ImageFont = REGULAR
        ) -> None:
        '''Add a psalm to the presentation.'''
        text = text.replace('|', '').replace('- ', '')
        title = text.splitlines()[0]
        psalm = [line.strip() for line in text.splitlines()[1:] if line]

        self.add_title_slide(title)

        p = []
        c = []
        first_lines = []

        width_formatted_text = []
        for i, line in enumerate(psalm):
            if i % 2 == 0:
                new_line = PowerPoint.get_width(line, draw, regular)
                first_lines.append(new_line.splitlines()[0])
                for l in new_line.splitlines():
                    p.append(l)
                width_formatted_text.append(new_line)
            else:
                new_line = PowerPoint.get_width(line, draw, bold)
                first_lines.append(new_line.splitlines()[0])
                for l in new_line.splitlines():
                    c.append(l)
                width_formatted_text.append(new_line)

        width_formatted_text = '\n'.join(width_formatted_text)

        slides = PowerPoint.get_height(width_formatted_text, draw, regular)

        for slide in slides:
            s = self._add_slide_with_header(title)
            content = s.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
            tf = content.text_frame
            tf.auto_size = MSO_AUTO_SIZE.NONE
            paragraph = tf.paragraphs[0]
            for line, has_more in lookahead(slide.splitlines()):
                if line in first_lines:
                    superscripts = get_superscripts(line)
                    if superscripts:
                        for start, end in superscripts:
                            self._add_run(paragraph, line[:start], bold=True if line in c else False)
                            self._add_run(paragraph, line[start:end], bold=True if line in c else False, superscript=True)
                            self._add_run(paragraph, line[end:], bold=True if line in c else False, has_more=has_more)
                    else:
                        self._add_run(paragraph, line, bold=True, has_more=has_more)
                else:
                    self._add_run(paragraph, line, bold=True if line in c else False, has_more=has_more)


    def add_gospel(
            self, 
            text: str,
            header: str = 'Gospel',
            draw: ImageDraw = DRAW,
            regular: ImageFont = REGULAR
        ) -> None:
        '''Add the gospel to the presentation.'''
        title = text.splitlines()[0].split()[0]
        reading = text.splitlines()[1:]

        slide = self.prs.slides.add_slide(self._blank_layout)
        content = slide.shapes.add_textbox(Inches(0), Inches(0), Inches(6), Inches(4))
        tf = content.text_frame
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        self._add_run(p, f'The holy gospel according to {title}.')
        p.add_line_break()
        self._add_run(p, 'Glory to you, O Lord.', bold=True)

        width_formatted_text = []
        for line in reading:
            width_formatted_text.append(PowerPoint.get_width(line, draw, regular))

        width_formatted_text = '\n'.join(width_formatted_text)

        slides = PowerPoint.get_height(width_formatted_text, draw, regular)

        for slide, is_not_last in lookahead(slides):
            s = self._add_slide_with_header(header)
            content = s.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
            tf = content.text_frame
            tf.auto_size = MSO_AUTO_SIZE.NONE
            paragraph = tf.paragraphs[0]
            paragraph.alignment = PP_ALIGN.LEFT
            for line, has_more in lookahead(slide.splitlines()):
                superscripts = get_superscripts(line)
                if len(superscripts) > 0:
                    index = pairwise(list(chain(*[[0], *[[s, e] for s, e in superscripts], [len(line)]])))
                    for start, end in index:
                        self._add_run(paragraph, line[start:end], superscript=True if (start, end) in superscripts else False)
                    if has_more:
                        paragraph.add_line_break()
                else:
                    if not is_not_last and not has_more:
                        self._add_run(paragraph, line, bold=True)
                    else:
                        self._add_run(paragraph, line, has_more=has_more)


    def add_intercessions(self, text: str) -> None:
        '''Add the intercessions to the presentation.'''
        slide = self._add_slide_with_header('Prayers of Intercession')
        content = slide.shapes.add_textbox(Inches(0), Inches(0), Inches(6), Inches(4))
        tf = content.text_frame
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        self._add_run(p, 'Each petition ends:', italic=True)
        p.add_line_break()
        self._add_run(p, text.splitlines()[0])
        p.add_line_break()
        self._add_run(p, text.splitlines()[1], bold=True)


    def add_dialogue(self, text: str) -> None:
        '''Add the dialogue to the presentation.'''
        text = grouper(text.splitlines(), 2)

        slide = self._add_slide_with_header('Dialogue')
        content = slide.shapes.add_textbox(Inches(0), Inches(0), Inches(6), Inches(4))
        tf = content.text_frame
        
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        for line, has_more in lookahead(text):
            self._add_run(p, line[0])
            p.add_line_break()
            self._add_run(p, line[1], bold=True, has_more=has_more)
            if has_more:
                p.add_line_break()


    def add_call_and_response(
            self, 
            title: str, 
            text: str, 
            anchor: MSO_VERTICAL_ANCHOR = None,
            draw: ImageDraw = DRAW,
            regular: ImageFont = REGULAR,
            bold: ImageFont = BOLD
        ) -> None:
        '''Add a call and response to the presentation.'''
        regular_text, bold_text = split_regular_bold_text(text)
        bold_lines = [line[1] for line in bold_text]
        lines = [
            line[1] for line in sorted(regular_text + bold_text, key=lambda x: x[0])
        ]
        width_formatted_text = []
        bold_formatted_text = []
        for line in lines:
            if line in bold_lines:
                bold_line = PowerPoint.get_width(line, draw, bold)
                width_formatted_text.append(bold_line)
                for l in bold_line.splitlines():
                    bold_formatted_text.append(l)
            else:
                width_formatted_text.append(PowerPoint.get_width(line, draw, regular))

        width_formatted_text = '\n'.join(width_formatted_text)

        slides = PowerPoint.get_height(width_formatted_text, draw, regular)

        for slide, is_not_last in lookahead(slides):
            s = self._add_slide_with_header(title)
            content = s.shapes.add_textbox(Inches(0), Inches(0.5), Inches(6), Inches(0))
            tf = content.text_frame
            tf.auto_size = MSO_AUTO_SIZE.NONE
            tf.vertical_anchor = anchor
            paragraph = tf.paragraphs[0]
            paragraph.alignment = PP_ALIGN.LEFT
            for line, has_more in lookahead(slide.splitlines()):
                superscripts = get_superscripts(line)
                if len(superscripts) > 0:
                    index = pairwise(list(chain(*[[0], *[[s, e] for s, e in superscripts], [len(line)]])))
                    for start, end in index:
                        self._add_run(
                            paragraph, 
                            line[start:end], 
                            superscript=True if (start, end) in superscripts else False,
                            bold=True if line in bold_formatted_text else False
                        )
                    if has_more:
                        paragraph.add_line_break()
                else:
                    if not is_not_last and not has_more:
                        self._add_run(paragraph, line, bold=True if line in bold_formatted_text else False)
                    else:
                        self._add_run(paragraph, line, has_more=has_more, bold=True if line in bold_formatted_text else False)


    def save(self) -> None:
        '''Save the presentation.'''
        if not os.path.exists(f'{self._path}/{self._day}'):
            os.makedirs(f'{self._path}/{self._day}')
        self.prs.save(f'{self._path}/{self._day}/{self._day}.pptx')


    def _load_hymns(self) -> list[tuple]:
        '''Load the hymns from the hymns.txt file.'''
        hymns = open(f'{self._path}/{self._day}/hymns.txt', 'r', encoding='utf-8').read()
        return grouper(hymns.splitlines(), 2)


    def _get_layouts(self) -> None:
        '''Get the layouts of the presentation.'''
        for l in self.prs.slide_layouts:
            print(l.name)


    def _get_image(self) -> None:
        '''Add an image to the presentation.'''
        prs = Presentation(f'{self._path}/{self._day}/image.pptx')
        slide = prs.slides[0]
        shape = slide.shapes[0]
        image = shape.image
        blob, ext = image.blob, image.ext
        with open(f'{self._path}/{self._day}/image.{ext}', 'wb') as f:
            f.write(blob)
    
        os.remove(f'{self._path}/{self._day}/image.pptx')


    def _add_slide_with_header(self, title_text: str) -> Slide:
        '''Add a slide with a header'''
        slide = self.prs.slides.add_slide(self._blank_layout)
        self._add_header(slide, title_text)
        return slide
    

    @staticmethod
    def _get_pastor(text: str) -> list[int]:
        '''Returns the indices of the pastor's lines'''
        return [p.start() for p in re.finditer(r'P:', text)]


    @staticmethod
    def _get_congregation(text: str) -> list[int]:
        '''Returns the indices of the congregation's lines'''
        return [c.start() for c in re.finditer(r'C:', text)]

    
    @staticmethod
    def _add_header(slide: Slide, header_text: str) -> None:
        '''Add a header to a slide'''
        header = slide.shapes.add_textbox(Inches(0), Inches(0.1), Inches(6), Inches(0))
        tf = header.text_frame
        tf.auto_size = MSO_AUTO_SIZE.NONE
        paragraph = tf.paragraphs[0]
        paragraph.alignment = PP_ALIGN.RIGHT
        PowerPoint._add_run(paragraph, header_text, size=12, bold=True, color=(66, 133, 244))
    
    
    @staticmethod
    def _add_run(
        paragraph: _Paragraph, 
        text: str, 
        font: str = DEFAULT_FONT, 
        size: int = DEFAULT_FONTSIZE, 
        bold: bool = False, 
        italic: bool = False, 
        color: tuple = (0, 0, 0), 
        has_more: bool = False, 
        superscript: bool = False
    ) -> None:
        '''Add a run to a paragraph'''
        run = paragraph.add_run()
        run.text = text.strip()
        run.font.name = font
        run.font.bold = bold
        run.font.italic = italic
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(*color)
        run.font._element.set('baseline', '30000' if superscript else '0')
        if has_more:
            paragraph.add_line_break()


    @staticmethod
    def check_size(
        line: str,
        draw: ImageDraw,
        font: ImageFont
    ) -> dict[str, int]:
        '''Checks the size of a line of text.'''
        size = draw.multiline_textbbox((0, 0), line, font)
        return {'width': size[2], 'height': size[3]}


    @staticmethod
    def get_width(
        line: str, 
        draw: ImageDraw, 
        font: ImageFont, 
        max_width: int = MAX_WIDTH
    ):
        '''Gets the width of a line of text and splits it if it's too long.'''
        if PowerPoint.check_size(line, draw, font)['width'] < max_width:
            return line
        else:
            lines = []
            for word in line.split():
                if PowerPoint.check_size(' '.join(lines[-1:] + [word]), draw, font)['width'] < max_width:
                    lines[-1:] = [' '.join(lines[-1:] + [word])]
                else:
                    lines += [word]

            return '\n'.join(lines)
        

    @staticmethod
    def get_height(
        lines: str, 
        draw: ImageDraw, 
        font: ImageFont, 
        max_height: int = MAX_HEIGHT
    ) -> list[str]:
        '''Gets the height of a line of text and splits it if it's too long.'''
        if PowerPoint.check_size(lines, draw, font)['height'] < max_height:
            return [lines]
        else:
            slides = []
            for line in lines.splitlines():
                if PowerPoint.check_size('\n'.join(slides[-1:] + [line]), draw, font)['height'] < max_height:
                    slides[-1:] = ['\n'.join(slides[-1:] + [line])]
                else:
                    slides += [line]

            return slides
        

    @staticmethod
    def get_slides(
        lines: str, 
        draw: ImageDraw, 
        regular: ImageFont,
    ) -> list[str]:
        '''Transforms a string into a list of strings that fit on a slide.'''
        width_formatted_text = []
        for line in lines.splitlines():
            width_formatted_text.append(PowerPoint.get_width(line, draw, regular))
        width_formatted_text = '\n'.join(width_formatted_text)

        return PowerPoint.get_height(width_formatted_text, draw, regular)
            