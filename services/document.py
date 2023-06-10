import os
import re
from datetime import date
from itertools import chain
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.text.paragraph import Paragraph

from config import Settings
from models.reading import Reading
from services.utils import clean_text, get_superscripts, lookahead, pairwise


class WordDocument:
    '''A class for creating a Word document.'''

    DEFAULT_FONTSIZE = 14

    def __init__(self, settings: Settings):
        self.day: date = date.today()
        self._path = f'{settings.LOCAL_DIR}/services'
        self._document = Document()
        self._section = self._document.sections[0]
        self._section.left_margin =  \
        self._section.right_margin = \
        self._section.top_margin =   \
        self._section.bottom_margin = Inches(0.5)


    def add_reading(self, reading: Reading) -> None:
        '''Add a reading to the document.'''
        paragraph = self._document.add_paragraph()
        run = paragraph.add_run(reading.title + "\n")
        run.font.bold = True
        run.font.size = Pt(14)
        
        superscripts = re.findall(r'<sup>(.*?)</sup>', reading.body)
        text = (
            reading.body
            .replace('<sup>', '')
            .replace('</sup>', '')
            .replace('<div>', '')
            .replace('</div>', '')
            .replace('<br>', '')
            .replace('<b>', '')
            .replace('</b>', '')
        )
        reading = [clean_text(line) for line in text.splitlines()]
        for line, has_more in lookahead(reading):
            sups = get_superscripts(superscripts, line)
            if len(sups) > 0:
                index = pairwise(
                    list(chain(*[[0], *[[s, e] for s, e in sups], [len(line)]]))
                )
                for start, end in index:
                    run = paragraph.add_run(line[start:end].strip())
                    run.font.superscript = True if (start, end) in sups else False
                    run.font.size = Pt(14)
                for _ in range(len(sups)):
                    superscripts.pop(0)
            else:
                run = paragraph.add_run(line.strip())
                run.font.size = Pt(14)
                run.font.bold = False if has_more else True

            if has_more:
                run.add_break()


    def add_psalm(self, psalm: Reading) -> None:
        '''Add a psalm to the document.'''
        paragraph = self._document.add_paragraph()
        run = paragraph.add_run(psalm.title + "\n")
        run.font.bold = True
        run.font.size = Pt(14)

        # superscripts = re.findall(r'<sup>(.*?)</sup>', psalm.body)
        psalm =(
            psalm.body
            .replace('<sup>', '')
            .replace('</sup>', '')
            .replace('<div>', '')
            .replace('</div>', '')
            .replace('<br>', '')
            .replace('<b>', '')
            .replace('</b>', '')
        )
        for i, line in enumerate(psalm.splitlines()):
            run = paragraph.add_run(line[0:2])
            run.font.superscript = True
            run.font.size = Pt(14)
            run.font.bold = False if i % 2 == 0 else True

            run = paragraph.add_run(line[2:].strip())
            run.font.superscript = False
            run.font.size = Pt(14)
            run.font.bold = False if i % 2 == 0 else True

            run.add_break()


    def save(self) -> None:
        '''Save the document to the services folder.'''        
        if not os.path.exists(f'{self._path}/{self.day}'):
            os.makedirs(f'{self._path}/{self.day}')
        self._document.save(f'{self._path}/{self.day}/{self.day}.docx')

        os.system(
            f'soffice --headless --invisible --convert-to pdf --outdir '
            f'{self._path}/{self.day} {self._path}/{self.day}/{self.day}.docx'
        )
        # os.remove(f'{self._path}/{self.day}/{self.day}.docx')


    @staticmethod
    def _add_run(
        paragraph: Paragraph, 
        text: str, 
        size: int = DEFAULT_FONTSIZE, 
        bold: bool = False, 
        italic: bool = False, 
        color: tuple = (0, 0, 0), 
        has_more: bool = False, 
        superscript: bool = False
    ) -> None:
        '''Add a run to a paragraph'''
        run = paragraph.add_run()
        run.text = text
        run.font.bold = bold
        run.font.italic = italic
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(*color)
        run.font.superscript = superscript
        if has_more:
            run.add_break()
        