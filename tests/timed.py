from dated.timedelta import seconds
from collected.dict.timed import TimedDefaultDict, KeyExpiration


def main():
    from collections import defaultdict
    import time
    from nose.tools import assert_equal
    

    counter = defaultdict(lambda: 0)

    def increment_counter(key):
        counter[key] += 1
        return counter[key]

    def print_expired(key, value):
        print 'Key Value expired: %s:%s' % (key, value)
        print 'Next Value: ', timed[key]

    expiration = KeyExpiration(seconds(1), on_expiration=print_expired)

    timed = TimedDefaultDict(increment_counter, expiration, check_every=seconds(1))
    assert timed[1] == 1
    time.sleep(5)

    assert_equal(5, timed[1])

if __name__ == '__main__':
    main()