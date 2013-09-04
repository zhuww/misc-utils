from uncertainties import Variable, num_with_uncert

class measurement(Variable):
    def value():
        def fget(self):
            return (self.nominal_value, self.std_dev())
        def fset(self, value):
            self._nominal_value = value[0]
            self._std_dev = value[1]
        return locals()
    value = property(**value())
    def __init__(self, representation, tag=None):
        if isinstance(representation, basestring):
            init_args = str_to_number_with_uncert(representation)
        else:
            try:  # This passes, for 2-character strings...
                (value, std_dev) = representation
            except TypeError:
                # Case of a single float, integer, etc.:
                init_args = (representation,)
            else:
                # The user provided a sequence with 2 elements:
                init_args = representation
        if tag is not None:
            assert ((type(tag) is str) or (type(tag) is unicode)), \
                   "The tag can only be a string."
        #! init_args must contain all arguments, here:
        Variable.__init__(self, *init_args, **{'tag': tag})
