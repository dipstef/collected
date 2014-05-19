class CaseLessDict(dict):

    __slots__ = ()

    def __init__(self, seq=None):
        super(CaseLessDict, self).__init__()
        if seq:
            self.update(seq)

    def __getitem__(self, key):
        return dict.__getitem__(self, self._normalize_key(key))

    def __setitem__(self, key, value):
        dict.__setitem__(self, self._normalize_key(key), self._normalize_value(value))

    def __delitem__(self, key):
        dict.__delitem__(self, self._normalize_key(key))

    def __contains__(self, key):
        return dict.__contains__(self, self._normalize_key(key))

    has_key = __contains__

    def __copy__(self):
        return self.__class__(self)

    copy = __copy__

    def _normalize_key(self, key):
        return key.lower()

    def _normalize_value(self, value):
        return value

    def get(self, key, def_val=None):
        return dict.get(self, self._normalize_key(key), self._normalize_value(def_val))

    def setdefault(self, key, def_val=None):
        return dict.setdefault(self, self._normalize_key(key), self._normalize_value(def_val))

    def update(self, seq):
        seq = seq.iteritems() if isinstance(seq, dict) else seq
        i_seq = ((self._normalize_key(k), self._normalize_value(v)) for k, v in seq)

        super(CaseLessDict, self).update(i_seq)

    @classmethod
    def fromkeys_(cls, keys, value=None):
        return cls((k, value) for k in keys)

    def pop(self, key, *args):
        return dict.pop(self, self._normalize_key(key), *args)