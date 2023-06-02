import os
from pathlib import Path

from services.document import WordDocument
from services.dropbox import Dropbox
from services.liturgy import Liturgy
from services.powerpoint import PowerPoint
from services.sundaysandseasons import SundaysAndSeasons
from services.utils import get_sunday

this_sunday = get_sunday()

path = Path('D:/Documents/Hosanna/Services')
if not os.path.exists(f'{path}/{this_sunday}'):
    os.makedirs(f'{path}/{this_sunday}')

sas = SundaysAndSeasons(this_sunday)
sas.get_texts_and_images()
sas.logoff()

# lit = Liturgy('pentecost')

ppt = PowerPoint(this_sunday)
# ppt.add_image()
# ppt.add_rich_text('Confession and Forgiveness', lit.confession)
# ppt.add_hymn()
# ppt.add_rich_text('Greeting', lit.greeting)
# ppt.add_congregation_text('Kyrie', lit.kyrie)
# ppt.add_rich_text('', lit.lord_be_with_you, anchor='middle')
# ppt.add_congregation_text('Prayer of the Day', sas.prayer)
ppt.add_reading('First Reading', sas.first_reading)
ppt.add_psalm(sas.psalm)
ppt.add_reading('Second Reading', sas.second_reading)
# ppt.add_congregation_text('Gospel Acclamation', lit.gospel_acclamation)
ppt.add_gospel(sas.gospel)
# ppt.add_title_slide('Sermon')
# ppt.add_hymn()
# ppt.add_congregation_text('Nicene Creed', lit.nicene_creed)
# ppt.add_intercessions(sas.intercession)
# ppt.add_rich_text('Dialogue', lit.dialogue, anchor='middle')
# ppt.add_rich_text('Preface', lit.preface, anchor='middle')
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

# doc = WordDocument(this_sunday)
# doc.add_reading(sas.first_reading)
# doc.add_psalm(sas.psalm)
# doc.add_reading(sas.second_reading)
# doc.save()

# dbx = Dropbox(this_sunday)
# dbx.upload('pptx')
# dbx.upload('pdf')
# dbx.close()
