'''This is a stub routine to launch BB-Py apps.  The file is not intended
to be imported from the bbpy package, but rather is copied into the
.bar file as the main entry point.'''

import sys
import importlib

if __name__ == '__main__':
    main = importlib.import_module(sys.argv[1])
    main.main()
