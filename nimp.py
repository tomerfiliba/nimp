"""\
Allows nested imports, a la Java. Nimp installs a harmless meta import-hook that 
adds support for *nested packages*, i.e., multiple packages that "live" under a 
common namespace. This is the idiom in Java, where you have packages like 
``com.foo.bar.spam`` and ``com.foo.bar.eggs``, as well as in Haskell and several 
other languages. Nimp basically allows packages to "inject" themselves into 
shared namespaces.

Usage:
  import nimp
  nimp.install()

See http://pypi.python.org/pypi/nimp for more info.
"""
import os
import sys
import imp


class _Nimp(object):
    def __init__(self):
        self.cache = {}
    
    def _get_name_prefixes(self, name):
        if "-" in name:
            sep = "-"
        else:
            sep = "."
        i = -1
        while True:
            i = name.find(sep, i+len(sep))
            if i < 0:
                yield name
                break
            yield name[:i]
    
    def _find_all(self, fullname):
        assert fullname not in self.cache
        for path in sys.path:
            if not os.path.isdir(path):
                continue
            for fn in os.listdir(path):
                fullpath = os.path.join(path, fn)
                if not fn.startswith(fullname) or ("-" not in fn and "." not in fn):
                    continue
                if not os.path.isdir(fullpath):
                    continue
                for prefix in self._get_name_prefixes(fn):
                    fullpath = os.path.join(path, prefix)
                    modname = prefix.replace("-", ".")
                    if os.path.exists(fullpath):
                        if modname in self.cache and self.cache[modname] != fullpath:
                            raise ImportError("%r duplicated: %s and %s" % (modname, fullpath, self.cache[modname]))
                        self.cache[modname] = fullpath # real
                    elif modname not in self.cache:
                        self.cache[modname] = None # namespace only
    
    def clear_cache(self):
        self.cache.clear()
    
    def find_module(self, fullname, path=None):
        if fullname in self.cache:
            return self
        self._find_all(fullname)
        if fullname in self.cache:
            return self
        else:
            return None
    
    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        path = self.cache[fullname]
        
        # must insert to sys.modules first, to avoid cyclic imports
        try:
            imp.acquire_lock()
            mod = sys.modules[fullname] = imp.new_module(fullname)
            try:
                if path is None:
                    mod.__file__ = "<namespace module>"
                    mod.__path__ = []
                else:
                    info = imp.find_module(os.path.basename(path), [os.path.dirname(path)])
                    mod = imp.load_module(fullname, *info)
                    # replace the stub in sys.modules
                    sys.modules[fullname] = mod
            except Exception:
                del sys.modules[fullname]
                raise
        finally:
            imp.release_lock()
        
        return mod

# create Nimp singleton
the_nimp = _Nimp()
_installed = False

def install():
    """installs the nimp meta-importer hook; this enables the use of nested imports"""
    global _installed
    if _installed:
        return
    sys.meta_path.append(the_nimphttp://pypi.python.org/pypi/nimp)
    _installed = True

def uninstall():
    """removed the nimp meta-importer hook; nested imports will no longer be possible"""
    global _installed
    if not _installed:
        return
    sys.meta_path.remove(the_nimp)
    _installed = False




