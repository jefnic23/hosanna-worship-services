import os
from datetime import date

from hosanna.document import WordDocument
from hosanna.powerpoint import PowerPoint
from hosanna.sundaysandseasons import SundaysAndSeasons
from hosanna.utils import get_sunday


if __name__ == '__main__':
    # TODO: prompt to install libreoffice if it doesn't exist
    # https://www.libreoffice.org/download/download-libreoffice/

    # TODO: prompt to add hymns if they don't exist

    TODAY = date.today()
    this_sunday = get_sunday(TODAY)

    if not os.path.exists(f'services/{this_sunday}'):
        os.makedirs(f'services/{this_sunday}')

    sas = SundaysAndSeasons(this_sunday)
    sas.login()
    sas.get_texts_and_slide()
    sas.logoff()

    ppt = PowerPoint(this_sunday)
    ppt.add_image()
    ppt.add_call_and_response('Confession and Forgiveness', ppt._confession)
    ppt.add_hymn()
    ppt.add_call_and_response('Greeting', ppt._greeting)
    ppt.add_congregation_text('Kyrie', ppt._kyrie)
    ppt.add_congregation_text('Prayer of the Day', sas.prayer)
    ppt.add_reading('First Reading', sas.first_reading)
    ppt.add_psalm(sas.psalm)
    ppt.add_reading('Second Reading', sas.second_reading)
    ppt.add_congregation_text('Gospel Acclamation', ppt._gospel_acclamation)
    ppt.add_gospel(sas.gospel)
    ppt.add_title_slide('Sermon')
    ppt.add_hymn()
    ppt.add_congregation_text('Apostle\'s Creed', ppt._creed)
    ppt.add_intercessions(sas.intercession)
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

    doc = WordDocument(this_sunday)
    doc.add_reading(doc._first_reading)
    doc.add_psalm(doc._psalm)
    doc.add_reading(doc._second_reading)
    doc.save()
