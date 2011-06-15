#!/bin/sh

python setup.py sdist --formats=gztar register upload
python setup.py bdist --formats=wininst --plat-name=win32 upload
