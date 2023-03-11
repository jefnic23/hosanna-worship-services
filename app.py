import calendar
import datetime
import os
from datetime import date

import art

from powerpoint import PowerPoint
from sundaysandseasons import SundaysAndSeasons

from pptx.enum.text import MSO_VERTICAL_ANCHOR

SUNDAY = calendar.SUNDAY
TODAY = date.today()

def get_this_sunday(today=TODAY, sunday=SUNDAY):
    return today + datetime.timedelta((sunday - today.weekday()) % 7)

# next_sunday = this_sunday + datetime.timedelta(7)




# TODO: implement tqdm/rich for progress bar

if __name__ == '__main__':
    # TODO: prompt to install libreoffice if it doesn't exist
    # https://www.libreoffice.org/download/download-libreoffice/

    this_sunday = get_this_sunday() + datetime.timedelta(14)

    # sas = SundaysAndSeasons(this_sunday)
    # sas.login()
    # sas.get_readings_and_slide()
    # sas.logoff()

    # if not os.path.exists(f'services/{this_sunday}'):
    #     os.makedirs(f'services/{this_sunday}')

    # with open(f'services/{this_sunday}/prayer.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.prayer)

    # with open(f'services/{this_sunday}/first-reading.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.first_reading)

    # with open(f'services/{this_sunday}/psalm.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.psalm)

    # with open(f'services/{this_sunday}/second-reading.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.second_reading)

    # with open(f'services/{this_sunday}/gospel.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.gospel)

    # with open(f'services/{this_sunday}/intercession.txt', 'w', encoding='utf-8') as f:
    #     f.write(f'{sas.intercession[0]}\n{sas.intercession[1]}')

    # TODO: prompt to add hymns if they don't exist

    ppt = PowerPoint(this_sunday)
    ppt.add_image()
    ppt.add_call_and_response('Confession and Forgiveness', ppt._confession)
    ppt.add_hymn()
    ppt.add_call_and_response('Greeting', ppt._greeting)
    ppt.add_congregation_text('Kyrie', ppt._kyrie)
    ppt.add_congregation_text('Prayer of the Day', ppt._prayer)
    ppt.add_reading('First Reading', ppt._first_reading)
    ppt.add_psalm()
    ppt.add_reading('Second Reading', ppt._second_reading)
    ppt.add_congregation_text('Gospel Acclamation', ppt._gospel_acclamation)
    ppt.add_gospel()
    ppt.add_title_slide('Sermon')
    ppt.add_hymn()
    ppt.add_congregation_text('Apostle\'s Creed', ppt._creed)
    ppt.add_intercessions()
    ppt.add_dialogue()
    ppt.add_congregation_text('Holy, holy, holy', ppt._hosanna)
    ppt.add_call_and_response('Communion Dialogue', ppt._communion_dialogue)
    ppt.add_congregation_text('Lord\'s Prayer', ppt._lords_prayer)
    ppt.add_title_slide('Communion')
    ppt.add_congregation_text('Communion Hymn', ppt._communion_hymn)
    ppt.add_call_and_response('Prayer after Communion', ppt._prayer_after_communion)
    ppt.add_call_and_response('Benediction', ppt._benediction)
    ppt.add_hymn()
    ppt.add_call_and_response('Dismissal', ppt._dismissal)
    ppt.add_image()
    ppt.save()
    