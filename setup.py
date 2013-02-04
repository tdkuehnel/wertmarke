from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='wertmarke',
      version=version,
      description="This is the python Wertmarken server package, including daemon, server and client program",
      long_description="""\
This is the python Wertmarken server package, including daemon, server and client program""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='wertmarke daemon client server valuetoken',
      author='Torsten Kuehnel',
      author_email='info@datentaeter.org',
      url='http://wertmarken.datentaeter.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
