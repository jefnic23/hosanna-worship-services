# TODO

- [X] Make sure the Psalm is being parsed correctly
- [x] Normalize the readings and gospel
- [x] Turn off word wrap
- [x] How to handle lines with multiple superscripts?
- [x] Certain lines should be grouped together (calls and responses)
- [ ] Make test cases
- [x] Decouple SundaysAndSeasons from PowerPoint
- [x] Load the liturgy from a class, not the PowerPoint
- [ ] Error handling
- [ ] Check Sundays and Seasons for multiple readings
- [ ] Change naming conventions for uploaded files (service.pptx, readings.pdf)

After installing eel, add these lines to ``def open(start_pages, options):`` in ``browser.py``:
```
elif mode == 'brave':
    for url in start_urls:
        brave_path = 'brave-portable/brave-portable.exe'
        wbr.register('brave-portable', None, wbr.BackgroundBrowser(brave_path))
        wbr.get('brave-portable').open(f'--app={url}')
```
