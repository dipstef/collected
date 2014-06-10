from collections import Callable, OrderedDict


class OrderedDefaultDict(OrderedDict):

    def __init__(self, factory, *args, **kwargs):
        if not (factory is None or callable(factory)):
            raise TypeError('first argument must be callable or None')

        self._factory = factory
        super(OrderedDefaultDict, self).__init__(*args, **kwargs)

    def __missing__(self, key):
        self[key] = default = self._factory()
        return default

    def __reduce__(self):
        return type(self), self._factory, None, None, self.items()


def default_dict(dict_type):
    assert issubclass(dict_type, dict)

    class DefaultDict(dict_type):

        def __init__(self, factory, *args, **kwargs):
            if not isinstance(factory, Callable):
                raise TypeError('first argument must be callable')

            dict_type.__init__(self, *args, **kwargs)
            self.default_factory = factory

        def __setitem__(self, key, value):
            return dict_type.__setitem__(self, key, value)

        def __getitem__(self, key):
            try:
                return dict_type.__getitem__(self, key)
            except KeyError:
                self[key] = value = self.default_factory()
                return value

        def __reduce__(self):
            return type(self), self.default_factory, None, None, dict_type.items(self)

        def copy(self):
            return self.__copy__()

        def __copy__(self):
            return type(self)(self.default_factory, self)

        def __deepcopy__(self, memo):
            import copy

            return type(self)(self.default_factory, copy.deepcopy(dict_type(self)))

        def __repr__(self):
            return '%s(%s, %s)' % (self.__class__.__name__, self.default_factory, dict_type.__repr__(self))

    return DefaultDict
