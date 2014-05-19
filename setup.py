from distutils.core import setup

VERSION = '0.1'

desc = """A collection of dictionary implementations and sequence functions"""

name = 'collected'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description=desc,
      packages=['collected', 'collected/dict'],

      platforms=['Any']
)