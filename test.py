from services.powerpoint import PowerPoint

if __name__ == '__main__':
    this_sunday = '2023-04-07'
    with open('tests/prayer.txt', 'r', encoding='utf-8') as f:
        psalm = f.read()

    ppt = PowerPoint(this_sunday)
    ppt.add_call_and_response('Psalm', psalm)

    ppt.prs.save('tests/test.pptx')
