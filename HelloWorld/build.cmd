@echo off
if not "%1" == "" goto package
echo Specify debug token .bar file as first argument.
goto done
:package
call blackberry-pythonpackager -package HelloWorld.bar -devMode ^
    -debugToken %1 ^
    -env PYTHONPATH=app/python/blackberry-py ^
    bar-descriptor.xml ^
    main.py main.qml ^
    -e ../assets/icon.png icon.png ^
    -e ../blackberry-py/ blackberry-py/ ^
    -e ../bbpy/ blackberry-py/bbpy
rem    -env PYTHONPATH=shared/misc/blackberry-py:shared/misc ^
:done
