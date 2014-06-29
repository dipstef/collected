Collected
=========

A collection of data structures, mostly dictionary implementations


Dictionaries
============

Caseless

.. code-block:: python

    from collectected import Case

    from collected import CaseLessDict

    >>> d = CaseLessDict()

    >>> d['FOO'] = 'bar'
    assert d['foo'] == 'bar'

Ordered Default

.. code-block:: python

    from collected import OrderedDefaultDict

    >>> d = OrderedDefaultDict(list)

    >>> d['one'].append('two')
    >>> d['one'].append('three')

    assert d['one'] == ['two', 'three']

Timed with expiration on key values, can be used to implement simple caches

.. code-block:: python

    from collected.dict.timed import TimedDefaultDict, expire

    counter = defaultdict(lambda: 0)

    def increment_counter(key):
        counter[key] += 1
        return counter[key]

    def print_expired(key, value):
        print 'Key Value expired: %s:%s' % (key, value)
        print 'Next Value: ', timed[key]

    >>> expiration = expire(after=seconds(1), on_expiration=print_expired)

    >>> timed = TimedDefaultDict(increment_counter, expiration, check_every=seconds(1))
    >>> time.sleep(5)

    Key Value expired: 1:1
    Next Value:  2
    Key Value expired: 1:2
    Next Value:  3
    Key Value expired: 1:3
    Next Value:  4
    Key Value expired: 1:4
    Next Value:  5
    Key Value expired: 1:5
    Next Value:  6