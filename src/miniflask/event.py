from .dummy import dummy_fn, dummy_fn_unique

class event_obj():
    def __init__(self, fn, unique, module):
        self.unique = unique
        if unique:
            self.fn = fn
            self.modules = module
        else:
            self.fn = [fn]
            self.modules = [module]

class event():
    def __init__(self, mf, optional=False, unique=False):
        self._mf = mf
        self.optional_value = optional
        self.unique_value = unique

    def __getattr__(self, name):
        if name == "_mf":
            return super().__getattribute__(name)
        elif name == "optional_value":
            return super().__getattribute__(name)
        elif name == "unique_value":
            return super().__getattribute__(name)
        elif name == "optional":
            return super().__getattribute__("_mf").event_optional
        elif name == "optional_unique":
            return super().__getattribute__("_mf").event_optional_unique
        if name not in self._mf.event_objs:
            if not self.optional_value:
                raise AttributeError("The Event '%s' has not been registered yet." % name)
            if self.unique_value:
                return dummy_fn_unique
            else:
                return dummy_fn
        def fn_wrap(*args,**kwargs):
            eobj = self._mf.event_objs[name]
            if eobj.unique:
                return eobj.fn(eobj.modules.state,eobj.modules.event,*args,**kwargs)
            else:
                return [fn(mf.state,mf.event,*args,**kwargs) for fn, mf in zip(eobj.fn,eobj.modules)]
        return fn_wrap


