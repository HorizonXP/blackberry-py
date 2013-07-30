
import os
import sys
import glob
from urllib.request import urlopen
import sqlite3
import time
import uuid
import traceback

import feedparser

import tart

URLFEED = 'http://cuteoverload.com/feed/'
DATABASE = 'data/data.db'
IMAGEDIR = 'data/images'

MAKE_SCHEMA = '''CREATE TABLE IF NOT EXISTS entries (
    url     TEXT PRIMARY KEY,
    title   TEXT,
    pubtime INTEGER,
    image   TEXT,
    summary TEXT,
    tags    TEXT
    )
'''

LOAD_ENTRIES = '''SELECT * FROM entries'''
ADD_ENTRY = '''INSERT INTO entries VALUES (:url, :title, :pubtime, :image, :summary, :tags)'''


def dict_factory(cursor, row):
    '''Create dictionary from database result row.'''
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class App(tart.Application):
    STATE_FILE = 'data/app.state'


    def __init__(self):
        super().__init__(debug=True)   # set True for some extra debug output

        self.state = {
            'last_checked': 0,
            'last_published': 0,
            'site_url': '',
            }
        self.restore_data(self.state, self.STATE_FILE)

        self.entries = {}


    def onUiReady(self):
        print('UI is ready')

        tart.send('siteUrl', url=self.state['site_url'])
        self.reloadEntries()


    def onManualExit(self):
        self.save_data(self.state, self.STATE_FILE)

        try:
            # clean up unused images
            existing = set(os.listdir(IMAGEDIR))
            used = {os.path.basename(x['image']) for x in self.entries.values()}
            unused = existing - used
            print('removing unused:', len(unused))
            for path in unused:
                os.remove(os.path.join(IMAGEDIR, path))

        finally:
            super().onManualExit()


    def reloadEntries(self):
        self.db = sqlite3.connect(DATABASE)

        self.db.row_factory = dict_factory

        with self.db:
            self.db.execute(MAKE_SCHEMA)

        with self.db:
            entries = list(self.db.execute(LOAD_ENTRIES))
            tart.send('entriesLoaded', entries=entries)

            for entry in entries:
                self.entries[entry['url']] = entry


    def onRefreshFeed(self, url=URLFEED):
        try:
            feed = feedparser.parse(url)
            if feed.status == 200:
                count = self.parseFeed(feed)
                if not count:
                    tart.send('noEntriesFound')

        except Exception as ex:
            tart.send('pyError', traceback=traceback.format_exc())


    def parseFeed(self, feed):
        print('parsing', feed.feed.title, feed.updated)
        self.state['last_published'] = time.mktime(feed.updated_parsed)
        self.state['last_checked'] = time.time()
        url = self.state['site_url'] = feed.feed.link
        tart.send('siteUrl', url=url)

        print('found entries:', len(feed.entries))
        count = 0
        for item in feed.entries:
            # ignore ones we've already seen
            if item.link in self.entries:
                print('ignoring, known', item.link)
                continue

            count += 1
            imagepath = self.addImage(item)
            tags = {x.term for x in item.tags} - {'Uncategorized'}
            entry = {
                'url': item.link,
                'title': item.title,
                'pubtime': time.mktime(item.published_parsed),
                'image': imagepath,
                'summary': item.summary.split('Filed under')[0].strip(),
                'tags': ', '.join(sorted(tags)),
                }

            self.addEntry(entry)
            self.entries[entry['url']] = entry

        return count


    def addEntry(self, entry):
        print('adding entry')
        with self.db:
            self.db.execute(ADD_ENTRY, entry)

        tart.send('entryAdded', entry=entry)


    EXTENSIONS = {
        'image/jpeg': '.jpg',
        'image/png': '.png',
    }

    def addImage(self, item):
        if not os.path.exists(IMAGEDIR):
            os.makedirs(IMAGEDIR)

        for img in item.media_content:
            if 'cuteoverload.files' in img['url']:
                url = urlopen(img['url'])
                if url.status != 200:
                    print('cannot load', url.url)
                    continue

                print('loading', url.url)
                data = url.read()

                mimetype = url.headers['content-type']
                fname = str(uuid.uuid4()) + self.EXTENSIONS.get(mimetype, '.jpg')
                path = os.path.join(IMAGEDIR, fname)
                print('save image', path, 'length', len(data))
                with open(path, 'wb') as f:
                    f.write(data)

                return os.path.abspath(path)

        return ''


    def onEraseData(self):
        self.db.close()
        os.remove(DATABASE)
        self.state.clear()
        self.reloadEntries()    # recreate database, empty


    def onFakeNew(self):
        entry = {
            'url': '',
            'title': 'A faked entry',
            'pubtime': time.time(),
            'image': '',
            'summary': 'This entry was faked',
            'tags': 'Faked,Totally',
            }
        tart.send('entryAdded', entry=entry)
