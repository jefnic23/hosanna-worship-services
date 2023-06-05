import os
from pathlib import Path

from config import Settings
from services.document import WordDocument
from services.dropbox import Dropbox
from services.liturgy import Liturgy
from services.powerpoint import PowerPoint
from services.sundaysandseasons import SundaysAndSeasons
from services.utils import get_sunday

this_sunday = get_sunday()
settings = Settings()

path = Path(settings.LOCAL_DIR, 'services')
if not os.path.exists(f'{path}/{this_sunday}'):
    os.makedirs(f'{path}/{this_sunday}')

sas = SundaysAndSeasons(settings)
sas.day = this_sunday
sas.login()
sas.get_texts_and_images()
sas.logoff()

# lit = Liturgy(settings)
# lit.load_files('pentecost')

ppt = PowerPoint(settings)
ppt.day = this_sunday
# ppt.add_image()
# ppt.add_rich_text('Confession and Forgiveness', lit.confession)
# ppt.add_hymn()
# ppt.add_rich_text('Greeting', lit.greeting)
# ppt.add_congregation_text('Kyrie', lit.kyrie)
# ppt.add_rich_text('', lit.lord_be_with_you, anchor='middle')
# ppt.add_congregation_text('Prayer of the Day', sas.prayer)
ppt.add_title_slide(sas.first_reading.splitlines()[0])
ppt.add_rich_text('First Reading', ''.join(sas.first_reading.splitlines()[1:]))
# ppt.add_psalm(sas.psalm)
ppt.add_title_slide(sas.second_reading.splitlines()[0])
ppt.add_rich_text('Second Reading', ''.join(sas.second_reading.splitlines()[1:]))
# ppt.add_congregation_text('Gospel Acclamation', lit.gospel_acclamation)
ppt.add_title_slide(sas.gospel.splitlines()[0])
ppt.add_rich_text('Gospel', ''.join(sas.gospel.splitlines()[1:]))
# ppt.add_title_slide('Sermon')
# ppt.add_hymn()
# ppt.add_congregation_text('Apostle\'s Creed', lit.creed)
# ppt.add_intercessions(sas.intercession)
# ppt.add_rich_text('Dialogue', lit.dialogue, anchor='middle')

# ppt.add_rich_text('Preface', lit.preface)
# ppt.add_congregation_text('Holy, holy, holy', lit.hosanna)

# ppt.add_rich_text('Thanksgiving', lit.thanksgiving)
# ppt.add_congregation_text('Lord\'s Prayer', lit.lords_prayer)
# ppt.add_title_slide('Communion')
# ppt.add_congregation_text('Communion Hymn', lit.communion_hymn)
# ppt.add_title_slide('Communion')
# ppt.add_rich_text('Communion', lit.communion_blessing)
# ppt.add_rich_text('Prayer after Communion', lit.prayer_after_communion)
# ppt.add_rich_text('Blessing', lit.blessing)
# ppt.add_hymn()
# ppt.add_rich_text('Dismissal', lit.dismissal, anchor='middle')
# ppt.add_image()
ppt.save()

# doc = WordDocument(settings, day = this_sunday)
# doc.add_reading(sas.first_reading)
# doc.add_psalm(sas.psalm)
# doc.add_reading(sas.second_reading)
# doc.save()

# dbx = Dropbox(settings, day = this_sunday)
# dbx.connect()
# dbx.upload('pptx')
# dbx.upload('pdf')
# dbx.close()
