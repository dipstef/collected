from collected import CaseLessDict

d = CaseLessDict()

d['FOO'] = 'bar'
assert d['foo'] == 'bar'