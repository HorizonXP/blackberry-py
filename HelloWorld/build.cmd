@echo off
if not "%1" == "" goto package
echo Specify debug token .bar file as first argument.
goto done
:package
call blackberry-pythonpackager -package HelloWorld.bar -devMode ^
    -debugToken %1 ^
    bar-descriptor.xml ^
    -e ../assets/icon.png icon.png^
    blackberry-py/ ^
    main.py main.qml
:done
