from datetime import timedelta, datetime
from UserDict import DictMixin
from collections import OrderedDict
import multiprocessing
from threading import Timer


class KeyExpiration(object):
    def __init__(self, expiration, refresh_seconds, call_on_expiration=None):
        self._expire_delta = timedelta(seconds=expiration)
        self._expiration_callback = call_on_expiration
        self.refresh = refresh_seconds

    def is_expired(self, last_refresh):
        refresh_diff = datetime.now() - last_refresh
        return refresh_diff > self._expire_delta

    def expired(self, key, value):
        if self._expiration_callback:
            self._execute_expiration_callback(key, value)

    def _execute_expiration_callback(self, key, value):
        self._expiration_callback(key, value)

default_expiration = KeyExpiration(1, refresh_seconds=5)


class TimedDict(object, DictMixin):

    def __init__(self, expiration, max_size=None):
        self._data = OrderedDict()
        self._lock = multiprocessing.RLock()
        self._max_size = max_size

        self._expiration = expiration
        self._key_updates = {}
        _schedule_every(seconds=expiration.refresh, fun=self._refresh)

    def __getitem__(self, key):
        with self._lock:
            return self._data[key]

    def __setitem__(self, key, value):
        with self._lock:
            self._data[key] = value
            self._key_updates[key] = datetime.now()

    def __delitem__(self, key):
        with self._lock:
            del self._data[key]
            del self._key_updates[key]

    def keys(self):
        with self._lock:
            return self._data.keys()

    def __len__(self):
        with self._lock:
            return len(self._data)

    def _refresh(self):
        self._remove_expired()
        if self._max_size:
            self._ensure_max_size()

    def _remove_expired(self):
        for key, value in self._data.iteritems():
            if self._is_expired(key):
                del self[key]
                self._expiration.expired(key, value)

    def _ensure_max_size(self):
        size_diff = len(self._data) - self._max_size

        if size_diff > 0:
            keys = sorted(self._key_updates.keys(), key=lambda k: self._key_updates[k])
            for key in keys[:size_diff]:
                del self[key]

    def _is_expired(self, key):
        if self._key_expired(key):
            with self._lock:
                return self._key_expired(key)
        return False

    def _key_expired(self, key):
        last_refresh = self._key_updates[key]
        return self._expiration.is_expired(last_refresh)


class TimedDefaultDict(TimedDict):

    def __init__(self, factory, expiration, max_size=None):
        super(TimedDefaultDict, self).__init__(expiration, max_size)
        self._factory = factory

    def __getitem__(self, key):
        with self._lock:
            try:
                value = super(TimedDefaultDict, self).__getitem__(key)
            except KeyError:
                self[key] = value = self._factory(key)

            return value


def _schedule_function(seconds, fun, daemon=False):
    timer = Timer(seconds, fun)
    timer.daemon = daemon
    timer.start()


def _schedule_every(seconds, fun, daemon=True):

    def schedule_after():
        fun()
        _schedule_function(seconds, schedule_after, daemon=daemon)

    _schedule_function(seconds, schedule_after, daemon=daemon)