import os
from hosanna.powerpoint import PowerPoint

if __name__ == '__main__':
    this_sunday = '2023-04-06'
    with open(f'services/{this_sunday}/psalm.txt', 'r', encoding='utf-8') as f:
        psalm = f.read()

    ppt = PowerPoint(this_sunday)
    ppt.add_call_and_response('Psalm', psalm)

    ppt.prs.save('tests/test.pptx')