"""
Allows nested imports, a la Java. It installs a harmless meta import-hook that 
adds support for *nested packages*, i.e., multiple packages that "live" under a 
common namespace. This is the idiom in Java, where you have packages like 
``com.foo.bar.spam`` and ``com.foo.bar.eggs``, as well as in Haskell. 
Nimp basically allows packages to "inject" themselves into shared namespaces.

Compatible with Python 2.3 and up and 3.0 and up

Usage::

  import nimp
  nimp.install()

Example Layout
--------------
Assume the following directory structure, say, in your ``site-packages``::

  com.ibm.storage/
    files...
  com.ibm.storage.plugins/
    files...
  com.ibm.pythontools/
    files...

Using Nimp, the following imports will work as expected::
  
  import com                              # a namespace package (empty)
  import com.ibm                          # a namespace package (empty)
  import com.ibm.pythontools              # a real package
  com.ibm.pythontools.myfunc(1,2,3)
  
  # and of course using `from` works too
  from com.ibm.storage import ScsiDisk    
  
  # note how the `plugins` package was "injected" into `storage`
  from com.ibm.storage.plugins import MySQLPlugin
"""
import os
import sys
import imp


class Nimp(object):
    def __init__(self):
        self.cache = {}
    
    @staticmethod
    def _get_name_parts(dotted_name):
        i = -1
        while i is not None:
            i = dotted_name.find(".", i+1)
            if i < 0:
                i = None
            part = dotted_name[0:i]
            yield part
    
    def _find(self, fullname):
        if fullname in self.cache:
            return
        for path in sys.path:
            if not os.path.isdir(path):
                continue
            for fn in os.listdir(path):
                fullpath = os.path.join(path, fn)
                if not os.path.isdir(fullpath) or "." not in fn or not fn.startswith(fullname):
                    continue
                for part in self._get_name_parts(fn):
                    fullpath = os.path.join(path, part)
                    if part in self.cache:
                        if os.path.exists(fullpath):
                            self.cache[part] = fullpath # namespace + real
                        else:
                            self.cache[part] = None # namespace
                    else:
                        self.cache[part] = fullpath # real
    
    def clear_cache(self):
        self.cache.clear()
    
    def find_module(self, fullname, path=None):
        self._find(fullname)
        if fullname in self.cache:
            return self
        else:
            return None
    
    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        path = self.cache[fullname]
        # must insert to sys.modules first, to avoid cyclic imports
        mod = sys.modules[fullname] = imp.new_module(fullname)
        try:
            if path is None:
                mod.__file__ = "<namespace module>"
                mod.__path__ = []
            else:
                info = imp.find_module(fullname, [os.path.dirname(path)])
                # replace the stub in sys.modules
                mod = imp.load_module(fullname, *info)
                sys.modules[fullname] = mod
        except Exception:
            del sys.modules[fullname]
            raise
        return mod

# create Nimp singleton
Nimp = Nimp()
_installed = False

def install():
    global _installed
    if _installed:
        return
    sys.meta_path.append(Nimp)
    _installed = True

def uninstall():
    global _installed
    if not _installed:
        return
    sys.meta_path.remove(Nimp)
    _installed = False


