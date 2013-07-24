@echo off
SETLOCAL
SET mypath=%~dp0
rem echo %mypath:~0,-1%
SET PYTHONPATH=%mypath%;%PYTHONPATH%
call python -m tartutil %*
ENDLOCAL
