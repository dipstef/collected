from collected.sequence import chunks


def main():
    l = range(100)

    l_chunks = chunks(l, 6)

    assert 17 == len(l_chunks)
    assert len(l_chunks[-1]) == 4
    assert len(l_chunks[-2]) == 6

if __name__ == '__main__':
    main()