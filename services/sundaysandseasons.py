import os
import re
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from config import settings
from services.utils import clean_text, grouper


class SundaysAndSeasons():
    '''Class for scraping Sundays and Seasons.'''

    BASE = 'https://members.sundaysandseasons.com'
    LOGIN = BASE + '/Account/Login'
    LOGOFF = BASE + '/Account/LogOff'
    TEXTS = BASE + '/Home/TextsAndResources/{}/0#texts'
    SLIDES = BASE + '/Visuals/Index/{}/0#projectable'
    CLIPART = BASE + '/Visuals/Inde/{}/0#clipart'

    PRAYER = 'Prayer of the Day'
    FIRST_READING = re.compile(r'First Reading:')
    PSALM = re.compile(r'Psalm:')
    SECOND_READING = re.compile(r'Second Reading:')
    GOSPEL = re.compile(r'^Gospel:')
    INTERCESSION = re.compile(r'Prayers of Intercession')

    READING_CALL = 'The word of the Lord,'
    READING_RESPONSE = 'Thanks be to God.'
    GOSPEL_CALL = 'The gospel of the Lord,'
    GOSPEL_RESPONSE = 'Praise to you, O Christ.'


    # TODO: error handling

    def __init__(
        self, 
        day: date,
        path: Path = Path('D:/Documents/Hosanna/services')
    ):
        self._session: requests.Session = requests.Session()
        self._username: str = settings.USER
        self._password: str = settings.PASSWORD
        self._day: date = day
        self._path: Path = path

        self.title: str = ''
        self.prayer: str = ''
        self.first_reading: str = ''
        self.psalm: str = ''
        self.second_reading: str = ''
        self.gospel: str = ''
        self.intercession: str = ''

        self._login()


    def _login(self, url: str = LOGIN) -> None:
        '''Login to the Sundays and Seasons website'''
        key, value = self._get_token(url)
        payload = {
            key: value,
            'UserName': self._username,
            'Password': self._password,
        }
        req = self._session.post(url, data=payload)
        if req.status_code != 200:
            raise Exception('Login failed')
        

    def logoff(self, url: str = LOGOFF) -> None:
        '''Logoff from the Sundays and Seasons website'''
        req = self._session.get(url)
        if req.status_code != 200:
            raise Exception('Logoff failed')
        

    def get_texts_and_images(self) -> None:
        '''Get all the data for the current date'''
        self._get_texts()
        self._get_slide()
        

    def _get_token(self, url: str = LOGIN) -> tuple[str, str]:
        '''Get the token from the login form'''
        html = self._session.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        login_form = soup.find(id='loginForm').form.find_all('input')[0]
        key, value = login_form['name'], login_form['value']
        return key, value
        

    def _get_texts(self, url: str = TEXTS) -> None:
        '''Get all the texts for the current date'''
        req = self._session.get(url.format(self._day))
        soup = BeautifulSoup(req.text, 'html.parser')
        self._get_prayer(soup)
        self._get_readings(soup)
        self._get_psalm(soup)
        self._get_intercession(soup)


    def _get_title(self, soup: BeautifulSoup) -> None:
        '''Get the title of the day in a soup object'''
        self.title = soup.body.find('h1', {'id': 'ribbontitle'}).get_text().strip()


    def _get_prayer(self, soup: BeautifulSoup) -> None:
        '''Get the prayer of the day in a soup object'''
        parent = soup.body.find(text=SundaysAndSeasons.PRAYER).parent
        self.prayer = parent.findNext('div', {'class': 'body'}).get_text().strip()


    def _get_readings(self, soup: BeautifulSoup) -> None:
        '''Get the readings in a soup object'''
        self.first_reading = self._get_reading(
            soup, 
            SundaysAndSeasons.FIRST_READING, 
            SundaysAndSeasons.READING_CALL, 
            SundaysAndSeasons.READING_RESPONSE
        )
        self.second_reading = self._get_reading(
            soup, 
            SundaysAndSeasons.SECOND_READING, 
            SundaysAndSeasons.READING_CALL, 
            SundaysAndSeasons.READING_RESPONSE)
        self.gospel = self._get_reading(
            soup, 
            SundaysAndSeasons.GOSPEL, 
            SundaysAndSeasons.GOSPEL_CALL,
            SundaysAndSeasons.GOSPEL_RESPONSE)


    def _get_psalm(
        self, 
        soup: BeautifulSoup, 
        regex: re.Pattern[str] = PSALM
    ) -> None:
        '''Get the psalm in a soup object'''
        parent = soup.find('h3', string=regex)
        title = parent.get_text().split('Psalm: ')[1]

        psalm = parent.find_next_sibling().find_next_sibling()
        superscripts = SundaysAndSeasons._get_superscripts(psalm)
        spans = [
            clean_text(span.get_text()) 
            for span in psalm.find_all('span', {'class': None}) 
            if 'style' not in span.attrs
        ]

        text = []
        for span in spans:
            if span in superscripts:
                text.append(f'<sup>{span}</sup>')
            else:
                text.append(span)

        self.psalm = (
            title + 
            '\n' + 
            '\n'.join([' '.join(line) for line in grouper(text, 3)])
        )
        # TODO: refrain spans are nested; remove them


    def _get_intercession(
        self, 
        soup: BeautifulSoup, 
        regex: re.Pattern[str] = INTERCESSION
    ) -> None:
        '''Get the intercessions in a soup object'''
        parent = soup.find('h3', string=regex)
        children = parent.find_all_next('div', {'class': 'body'})[1].find_all('div')[:2]
        p = (pastor := children[0].get_text())[pastor.rfind('. '):].split('. ')[1]
        c = children[1].get_text().strip()
        self.intercession = p + '\n' + c


    def _get_slide(
        self, 
        url: str = SLIDES, 
        base: str = BASE
    ) -> None:
        '''Get the main slide in a soup object'''
        req = self._session.get(url.format(self._day))
        soup = BeautifulSoup(req.text, 'html.parser')
        parent = soup.body.find('div', {'id': 'toggle-btn-panel-projectable'})
        children = parent.find_all_next('img')
        for img in children:
            if not img.has_attr('title'):
                continue

            title = img['title']
            if 'Slide 1' in title and '(wide screen)' not in title:
                file = img['data-download']
                url = base + file
                
                if not os.path.exists(f'{self._path}/{self._day}'):
                    os.makedirs(f'{self._path}/{self._day}')

                with open(f'{self._path}/{self._day}/image.ppt', 'wb') as f:
                    f.write(self._session.get(url).content)

                os.system(
                    f'soffice --headless --invisible --convert-to pptx --outdir '
                    f'{self._path}/{self._day} {self._path}/{self._day}/image.ppt'
                )
                os.remove(f'{self._path}/{self._day}/image.ppt')


    @staticmethod
    def _get_reading(
        soup: BeautifulSoup, 
        regex: re.Pattern[str], 
        call: str, 
        response: str
    ) -> str:
        '''Get the first reading in a soup object'''
        parent = soup.find('h3', string=regex)
        reading = parent.find_next_sibling().find_next_sibling()
        title = re.split(regex, parent.get_text())[1].strip()
        
        superscripts = SundaysAndSeasons._get_superscripts(reading)
        text = SundaysAndSeasons._add_superscripts(
            '\n'.join([clean_text(ele) for ele in reading.get_text().splitlines()]),
            superscripts
        )
        return '\n'.join([title, text, call, response])
    
    
    @staticmethod
    def _get_superscripts(soup: BeautifulSoup) -> list[str]:
        '''Get the superscripts in a soup object'''
        superscripts = [
            s.get_text() for s in soup.find_all('sup', {'class': None})
        ]
        
        for i, s in enumerate(superscripts):
            if ':' in s:
                superscripts[i] = f'{s}{superscripts[i + 1]}'
                superscripts.pop(i + 1)
                
        return superscripts
    
    
    @staticmethod
    def _add_superscripts(text: str, superscripts: list) -> str:
        def find_superscript(text: str, superscript: str, start: int = 0):
            '''Find the start and end index of a superscript in a string'''
            length = len(superscript)
            index = text.find(superscript, start)
            return index, index + length

        start = 0
        new_text = ""
        for superscript in superscripts:
            indeces = find_superscript(text, superscript, start)
            new_text += text[start:indeces[0]] + f'<sup>{superscript}</sup>'
            start = indeces[1]
        new_text += text[start:]
        return new_text
