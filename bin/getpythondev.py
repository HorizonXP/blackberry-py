#!/usr/bin/env python
'''Retrieve Python 3.2.2 source tarball and extract.'''

import sys
import os
import hashlib
import urllib.request
import tarfile

URL = 'http://python.org/ftp/python/3.2.2/Python-3.2.2.tgz'
HASH = '3c63a6d97333f4da35976b6a0755eb67'

def main():
    filename = os.path.basename(URL)

    folder = os.path.splitext(filename)[0]
    if os.path.exists(folder):
        sys.exit('folder already exists: {}'.format(folder))

    if not os.path.exists(filename):
        print('downloading ' + URL)
        resp = urllib.request.urlopen(URL)
        if resp.status != 200:
            sys.exit('unable to read ' + URL)

        data = resp.read()
        with open(filename, 'wb') as f:
            f.write(data)

    else:
        data = open(filename, 'rb').read()

    print('checking MD5 hash')
    hashval = hashlib.md5(data).hexdigest()
    if hashval != HASH:
        sys.exit('incorrect hash on {}: {}'.format(filename, hashval))

    print('extracting tarball')
    t = tarfile.open(filename)
    t.extractall()

    print('Python-3.2.2 folder created with Python source tree')


if __name__ == '__main__':
    main()
