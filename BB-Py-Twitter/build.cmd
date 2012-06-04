@echo off
call blackberry-pythonpackager -package BBPyTwitter.bar ^
    -devMode ^
    -env PYTHONPATH=shared/misc/blackberry-py:shared/misc/twitter ^
    -arg bbpy_twitter.main ^
    bar-descriptor.xml ^
    -e ../blackberry-py/bbpy/_main.py _main.py ^
    assets/*.png assets/*.sci ^
    -debugToken \svn\hg\prj246-playbook\debugtoken.bar
:done
