import os
import sys
import signal
import time

import tart


class App(tart.Application):
    def onUiReady(self):
        self.onRefreshApps()


    def onSlayApp(self, pid):
        os.kill(pid, signal.SIGHUP)
        time.sleep(0.3)
        tart.send('appSlain', pid=pid)


    def onRefreshApps(self):
        apps = self.list_apps()
        tart.send('appsRefreshed', apps=apps)


    def list_apps(self):
        '''list all devmode apps that we can find'''
        apps = []
        mypid = os.getpid()
        tart.send('ownPid', pid=mypid)

        for pid in os.listdir('/proc'):
            try:
                pid = int(pid)
            except Exception:
                continue
            if pid == mypid:
                continue

            try:
                cmdline = open('/proc/{}/cmdline'.format(pid)).read().replace('\0', '\n')
            except IOError:
                pass
            else:
                exefile = open('/proc/{}/exefile'.format(pid)).read().rstrip('\0')
                # print('{}: {}'.format(pid, exefile))
                if not exefile.startswith('/accounts/1000/appdata'):
                    continue

                path = exefile.split('\n')[0]
                while path and path != '/':
                    parent = os.path.dirname(path)
                    if parent == '/accounts/1000/appdata':
                        break
                    path = parent

                name = os.path.basename(path)

                # find icon, if it's public
                iconpath = self.find_icon(path)
                info = {'pid': pid, 'name': name, 'iconpath': iconpath}
                print('info', info)
                apps.append(info)

        return sorted(apps, key=lambda x: x.get('name', ''))


    def find_icon(self, path):
        '''Unfortunately we can't read the MANIFEST.MF even for other devmode
        apps, so we have to guess for now (or use trickier approaches...).'''
        # print('find icon', path)
        icon = ''
        try:
            candidates = set()
            pubdir = os.path.join(path, 'app/public')
            for base, dirs, names in os.walk(pubdir):
                # print('walk', base, dirs, names)
                for name in names:
                    p = os.path.join(base, name)
                    if not os.path.isfile(p): continue
                    # print('file', p)
                    if not p.lower().endswith('.png'): continue
                    candidates.add(p)

            # for now, pick one at random
            if candidates:
                icon = list(candidates)[0]
                if len(candidates) > 1:
                    print('warning, multiple icon candidates ({}), picked only {}'.
                        format(len(candidates), icon))

        except Exception as ex:
            print('error', ex)
            raise

        return icon


# EOF
