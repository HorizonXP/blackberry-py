@echo off
if not "%1" == "" goto build
echo Specify path to your debugtoken .bar file as first argument.
goto done
:build
rem Note: this assumes you have unpacked the bbpy .tar.bz2 file into the
rem parent directory so there's a ..\blackberry-py folder there.
call blackberry-pythonpackager -package BBPyQMLViewer.bar ^
    -devMode ^
    -env PYTHONPATH=app/python/blackberry-py ^
    -env PYTHONDONTWRITEBYTECODE=1 ^
    -arg viewer.main ^
    bar-descriptor.xml ^
    viewer/ ^
    assets/*.png assets/*.jpg ^
    -e ../blackberry-py blackberry-py ^
    -e ../blackberry-py/bbpy/_main.py _main.py ^
    -debugToken %1
:done
