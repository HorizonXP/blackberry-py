'''Useful decorators used in Tart and apps built with it.'''


class cached_property(object):
    '''Decorator to create property which caches the result of the initial
    access as an attribute, avoiding repeated calls.  By virtue of this
    descriptor not defining __set__ it acts as a non-data descriptor.
    See http://docs.python.org/3.2/reference/datamodel.html#invoking-descriptors
    for more.'''
    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except AttributeError:
            pass


    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.wrapped(instance)
        setattr(instance, self.wrapped.__name__, value)
        return value


# EOF
