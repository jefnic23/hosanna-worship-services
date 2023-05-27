import os
from pathlib import Path

from services.document import WordDocument
from services.dropbox import Dropbox
from services.liturgy import Liturgy
from services.powerpoint import PowerPoint
from services.sundaysandseasons import SundaysAndSeasons
from services.utils import get_sunday


this_sunday = get_sunday()

path = Path('D:/Documents/Hosanna/services')
if not os.path.exists(f'{path}/{this_sunday}'):
    os.makedirs(f'{path}/{this_sunday}')

sas = SundaysAndSeasons(this_sunday)
sas.get_texts_and_slide()
sas.logoff()

lit = Liturgy('pentecost')

ppt = PowerPoint(this_sunday)
ppt.add_image()
ppt.add_call_and_response('Confession and Forgiveness', lit.confession)
ppt.add_hymn()
ppt.add_call_and_response('Greeting', lit.greeting)
ppt.add_congregation_text('Kyrie', lit.kyrie)
ppt.add_call_and_response('', lit.lord_be_with_you)
ppt.add_congregation_text('Prayer of the Day', sas.prayer)
ppt.add_reading('First Reading', sas.first_reading)
ppt.add_psalm(sas.psalm)
ppt.add_reading('Second Reading', sas.second_reading)
ppt.add_congregation_text('Gospel Acclamation', lit.gospel_acclamation)
ppt.add_gospel(sas.gospel)
ppt.add_title_slide('Sermon')
ppt.add_hymn()
ppt.add_congregation_text('Nicene Creed', lit.nicene_creed)
ppt.add_intercessions(sas.intercession)
ppt.add_call_and_response('Dialogue', lit.dialogue)
ppt.add_congregation_text('Holy, holy, holy', lit.hosanna)
ppt.add_call_and_response('Communion Dialogue', lit.communion_dialogue)
ppt.add_congregation_text('Lord\'s Prayer', lit.lords_prayer)
ppt.add_title_slide('Communion')
ppt.add_congregation_text('Communion Hymn', lit.communion_hymn)
ppt.add_title_slide('Communion')
ppt.add_call_and_response('Communion', lit.communion_blessing)
ppt.add_call_and_response('Prayer after Communion', lit.prayer_after_communion)
ppt.add_call_and_response('Benediction', lit.blessing)
ppt.add_hymn()
ppt.add_call_and_response('Dismissal', lit.dismissal)
ppt.add_image()
ppt.save()

doc = WordDocument(this_sunday)
doc.add_reading(sas.first_reading)
doc.add_psalm(sas.psalm)
doc.add_reading(sas.second_reading)
doc.save()

dbx = Dropbox(this_sunday)
dbx.upload('pptx')
dbx.upload('pdf')
dbx.close()