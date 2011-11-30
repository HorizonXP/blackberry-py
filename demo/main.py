# script runs with __name__ == '__main__'
# script runs with __file__ == 'app/python/main.py'
# os.getcwd() is '/accounts/1000/appdata/APPSANDBOXDIR'

if __name__ == '__main__':
    try:
        try:
            import bbxrun
            bbxrun.run()
        except SystemExit:
            pass
        except:
            import traceback
            traceback.print_exc()
            raise
    finally:
        import sys
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdout.close()
        sys.stderr.close()

        # copy log over to shared/documents for viewing
        import os
        dst = 'shared/documents/%s.log' % os.path.basename(os.getcwd()).rsplit('.', 1)[0]
        with open(dst, 'w') as copy, open('logs/log') as log:
            while 1:
                data = log.read(65536)
                if not data:
                    break
                copy.write(data)
