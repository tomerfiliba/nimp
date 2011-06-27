import sys
from types import ModuleType

class NormalModule(ModuleType):
    pass

class OnDemandModule(ModuleType):
    def __repr__(self):
        return "<lazy module %r>" % (ModuleType.__getattribute__(self, "__name__"),)
    def __strict__(self):
        ModuleType.__setattr__(self, "__class__", NormalModule)
        if "." in self.__name__:
            parent_name, leaf_name = self.__name__.rsplit(".", 1)
            parent = sys.modules[parent_name]
            setattr(parent, leaf_name, self) # this will __strict__ the parent
        reload(self)
    def __dir__(self):
        self.__strict__()
        return dir(self)
    def __getattr__(self, name):
        self.__strict__()
        return getattr(self, name)
    def __setattr__(self, name, value):
        self.__strict__()
        return setattr(self, name, value)
    def __detattr__(self, name):
        self.__strict__()
        return delattr(self, name)

def lazy_import(modname):
    """
    "Lazily imports" the given module. Importing ``a.b.c`` will create lazy 
    module-stubs (in ``sys.modules``) for ``a.b.c``, ``a.b`` and ``a``. 
    Accessing an attribute of a lazy module will "strict" (load) it. Note that
    stricting ``a.b.c`` will strict ``a`` and ``a.b`` as well.
    If a module is already imported, this function will return it directly.
    
    :param modname: the module name (a dotted string)
    
    Example::
    
      >>> minidom = lazy_import("xml.dom.minidom")
      >>> print minidom
      <lazy module 'xml.dom.minidom'>
      >>> minidom.parseString("<a/>")                       # doctest: +ELLIPSIS
      <xml.dom.minidom.Document instance at ...>
      >>> print minidom                                     # doctest: +ELLIPSIS
      <module 'xml.dom.minidom' from '...'>
    """
    if modname in sys.modules:
        return sys.modules[modname]
    mod = sys.modules[modname] = OnDemandModule(modname)
    if "." in modname:
        parent_name = modname.rsplit(".", 1)[0]
        lazy_import(parent_name)
    return mod


if __name__ == "__main__":
    import doctest
    doctest.testmod()


