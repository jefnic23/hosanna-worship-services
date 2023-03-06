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
    # this_sunday = get_this_sunday()

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

    this_sunday = '2023-02-26'

    ppt = PowerPoint(this_sunday)
    ppt.add_image()
    ppt.add_confession()
    ppt.add_hymn()
    ppt.add_greeting()
    ppt.add_kyrie()
    ppt.add_prayer_of_the_day()
    ppt.add_reading('First Reading', ppt._first_reading)
    ppt.add_psalm()
    ppt.add_reading('Second Reading', ppt._second_reading)
    ppt.add_gospel_acclamation()
    ppt.add_gospel()
    ppt.add_title_slide('Sermon')
    ppt.save()
    # ppt.get_image()