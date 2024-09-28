import os
import re
from datetime import date
from pathlib import Path
from typing import Optional

import requests
from boltons.iterutils import split
from bs4 import BeautifulSoup

from models.petition import Petition
from models.reading import Reading
from services.settings import Settings
from services.utils import clean_text


class SundaysAndSeasons:
    """Class for scraping Sundays and Seasons."""

    BASE = "https://members.sundaysandseasons.com"
    LOGIN = BASE + "/Account/Login"
    LOGOFF = BASE + "/Account/LogOff"
    HOME = BASE + "/Home/Index/{}/0#plans"

    PRAYER = re.compile(r"Prayer of the Day")
    PRAYER_ALTERNATE = re.compile(r"Prayer of the Day (Alternate)")
    FIRST_READING = re.compile(r"First Reading:")
    PSALM = re.compile(r"Psalm:")
    SECOND_READING = re.compile(r"Second Reading:")
    GOSPEL = re.compile(r"^Gospel:")
    PROCESSIONAL_GOSPEL = re.compile(r"Processional Gospel:")
    INTERCESSION = re.compile(r"Prayers of Intercession")

    READING_CALL = "The word of the Lord,"
    READING_RESPONSE = "<b>Thanks be to God.</b>"
    GOSPEL_CALL = "The gospel of the Lord,"
    GOSPEL_RESPONSE = "<b>Praise to you, O Christ.</b>"

    def __init__(self, settings: Settings):
        self.day: date = date.today()
        self._session: requests.Session = requests.Session()
        self._username: str = settings.USER
        self._password: str = settings.PASSWORD
        self._path: Path = f"{settings.LOCAL_DIR}/services"
        self._page: str = 0
        self._texts_url: str = (
            SundaysAndSeasons.BASE + "/Home/TextsAndResources/{}/{}#texts"
        )
        self._slides_url: str = (
            SundaysAndSeasons.BASE + "/Visuals/Index/{}/{}#projectable"
        )
        self._clipart_url: str = SundaysAndSeasons.BASE + "/Visuals/Index/{}/{}#clipart"

        self.title: str
        self.prayer: str
        self.prayer_alternate: str
        self.first_reading: Reading
        self.psalm: Reading
        self.second_reading: Reading
        self.gospel: Reading
        self.processional_gospel: Reading
        self.intercession: Petition

    def login(self, url: str = LOGIN) -> None:
        """Login to the Sundays and Seasons website"""
        key, value = self._get_token(url)
        payload = {
            key: value,
            "UserName": self._username,
            "Password": self._password,
        }
        req = self._session.post(url, data=payload)
        if req.status_code != 200:
            raise Exception("Login failed")

    def logoff(self, url: str = LOGOFF) -> None:
        """Logoff from the Sundays and Seasons website"""
        req = self._session.get(url)
        if req.status_code != 200:
            raise Exception("Logoff failed")

    def get_texts_and_images(self, processional_gospel: bool = False) -> None:
        """Get all the data for the current date"""
        self._get_title_and_url()
        self._get_texts(processional_gospel)
        self._get_slide()

    # region Private Methods

    def _get_token(self, url: str = LOGIN) -> tuple[str, str]:
        """Get the token from the login form"""
        html = self._session.get(url)
        soup = BeautifulSoup(html.text, "html.parser")
        login_form = soup.find(id="loginForm").form.find_all("input")[0]
        key, value = login_form["name"], login_form["value"]
        return key, value

    def _get_title_and_url(self, url: str = HOME):
        req = self._session.get(url.format(self.day))
        soup = BeautifulSoup(req.text, "html.parser")
        html = soup.body.find("div", {"id": "ribbondescription"})

        if link := html.find("a"):
            self._page = link.get("href").split("/")[-1]
            self.title = link.get_text()
        else:
            self.title = html.find("h3").get_text()

    def _get_texts(
        self, processional_gospel: bool = False, alternate_prayer: bool = False
    ) -> None:
        """Get all the texts for the current date"""
        req = self._session.get(self._texts_url.format(self.day, self._page))
        soup = BeautifulSoup(req.text, "html.parser")

        self.prayer = self._get_prayer(soup, SundaysAndSeasons.PRAYER)
        self.first_reading = self._get_reading(
            soup,
            SundaysAndSeasons.FIRST_READING,
            SundaysAndSeasons.READING_CALL,
            SundaysAndSeasons.READING_RESPONSE,
        )
        self.psalm = self._get_psalm(soup)
        self.second_reading = self._get_reading(
            soup,
            SundaysAndSeasons.SECOND_READING,
            SundaysAndSeasons.READING_CALL,
            SundaysAndSeasons.READING_RESPONSE,
        )
        self.gospel = self._get_reading(
            soup,
            SundaysAndSeasons.GOSPEL,
            SundaysAndSeasons.GOSPEL_CALL,
            SundaysAndSeasons.GOSPEL_RESPONSE,
        )
        self.intercession = self._get_intercession(soup)

        if processional_gospel:
            self.processional_gospel = self._get_reading(
                soup,
                SundaysAndSeasons.PROCESSIONAL_GOSPEL,
                SundaysAndSeasons.GOSPEL_CALL,
                SundaysAndSeasons.GOSPEL_RESPONSE,
            )

        if alternate_prayer:
            self.prayer_alternate = self._get_prayer(
                soup, SundaysAndSeasons.PRAYER_ALTERNATE
            )

    def _get_slide(self, base: str = BASE) -> None:
        """Get the main slide in a soup object"""
        req = self._session.get(self._slides_url.format(self.day, self._page))
        soup = BeautifulSoup(req.text, "html.parser")
        parent = soup.body.find("div", {"id": "toggle-btn-panel-projectable"})
        children = parent.find_all_next("img")
        for img in children:
            if not img.has_attr("title"):
                continue

            title = img["title"]
            if "Slide 1" in title and "(wide screen)" not in title:
                file = img["data-download"]
                url = base + file

                if not os.path.exists(f"{self._path}/{self.day}"):
                    os.makedirs(f"{self._path}/{self.day}")

                with open(f"{self._path}/{self.day}/image.ppt", "wb") as f:
                    f.write(self._session.get(url).content)

                os.system(
                    f"soffice --headless --invisible --convert-to pptx --outdir "
                    f"{self._path}/{self.day} {self._path}/{self.day}/image.ppt"
                )
                os.remove(f"{self._path}/{self.day}/image.ppt")

    # endregion Private Methods

    # region Static Methods

    @staticmethod
    def _get_prayer(soup: BeautifulSoup, regex: re.Pattern[str]) -> str:
        """Get the prayer of the day in a soup object"""
        parent = soup.body.find(string=regex).parent
        text = parent.findNext("div", {"class": "body"}).get_text().strip()
        return "Let us pray.\n" + "\n".join(
            [f"<b>{line}</b>" for line in text.splitlines()]
        )

    @staticmethod
    def _get_reading(
        soup: BeautifulSoup,
        regex: re.Pattern[str],
        call: Optional[str],
        response: Optional[str],
    ) -> Reading:
        """Get the first reading in a soup object"""
        parent = soup.find("h3", string=regex)
        reading = parent.find_next_sibling().find_next_sibling()
        title = re.split(regex, parent.get_text())[1].strip()

        for br in reading.find_all("br"):
            br.replace_with("\n")
        superscripts = SundaysAndSeasons._get_superscripts(reading)
        text = SundaysAndSeasons._add_superscripts(
            "\n".join(
                [clean_text(ele) for ele in reading.get_text().splitlines() if ele]
            ),
            superscripts,
        )

        return Reading(
            title=title, body="\n".join([text, "<div>", call, response, "</div>"])
        )

    @staticmethod
    def _get_psalm(soup: BeautifulSoup, regex: re.Pattern[str] = PSALM) -> None:
        """Get the psalm in a soup object"""
        parent = soup.find("h3", string=regex)
        title = parent.get_text().split("Psalm: ")[1]
        psalm = parent.find_next_sibling().find_next_sibling()

        for br in psalm.find_all("br"):
            br.replace_with("\n")
        superscripts = SundaysAndSeasons._get_superscripts(psalm)
        text = SundaysAndSeasons._add_superscripts(
            "\n".join(
                [
                    clean_text(span.get_text())
                    for span in psalm.find_all("span", {"class": None})
                    if span.get_text() and "style" not in span.attrs
                ]
            ),
            superscripts,
        )

        bold_text = [
            clean_text(strong.get_text()) for strong in psalm.find_all("strong")
        ]
        formatted_text = []
        for i, line in enumerate(text.splitlines()):
            if line.replace("<sup>", "").replace("</sup>", "") in superscripts:
                try:
                    if (
                        text.splitlines()[i + 1] in bold_text
                        or text.splitlines()[i - 1] in bold_text
                        and i != 0
                    ):
                        formatted_text.append(None)
                except IndexError:
                    pass
                formatted_text.append(line)
            else:
                formatted_text.append(line)

        body = []
        for i, line in enumerate(split(formatted_text, lambda x: x is None)):
            if line:
                new_line = SundaysAndSeasons._remove_whitespace(
                    f"{line[0]}{' '.join(line[1:])}"
                )
                if i % 2 == 0:
                    body.append(f"<div>\n{new_line}\n</div>")
                else:
                    body.append(f"<div>\n<b>{new_line}</b>\n</div>")

        return Reading(title=title, body="\n".join(body))

    @staticmethod
    def _get_intercession(
        soup: BeautifulSoup, regex: re.Pattern[str] = INTERCESSION
    ) -> Petition:
        """Get the intercessions in a soup object"""
        parent = soup.find("h3", string=regex)
        if parent:
            children = parent.find_all_next("div", {"class": "body"})[1].find_all(
                "div"
            )[:2]
            p = (pastor := children[0].get_text())[pastor.rfind(". ") :].split(". ")[1]
            c = children[1].get_text().strip()
            return Petition(call=p, response=c)
        else:
            return Petition(call="Lord, in your mercy,", response="hear our prayer.")

    @staticmethod
    def _get_superscripts(soup: BeautifulSoup) -> list[str]:
        """Get the superscripts in a soup object"""
        superscripts = [s.get_text() for s in soup.find_all("sup", {"class": None})]

        for i, s in enumerate(superscripts):
            if ":" in s:
                superscripts[i] = f"{s}{superscripts[i + 1]}"
                superscripts.pop(i + 1)

        return superscripts

    @staticmethod
    def _add_superscripts(text: str, superscripts: list) -> str:
        """Finds the superscripts in a text string and surrounds them with the html
        superscript tag, which is later used to format the text in the powerpoint slides.

        Args:
            text (str): The line of text to search for superscripts.
            superscripts (list): The list of superscripts to search for.

        Returns:
            str: The original text with <sup></sup> tags surrounding the superscripts.
        """

        def find_superscript(text: str, superscript: str, start: int = 0):
            """Find the start and end index of a superscript in a string"""
            length = len(superscript)
            index = text.find(superscript, start)
            return index, index + length

        start = 0
        new_text = ""
        for superscript in superscripts:
            indeces = find_superscript(text, superscript, start)
            new_text += text[start : indeces[0]] + f"<sup>{superscript}</sup>"
            start = indeces[1]
        new_text += text[start:]
        return new_text

    @staticmethod
    def _remove_whitespace(text: str) -> str:
        """Remove whitespace between superscripts and text"""
        return re.sub(r"(?<=<\/sup>)\s+", "", text)

    # endregion Static Methods
