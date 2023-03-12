from sundaysandseasons import SundaysAndSeasons
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
    with open('tests/readings.txt', 'r', encoding='utf-8') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')

    sas = SundaysAndSeasons('2023-03-26')
    text = sas._get_reading(soup, re.compile(r'^Gospel:'), '', '')

    print(text)