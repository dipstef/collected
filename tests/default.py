from collected import OrderedDefaultDict

d = OrderedDefaultDict(list)

d['one'].append('two')
d['one'].append('three')

assert d['one'] == ['two', 'three']