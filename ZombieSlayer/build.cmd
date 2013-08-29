@echo off
echo Remember to turn on ACCESS_SHARED!
if not exist _buildId echo 0>_buildId
call blackberry-nativepackager -package ZombieSlayer.bar ^
    -configuration Device-Debug ^
    -devMode ^
    -target bar ^
    -env PYTHONPATH=shared/misc/tart/python:shared/misc/ZombieSlayer ^
    -env PYTHONDONTWRITEBYTECODE=1 ^
    -arg -qml -arg shared/misc/ZombieSlayer/assets/main.qml ^
    -arg shared/misc/tart/python/blackberry_tart.py ^
    bar-descriptor.xml ^
    icon.png ^
    -C ../tart/entry ../tart/entry/TartStart ^
    -debugToken ../debugtoken.bar
