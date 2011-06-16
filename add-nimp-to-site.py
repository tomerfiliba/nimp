#!/usr/bin/env python
"""
This script adds the following two lines to your ``site.py`` ::

  import nimp
  nimp.install()

This enables the use of nested packages "out of the box". 
If the lines already exist in your ``site.py``, this script will not do anything.

.. note::
   You'll probably need to ``sudo`` this script in order to update ``site.py``
"""
import inspect
import site


site_file = inspect.getsourcefile(site)
f = open(site_file, "r")
data = f.read()
f.close()

if "import nimp" not in data:
    lines = data.splitlines()
    ind = lines.index("if __name__ == '__main__':")
    lines.insert(ind, "\n# enable nested packages support\nimport nimp\nnimp.install()\n\n")
    data = "\n".join(lines)
    #print data
    f = open(site_file, "w")
    f.write(data)
    f.close()
    print ("added to site.py (%s)" % (site_file,))
else:
    print ("already installed in %s" % (site_file,))
