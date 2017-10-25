from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

README = open(join(abspath(dirname(__file__)), 'README.rst'), encoding="utf8").read()

setup(name='treetagger',
      version='1.1.2',
      description='NLTK module for interfacing with the TreeTagger by Helmut Schmidt',
      long_description=README,
      author='Paulius Danenas',
      author_email='danpaulius@gmail.com',
      url='https://github.com/paudan/treetagger-python',
      py_modules=['treetagger'],
      install_requires=['nltk'],
      license='GPL Version 3',
    )



