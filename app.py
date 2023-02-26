import calendar
import datetime
from datetime import date
import os

from powerpoint import PowerPoint
from sundaysandseasons import SundaysAndSeasons

SUNDAY = calendar.SUNDAY
TODAY = date.today()

# next_sunday = this_sunday + datetime.timedelta(7)

def get_this_sunday(today=TODAY, sunday=SUNDAY):
    return today + datetime.timedelta((sunday - today.weekday()) % 7)


# TODO: implrement tqdm for progress bar

if __name__ == '__main__':
    this_sunday = get_this_sunday()

    sas = SundaysAndSeasons()
    sas.login()
    sas.get_readings_and_slide(this_sunday)
    sas.logoff()
    
    # os.system('soffice --headless --invisible --convert-to pptx slides.ppt')

    # ppt = PowerPoint(this_sunday)
    # ppt.get_image()