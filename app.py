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
    # TODO: prompt to install libreoffice if it doesn't exist

    this_sunday = get_this_sunday()

    # sas = SundaysAndSeasons(this_sunday)
    # sas.login()
    # sas.get_readings_and_slide()
    # sas.logoff()

    # with open(f'services/{this_sunday}/prayer.txt', 'w', encoding='utf-8') as f:
    #     f.write(sas.prayer)

    # first_reading = sas.readings[0]
    # psalm = sas.readings[1]
    # second_reading = sas.readings[2]
    # gospel = sas.readings[3]

    # with open(f'services/{this_sunday}/first-reading.txt', 'w', encoding='utf-8') as f:
    #     f.write(f'{first_reading[0]}\n{first_reading[1]}')

    # with open(f'services/{this_sunday}/psalm.txt', 'w', encoding='utf-8') as f:
    #     f.write(f'{psalm[0]}\n{psalm[1]}')

    # with open(f'services/{this_sunday}/second-reading.txt', 'w', encoding='utf-8') as f:
    #     f.write(f'{second_reading[0]}\n{second_reading[1]}')

    # with open(f'services/{this_sunday}/gospel.txt', 'w', encoding='utf-8') as f:
    #     f.write(f'{gospel[0]}\n{gospel[1]}')

    # with open(f'services/{this_sunday}/intercession.txt', 'w', encoding='utf-8') as f:
    #     f.write(f'{sas.intercession[0]}\n{sas.intercession[1]}')

    # TODO: prompt to add hymns if they don't exist

    # ppt = PowerPoint(this_sunday)
    # ppt.add_image()
    # ppt.add_confession()
    # ppt.add_hymn()
    # ppt.add_greeting()
    # ppt.add_kyrie()
    # ppt.add_prayer_of_the_day()
    # ppt.add_reading('First Reading', ppt._first_reading)
    # ppt.add_psalm()
    # ppt.add_reading('Second Reading', ppt._second_reading)
    # ppt.add_gospel_acclamation()
    # ppt.add_gospel()
    # ppt.add_title_slide('Sermon')
    # ppt.add_hymn()
    # ppt.add_creed('Apostle\'s Creed')
    # ppt.add_intercessions()
    # ppt.add_dialogue()
    # ppt.add_hosanna()
    # ppt.add_communion_dialogue()
    # ppt.add_lords_prayer('Lord\'s Prayer')
    # ppt.add_title_slide('Communion')
    # ppt.add_communion_hymn()
    # ppt.add_call_and_response('Prayer after Communion', ppt._prayer_after_communion)
    # ppt.add_call_and_response('Benediction', ppt._benediction)
    # ppt.add_hymn()
    # ppt.add_call_and_response('Dismissal', ppt._dismissal)
    # ppt.add_image()
    # ppt.save()
    