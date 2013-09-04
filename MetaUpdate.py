import weakref, inspect

class MetaInstanceTracker(type):
    def __init__(cls, name, bases, ns):
        super(MetaInstanceTracker, cls).__init__(name, bases, ns)
        cls.__instance_refs__ = []
    def __instances__(self):
        instances = [(r, r()) for r in self.__instance_refs__]
        instances = filter(lambda (x,y): y is not None, instances)
        self.__instance_refs__ = [r for (r, o) in instances]
        return [o for (r, o) in instances]
    def __call__(self, *args, **kw):
        instance = super(MetaInstanceTracker, self).__call__(*args, **kw)
        self.__instance_refs__.append(weakref.ref(instance))
        return instance

class InstanceTracker:
    __metaclass__ = MetaInstanceTracker

class MetaAutoReloader(MetaInstanceTracker):
    def __init__(cls, name, bases, ns):
        updater = ns.pop('__update__', None)
        super(MetaAutoReloader, cls).__init__(
            name, bases, ns)
        f = inspect.currentframe().f_back
        for d in [f.f_locals, f.f_globals]:
            if d.has_key(name):
                old_class = d[name]
                for instance in old_class.__instances__():
                    instance.__class__ = cls
                    instance.update_instance()
                    if updater: updater(instance)
                    cls.__instance_refs__.append(
                        weakref.ref(instance))
                for subclass in old_class.__subclasses__():
                    bases = list(subclass.__bases__)
                    bases[bases.index(old_class)] = cls
                    subclass.__bases__ = tuple(bases)
                break

class AutoReloader:
    __metaclass__ = MetaAutoReloader
    def update_instance(self):
        pass

class Bar(AutoReloader):
    pass

class Baz(Bar):
    pass

b = Bar()
b2 = Baz()

class Bar(AutoReloader):
    def meth(self, arg):
        print arg

if __name__ == '__main__':
    # now b is "upgraded" to the new Bar class:
    b.meth(1)
    # unfortunately, Baz instances can't join the fun:
    try:
        b2.meth(2)
    except AttributeError:
        print "nuts"
    # even worse (and, actually, harder to deal with):
    # new Baz() instances can't play either:
    # unfortunately, Baz instances can't join the fun:
    try:
        Baz().meth(3)
    except AttributeError:
        print "nuts again"

