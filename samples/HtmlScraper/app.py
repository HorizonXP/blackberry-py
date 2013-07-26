
from urllib.request import urlopen
from bs4 import BeautifulSoup

import tart

URL = 'http://news.ycombinator.com/{}'

class App(tart.Application):
    def onRequestPage(self, source='news'):
        resp = urlopen(URL.format(source))
        body = resp.read().decode('utf-8')
        soup = BeautifulSoup(body)

        stories = []
        for item in soup.find_all('td', class_='title'):
            if item.a is not None:
                stories.append((item.a.string, item.a['href']))

        tart.send('addStories', stories=stories)
