from enum import Enum

from pptx.enum.text import MSO_VERTICAL_ANCHOR


class VerticalAlignment(Enum):
    TOP = MSO_VERTICAL_ANCHOR.TOP
    MIDDLE = MSO_VERTICAL_ANCHOR.MIDDLE
    BOTTOM = MSO_VERTICAL_ANCHOR.BOTTOM
