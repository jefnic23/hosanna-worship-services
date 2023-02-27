import calendar
import datetime
import os
from datetime import date

import art

from powerpoint import PowerPoint
from sundaysandseasons import SundaysAndSeasons

SUNDAY = calendar.SUNDAY
TODAY = date.today()

# next_sunday = this_sunday + datetime.timedelta(7)

def get_this_sunday(today=TODAY, sunday=SUNDAY):
    return today + datetime.timedelta((sunday - today.weekday()) % 7)


# TODO: implement tqdm for progress bar

if __name__ == '__main__':
    this_sunday = get_this_sunday()

    # sas = SundaysAndSeasons(this_sunday)
    # sas.login()
    # sas.get_readings_and_slide()
    # sas.logoff()

    # with open(f'services/{this_sunday}/prayer.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.prayer)

    # with open(f'services/{this_sunday}/readings.txt', 'w', encoding='utf-8') as f:
    #     for reading in sas.readings:
    #         f.write(f'{reading[0]}\n{reading[1]}\n\n')

    # with open(f'services/{this_sunday}/intercession.txt', 'w', encoding='utf-8') as f:
    #     f.write(f'{sas.intercession[0]}\n{sas.intercession[1]}')

    with open(f'services/{this_sunday}/prayer.txt', 'r', encoding='utf-8') as f:
        prayer = f.read()

    ppt = PowerPoint(this_sunday)
    ppt.add_image()
    ppt.add_title_content_slide('Prayer of the Day', prayer)
    ppt.save()
    # ppt.get_image()