from collections import OrderedDict
from itertools import islice, tee, ifilterfalse, cycle


def chunks(iterable, n):
    return list(iterate_chunks(iterable, n))


def iterate_chunks(iterable, n):
    it = iter(iterable)
    chunk = list(islice(it, n))
    while chunk:
        yield chunk
        chunk = list(islice(it, n))


def no_duplicates(sequence):
    return OrderedDict(((v, v) for v in sequence)).values()


def partition(predicate, iterable):
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filter(predicate, t2), list(ifilterfalse(predicate, t1))


def round_robin(*sequences):
    "round_robin('ABC', 'D', 'EF') --> A D E B F C"
    pending = len(sequences)
    next_items = cycle(iter(it).next for it in sequences)
    while pending:
        try:
            for next_item in next_items:
                yield next_item()
        except StopIteration:
            pending -= 1
            next_items = cycle(islice(next_items, pending))