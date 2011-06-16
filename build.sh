#!/bin/sh

python setup.py register
python setup.py sdist --formats=gztar upload
python setup.py bdist --formats=wininst --plat-name=win32 upload
