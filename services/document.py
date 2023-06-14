import os
import re
from datetime import date
from itertools import chain, pairwise
from pathlib import Path

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.text.paragraph import Paragraph, Run

from config import Settings
from models.reading import Reading
from services.utils import (clean_text, get_superscripts, lookahead,
                            split_formatted_text)


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


    def add_rich_text(self, text: Reading) -> None:
        '''Add text to the document.'''
        paragraph = self._document.add_paragraph()
        
        WordDocument._add_run(paragraph, text.title + '\n', bold=True)

        superscripts = re.findall(r'<sup>(.*?)</sup>', text.body)
        regular_text, bold_text, italic_text = split_formatted_text(
            text.body
            .replace('<sup>', '').replace('</sup>', '')
            .replace('<div>', '').replace('</div>', '')
            .replace('<br>', '')
        )
        bold_lines = [line[1] for line in bold_text]
        lines = [
            clean_text(line[1]) for line in sorted(regular_text + bold_text + italic_text, key=lambda x: x[0])
        ]
        for line, has_more in lookahead(lines):
            if not line:
                continue
            sups = get_superscripts(superscripts, line)
            if len(sups) > 0:
                index = pairwise(list(chain(*[
                    [0], 
                    *[[s, e] for s, e in sups], 
                    [len(line)]
                ])))
                for start, end in index:
                    run = WordDocument._add_run(
                        paragraph, 
                        line[start:end], 
                        superscript=True if (start, end) in sups else False,
                        bold=True if line in bold_lines else False,
                        color=(86, 86, 86) if (start, end) in sups else (0, 0, 0),
                    )
                for _ in range(len(sups)):
                    superscripts.pop(0)
            else:
                run = WordDocument._add_run(
                    paragraph, 
                    line, 
                    bold=True if line in bold_lines else False,
                    color=(86, 86, 86) if line in sups else (0, 0, 0),
                )
            if has_more:
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
        os.remove(f'{self._path}/{self.day}/{self.day}.docx')


    @staticmethod
    def _add_run(
        paragraph: Paragraph, 
        text: str, 
        size: int = DEFAULT_FONTSIZE, 
        bold: bool = False, 
        italic: bool = False, 
        superscript: bool = False,
        color: tuple = (0, 0, 0), 
    ) -> Run:
        '''Add a run to a paragraph'''
        run = paragraph.add_run()
        run.text = text
        run.font.bold = bold
        run.font.italic = italic
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(*color)
        run.font.superscript = superscript
        return run
        