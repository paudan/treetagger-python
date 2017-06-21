#!/usr/bin/env python

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(name='treetagger',
      version='1.1',
      description='A Python module for interfacing with the TreeTagger by Helmut Schmid.',
      long_description=README,
      author='Paulius Danenas',
      author_email='danpaulius@gmail.com',
      url='https://github.com/paudan/treetagger-python',
      py_modules=['treetagger'],
      install_requires=['nltk'],
      license='GPL Version 3',
    )



