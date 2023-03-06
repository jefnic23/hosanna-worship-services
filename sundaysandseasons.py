import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


class SundaysAndSeasons():
    '''Class for scraping Sundays and Seasons'''

    BASE = 'https://members.sundaysandseasons.com'
    LOGIN = BASE + '/Account/Login'
    LOGOFF = BASE + '/Account/LogOff'
    TEXTS = BASE + '/Home/TextsAndResources/{}/0#texts'
    SLIDES = BASE + '/Visuals/Index/{}/0#projectable'

    PRAYER = 'Prayer of the Day'
    READINGS = 'Readings and Psalm'
    INTERCESSION = 'Prayers of Intercession'


    # TODO: error handling

    def __init__(self, day):
        load_dotenv()
        self._session = requests.Session()
        self._username = os.getenv('user')
        self._password = os.getenv('password')
        self._day = day

        self.title = None
        self.prayer = None
        self.readings = []
        self.intercession = None


    def login(self, url=LOGIN):
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
        

    def logoff(self, url=LOGOFF):
        '''Logoff from the Sundays and Seasons website'''
        req = self._session.get(url)
        if req.status_code != 200:
            raise Exception('Logoff failed')
        

    def get_readings_and_slide(self):
        '''Get all the data for the current date'''
        self._get_all_texts()
        self._get_slide()
        

    def _get_token(self, url=LOGIN):
        '''Get the token from the login form'''
        html = self._session.get(url)
        soup = BeautifulSoup(html.text, 'html.parser')
        login_form = soup.find(id='loginForm').form.find_all('input')[0]
        key, value = login_form['name'], login_form['value']
        return key, value
        

    def _get_all_texts(self, url=TEXTS):
        '''Get all the texts for the current date'''
        req = self._session.get(url.format(self._day))
        soup = BeautifulSoup(req.text, 'html.parser')
        self._get_prayer(soup)
        self._get_readings(soup)
        self._get_intercession(soup)


    def _get_title(self, soup):
        '''Get the title of the day in a soup object'''
        self.title = soup.body.find('h1', {'id': 'ribbontitle'}).get_text().strip()


    def _get_prayer(self, soup):
        '''Get the prayer of the day in a soup object'''
        parent = soup.body.find(text=SundaysAndSeasons.PRAYER).parent
        self.prayer = parent.findNext('div', {'class': 'body'}).get_text().strip()


    def _get_readings(self, soup):
        '''Get the readings and psalm in a soup object'''
        parent = soup.body.find(text=SundaysAndSeasons.READINGS).parent
        headings = parent.find_all_next('a', {'class': 'scripture'})[:4]
        intros = parent.find_all_next('div', {'class': 'reading_intro'})
        # TODO: omit <span class="refrain"> from psalm
        for i in range(len(headings)):
            reading = [headings[i].get_text().strip(), intros[i].find_next_sibling().get_text().strip()]
            self.readings.append(reading)


    def _get_intercession(self, soup):
        '''Get the intercessions in a soup object'''
        parent = soup.body.find(text=SundaysAndSeasons.INTERCESSION).parent
        children = parent.find_all_next('div', {'class': 'body'})[1].find_all('div')[:2]
        p = (pastor := children[0].get_text())[pastor.rfind('. '):].split('. ')[1]
        c = children[1].get_text().strip()
        self.intercession = [p, c]


    def _get_slide(self, url=SLIDES):
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
                url = SundaysAndSeasons.BASE + file
                
                if not os.path.exists(f'services/{self._day}'):
                    os.makedirs(f'services/{self._day}')

                with open(f'services/{self._day}/service.ppt', 'wb') as f:
                    f.write(self._session.get(url).content)

                os.system(f'soffice --headless --invisible --convert-to pptx --outdir services/{self._day} services/{self._day}/service.ppt')
                os.remove(f'services/{self._day}/service.ppt')
                    