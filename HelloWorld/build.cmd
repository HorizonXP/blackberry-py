@echo off
if not "%1" == "" goto package
echo Specify debug token .bar file as first argument.
echo If signing, also specify -sign -storepass XXX -cskpass XXX -buildId
goto done
:package
call blackberry-pythonpackager -package HelloWorld.bar ^
    -env PYTHONPATH=app/python/blackberry-py ^
    bar-descriptor.xml ^
    main.py main.qml ^
    -e ../assets/icon.png icon.png ^
    -e ../blackberry-py/ blackberry-py/ ^
    -debugToken %*
:done
