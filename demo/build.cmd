@echo off
setlocal
if "%1" == "" goto devmode
if "%1" == "release" goto release
:devmode
echo Building for development mode
set bbx_opts=-devMode
goto :build
:release
echo Building for release mode
set bbx_opts=-buildId _buildnum
goto :build
:build
call blackberry-pythonpackager -package demo.bar %bbx_opts% ^
    bar-descriptor.xml icon.png main.py bbxrun.py bbxpy/ scripts/ -C ../freetype-py-0.3.3 ../freetype-py-0.3.3/freetype
endlocal
