'''This is a stub routine to launch BB-Py apps.  The file is not intended
to be imported from the bbpy package, but rather is copied into the
.bar file as the main entry point.'''

import os
import sys
import importlib
import datetime as dt


if __name__ == '__main__':
    try:
        main = importlib.import_module(sys.argv[1])
        main.main()

    except SystemExit: # clean exit, let it pass
        print('clean exit:', dt.datetime.now(), file=sys.stderr)

    except: # anything else gets logged
        import traceback
        traceback.print_exc(file=sys.stderr)

    finally:
        print('done:', dt.datetime.now(), file=sys.stderr)

        sys.stderr.flush()
        sys.stdout.flush()

        # this is useful for troubleshooting problems with signed apps,
        # where you can't get to your own log file
        if '--savelogs' in sys.argv:
            sys.stdout.close()
            sys.stderr.close()

            # copy log over to shared/documents for viewing
            # For reasons now forgotten, we don't merely move the file, or
            # copy it with shutil.copyfile().  Could have been a one-time
            # issue and anyone's welcome to investigate this and improve it.
            import os
            dst = 'shared/documents/%s.log' % os.path.basename(os.getcwd()).rsplit('.', 1)[0]
            with open(dst, 'w') as copy, open('logs/log') as log:
                while 1:
                    data = log.read(65536)
                    if not data:
                        break
                    copy.write(data)

