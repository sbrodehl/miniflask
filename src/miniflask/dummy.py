def dummy_fn(*args,**kwargs):
    pass

class miniflask_dummy():
    def __init__(self, *args, **kwargs):
        self.events = {}
        self.modules_avail = {}
        self.modules_loaded = {}

    def getEvents(self):
        return list(zip(self.events.keys(),self.events.values()))

    def register_event(self,name,fn,unique=False):
        self.events[name] = unique
    def register_defaults(self,*args):
        pass

    # ignore all other function calls
    def __getattr__(self, name):
        if name in ["events","modules_avail","modules_loaded","register_event","register_defaults"]:
            return super().__getattribute__(name)
        return dummy_fn
    # def load(self,*args):
    #     pass
    # def showModules(self,*args):
    #     pass


