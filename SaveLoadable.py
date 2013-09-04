import cPickle

class SaveLoadable(object):
    """A class that defines some universal methods like saving, loading and displaying parameters. By inherienting from this class, subclass can gain access to these methods."""
    def save(self, filename):
        """Saving the object."""
        file = open(filename, 'wb')
        cPickle.dump(self, file, -1)
        file.close()
    @classmethod
    def load(cls, filename):
        """Loading an object from a file."""
        file = open(filename, 'rb')
        obj = cPickle.load(file)
        file.close()
        if isinstance(obj, cls):
            return obj
        else:
            raise 'File %s does not contain a %s object' % (filename, cls.__name__)
    def display(self):
        """Display all parameters in this object."""
        for key in self.__dict__.keys():
            print "%s: %s" % (key, self.__dict__[key])


class MetaSaveLoader(type):
    def __new__(mcl, name, base, dict):
        def save(self, filename):
            """Saving the object."""
            file = open(filename, 'wb')
            cPickle.dump(self, file, -1)
            file.close()
        @classmethod
        def load(cls, filename):
            """Loading an object from a file."""
            file = open(filename, 'rb')
            obj = cPickle.load(file)
            file.close()
            if isinstance(obj, cls):
                return obj
            else:
                raise 'File %s does not contain a %s object' % (filename, cls.__name__)
        def display(self):
            """Display all parameters in this object."""
            for key in self.__dict__.keys():
                print "%s: %s" % (key, self.__dict__[key])

        dict['save'] = save
        dict['load'] = load
        dict['display'] = display
        return super(MetaSaveLoader, mcl).__new__(mcl, name, base, dict)
