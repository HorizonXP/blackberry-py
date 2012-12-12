@echo off
echo Remember to turn on ACCESS_SHARED!
if not exist _buildId echo 0>_buildId
call blackberry-nativepackager -package ZombieSlayer.bar ^
    -configuration Device-Debug ^
    -devMode ^
    -target bar ^
    -env PYTHONPATH=app/native:shared/misc/ZombieSlayer ^
    -env PYTHONDONTWRITEBYTECODE=1 ^
    -arg -qml -arg shared/misc/ZombieSlayer/assets/main.qml ^
    -arg app/native/blackberry_tart.py ^
    bar-descriptor.xml ^
    icon.png ^
    tart.cfg ^
    -C ../tart/entry ../tart/entry/TartStart ^
    -C ../tart/python ../tart/python/*.py ^
    -C ../tart/js ../tart/js/*.js ^
    -debugToken ..\debugtoken.bar
