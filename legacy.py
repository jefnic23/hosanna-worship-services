import os
from pathlib import Path

from pptx.enum.text import MSO_VERTICAL_ANCHOR

from models.enums.weekday import Weekday
from services.document import WordDocument
from services.dropbox import Dropbox
from services.hymns import Hymns
from services.liturgy import Liturgy
from services.powerpoint import PowerPoint
from services.settings import Settings
from services.sundaysandseasons import SundaysAndSeasons
from services.utils import get_day

settings = Settings()
hymnal = Hymns()
lit = Liturgy(settings)
sas = SundaysAndSeasons(settings)
ppt = PowerPoint(settings)
doc = WordDocument(settings)
# dbx = Dropbox(settings)


if __name__ == "__main__":
    # dbx.connect()
    sas.login()

    hymn_list = [
        [532, 414, 434],
    ]

    for i, hymns in enumerate(hymn_list):
        day = get_day(delta=i, weekday=Weekday.SUNDAY)

        path = Path(settings.LOCAL_DIR, "services")
        if not os.path.exists(f"{path}/{day}"):
            os.makedirs(f"{path}/{day}")

        lit.load_files("Pentecost")

        first_hymn = hymnal.get_hymn(hymns[0])
        second_hymn = hymnal.get_hymn(hymns[1])
        third_hymn = hymnal.get_hymn(hymns[2])

        # dbx.day = day
        doc.day = day
        ppt.day = day
        sas.day = day

        sas.get_texts_and_images()

        # region Build PowerPoint

        ppt.convert_image()
        ppt.add_image()
        ppt.add_rich_text("Confession and Forgiveness", lit.confession)
        ppt.add_hymn(first_hymn)
        ppt.add_rich_text("Greeting", lit.greeting)
        ppt.add_rich_text("Hymn of Praise", lit.kyrie, spoken=True)
        ppt.add_rich_text("", lit.lord_be_with_you, anchor=MSO_VERTICAL_ANCHOR.MIDDLE)
        ppt.add_rich_text("Prayer of the Day", sas.prayer)
        ppt.add_title_slide(sas.first_reading.title)
        ppt.add_rich_text("First Reading", sas.first_reading.body)
        ppt.add_title_slide(sas.psalm.title)
        ppt.add_rich_text("Psalm", sas.psalm.body)
        ppt.add_title_slide(sas.second_reading.title)
        ppt.add_rich_text("Second Reading", sas.second_reading.body)
        ppt.add_rich_text("Gospel Acclamation", lit.gospel_acclamation, spoken=True)
        ppt.add_gospel_title(sas.gospel.title)
        ppt.add_rich_text("Gospel", sas.gospel.body)
        ppt.add_title_slide("Sermon")
        ppt.add_hymn(second_hymn)
        ppt.add_rich_text("Apostles' Creed", lit.apostles_creed, spoken=True)
        ppt.add_intercessions("Lord, in your mercy,", "hear our prayer.")
        ppt.add_rich_text("Dialogue", lit.dialogue, anchor=MSO_VERTICAL_ANCHOR.MIDDLE)
        ppt.add_rich_text("Preface", lit.preface)
        ppt.add_rich_text("Holy, holy, holy", lit.canticle, spoken=True)
        ppt.add_rich_text("Thanksgiving", lit.thanksgiving)
        ppt.add_rich_text("Lord's Prayer", lit.lords_prayer, spoken=True)
        ppt.add_title_slide("Communion")
        ppt.add_rich_text("Communion Hymn", lit.communion_hymn, spoken=True)
        ppt.add_title_slide("Communion")
        ppt.add_rich_text("Communion", lit.communion_blessing)
        ppt.add_rich_text("Prayer after Communion", lit.prayer_after_communion)
        ppt.add_rich_text("Blessing", lit.blessing)
        ppt.add_hymn(third_hymn)
        ppt.add_rich_text("Dismissal", lit.dismissal, anchor=MSO_VERTICAL_ANCHOR.MIDDLE)
        ppt.add_image()
        ppt.save(sas.title)
        ppt.reset()

        # endregion

        # region Generate Readings

        doc.add_rich_text(
            title=f"First Reading: {sas.first_reading.title}",
            body=sas.first_reading.body,
            keep_together=True,
        )
        doc.add_rich_text(
            title=sas.psalm.title, body=sas.psalm.body, keep_together=True
        )
        doc.add_rich_text(
            title=f"Second Reading: {sas.second_reading.title}",
            body=sas.second_reading.body,
            keep_together=True,
        )
        doc.save(filename="Readings", convert_to_pdf=True)
        doc.reset()

        # endregion

        # region Print Service

        doc.add_rich_text(title="Prelude", body=None, highlight_title=True)
        doc.add_rich_text(title="Confession and Forgiveness", body=lit.confession)
        doc.add_rich_text(
            title=f"Hymn: {first_hymn.title}, ELW {first_hymn.number}",
            body=None,
            highlight_title=True,
        )
        doc.add_rich_text(title="Greeting", body=lit.greeting)
        doc.add_rich_text(title="Kyrie", body=None, highlight_title=True)
        doc.add_rich_text(title=None, body=lit.lord_be_with_you)
        doc.add_rich_text(title="Prayer of the Day", body=sas.prayer)
        doc.add_rich_text(
            title=f"First Reading: {sas.first_reading.title}",
            body=sas.first_reading.body,
        )
        doc.add_rich_text(title=sas.psalm.title, body=sas.psalm.body)
        doc.add_rich_text(
            title=f"Second Reading: {sas.second_reading.title}",
            body=sas.second_reading.body,
        )
        doc.add_rich_text(title="Gospel Acclamation", body=None, highlight_title=True)
        doc.add_rich_text(
            title=f"Gospel Reading: {sas.gospel.title}", body=sas.gospel.body
        )
        doc.add_rich_text(title="Sermon", body=None)
        doc.add_rich_text(
            title=f"Hymn: {second_hymn.title}, ELW {second_hymn.number}",
            body=None,
            highlight_title=True,
        )
        doc.add_rich_text(title="Apostles' Creed", body=lit.apostles_creed)
        doc.add_rich_text(title="Prayers of Intercession", body=None)
        doc.add_rich_text(title="Dialogue", body=lit.dialogue)
        doc.add_rich_text(title="Preface", body=lit.preface)
        doc.add_rich_text(title="Holy, holy, holy", body=None, highlight_title=True)
        doc.add_rich_text(title="Lord's Prayer", body=lit.lords_prayer)
        doc.add_rich_text(title="Communion", body=None, highlight_title=True)
        doc.add_rich_text(title="Communion Blessing", body=lit.communion_blessing)
        doc.add_rich_text(
            title="Prayer after Communion", body=lit.prayer_after_communion
        )
        doc.add_rich_text(title="Blessing", body=lit.blessing)
        doc.add_rich_text(
            title=f"Hymn: {third_hymn.title}, ELW {third_hymn.number}",
            body=None,
            highlight_title=True,
        )
        doc.add_rich_text(title="Dismissal", body=lit.dismissal)
        doc.save(filename=sas.title, convert_to_pdf=True)
        doc.reset()

        # endregion

        # dbx.upload(f"{sas.title}.docx")
        # dbx.upload(f"{sas.title}.pptx")

    sas.logoff()
    # dbx.close()
