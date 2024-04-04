from enum import Enum

from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT as PP_ALIGN


class HorizontalAlignment(Enum):
    LEFT = PP_ALIGN.LEFT
    CENTER = PP_ALIGN.CENTER
    RIGHT = PP_ALIGN.RIGHT
