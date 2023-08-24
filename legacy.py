import os
from pathlib import Path

from services.document import WordDocument
from services.dropbox import Dropbox
from services.hymns import Hymns
from services.liturgy import Liturgy
from services.powerpoint import PowerPoint
from services.settings import Settings
from services.sundaysandseasons import SundaysAndSeasons
from services.utils import get_sunday

this_sunday = get_sunday(delta=0)
settings = Settings()

path = Path(settings.LOCAL_DIR, 'services')
if not os.path.exists(f'{path}/{this_sunday}'):
    os.makedirs(f'{path}/{this_sunday}')

sas = SundaysAndSeasons(settings)
sas.day = this_sunday
sas.login()
sas.get_texts_and_images()
sas.logoff()

lit = Liturgy(settings)
lit.load_files('Autumn')

hymns = Hymns(settings)
hymns.day = this_sunday
hymns.add_hymn(513)
hymns.add_hymn(517)
hymns.add_hymn(504)

ppt = PowerPoint(settings)
ppt.day = this_sunday
ppt.convert_image()
ppt.add_image()
ppt.add_rich_text('Confession and Forgiveness', lit.confession)
ppt.add_hymn(hymns._hymns[0])
ppt.add_rich_text('Greeting', lit.greeting)
ppt.add_rich_text('Kyrie', lit.kyrie, spoken=True)
ppt.add_rich_text('', lit.lord_be_with_you, anchor='middle')
ppt.add_rich_text('Prayer of the Day', sas.prayer, spoken=True)
ppt.add_title_slide(sas.first_reading.title)
ppt.add_rich_text('First Reading', sas.first_reading.body)
ppt.add_title_slide(sas.psalm.title)
ppt.add_rich_text('Psalm', sas.psalm.body)
ppt.add_title_slide(sas.second_reading.title)
ppt.add_rich_text('Second Reading', sas.second_reading.body)
ppt.add_rich_text('Gospel Acclamation', lit.gospel_acclamation, spoken=True)
ppt.add_gospel_title(sas.gospel.title)
ppt.add_rich_text('Gospel', sas.gospel.body)
ppt.add_title_slide('Sermon')
ppt.add_hymn(hymns._hymns[1])
ppt.add_rich_text('Apostle\'s Creed', lit.creed, spoken=True)
ppt.add_intercessions('Lord, in your mercy,', 'hear our prayer.')
ppt.add_rich_text('Dialogue', lit.dialogue, anchor='middle')

# ppt.add_rich_text('Preface', lit.preface)
# ppt.add_rich_text('Holy, holy, holy', lit.hosanna, spoken=True)

ppt.add_rich_text('Thanksgiving', lit.thanksgiving)
ppt.add_rich_text('Lord\'s Prayer', lit.lords_prayer, spoken=True)
ppt.add_title_slide('Communion')
ppt.add_rich_text('Communion Hymn', lit.communion_hymn, spoken=True)
ppt.add_title_slide('Communion')
ppt.add_rich_text('Communion', lit.communion_blessing)
ppt.add_rich_text('Prayer after Communion', lit.prayer_after_communion)
ppt.add_rich_text('Blessing', lit.blessing)
ppt.add_hymn(hymns._hymns[2])
ppt.add_rich_text('Dismissal', lit.dismissal, anchor='middle')
ppt.add_image()
ppt.save()

doc = WordDocument(settings)
doc.day = this_sunday
doc.add_rich_text(sas.first_reading)
doc.add_rich_text(sas.psalm)
doc.add_rich_text(sas.second_reading)
doc.save()

dbx = Dropbox(settings)
dbx.day = this_sunday
dbx.connect()
dbx.upload('pptx')
dbx.upload('pdf')
dbx.close()
