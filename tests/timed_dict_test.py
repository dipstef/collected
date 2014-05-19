from collected.dict.timed import TimedDefaultDict, KeyExpiration


def main():
    from collections import defaultdict
    from nose.tools import assert_equal
    import time

    counter = defaultdict(lambda: 0)

    def increment_counter(key):
        counter[key] += 1
        return counter[key]

    def call_back(key, value):
        print 'Key Value expired: %s:%s' % (key, value)
        print 'Next Value: ', timed[key]

    timed = TimedDefaultDict(increment_counter, KeyExpiration(1, refresh_seconds=1, call_on_expiration=call_back))
    assert timed[1] == 1
    time.sleep(5)
    assert_equal(5, timed[1])

if __name__ == '__main__':
    main()