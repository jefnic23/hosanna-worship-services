from pptx import Presentation

class PowerPoint():
    def __init__(self, date):
        self.prs = Presentation()
        self.title_layout = self.prs.slide_layouts.get_by_name('Title')

    def add_slide(self):
        title_layout = self.prs.slide_layouts.get_by_name('Title')
        # slide = self.prs.slides.add_slide(title_layout)
        # for l in self.prs.slide_layouts:
        #     print(l.name)

    @staticmethod
    def get_image():
        prs = Presentation('slides.pptx')
        slide = prs.slides[0]
        shape = slide.shapes[0]
        image = shape.image
        blob = image.blob
        ext = image.ext
        with open('test.{}'.format(ext), 'wb') as f:
            f.write(blob)