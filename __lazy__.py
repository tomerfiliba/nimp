import sys
from types import ModuleType

__path__ = []
LAZY_PREFIX = "__lazy__"

class OnDemandModule(ModuleType):
    def __init__(self, name):
        ModuleType.__init__(self, name)
        object.__setattr__(self, "__module", None)
    def _get_module(self):
        if object.__getattribute__(self, "__module"):
            return object.__getattribute__(self, "__module")
        mod = __import__(self.__name__, None, None, "*")
        object.__setattr__(self, "__module", mod)
        object.__setattr__(self, "__doc__", mod.__doc__)
        object.__setattr__(self, "__file__", mod.__file__)
        if hasattr(mod, "__path__"):
            object.__setattr__(self, "__path__", mod.__path__)
        return mod
    def __dir__(self):
        return dir(self._get_module())
    def __repr__(self):
        if object.__getattribute__(self, "__module"):
            return repr(self._get_module())
        else:
            return "<%s '%s'>" % (self.__class__.__name__, self.__name__)
    def __getattr__(self, name):
        return getattr(self._get_module(), name)
    def __delattr__(self, name):
        return delattr(self._get_module(), name)
    def __setattr__(self, name, value):
        return setattr(self._get_module(), name, value)

class LazyImporter(object):
    def find_module(self, fullname, path = None):
        if fullname.startswith(LAZY_PREFIX + "."):
            return self
        else:
            return None
    def load_module(self, fullname):
        realname = fullname[len(LAZY_PREFIX) + 1:]
        if realname in sys.modules:
            return sys.modules[realname]
        if fullname in sys.modules:
            return sys.modules[fullname]
        mod = sys.modules[fullname] = OnDemandModule(realname)
        return mod

_the_lazy_importer = LazyImporter()
sys.meta_path.append(_the_lazy_importer)


