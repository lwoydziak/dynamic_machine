'''
Created on Jun 10, 2014

@author: lwoydziak
'''
from setuptools import setup
import glob
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

import os.path

if os.path.exists('README.md'):
    import shutil
    shutil.copyfile('README.md', 'README.txt')

scripts = glob.glob("application/*")

setup(name='DynamicMachine',
      version='0.1',
      maintainer='Luke Woydziak',
      url = 'https://github.com/Pipe-s/devops',
      platforms = ["any"],
      description = 'Python package for running the Dynamic Machine application.',
      long_description = read('README.txt'),
      classifiers = [
            'Development Status :: 3 - Alpha',
            'Natural Language :: English',
            'Operating System :: Unix',
            'Programming Language :: Python',
            'Programming Language :: Unix Shell',
            'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      packages=[
                'dynamic_machine',
                'providers'
               ],
      install_requires=[
                        "apache-libcloud",
                        "pexpect",
                        "jsonconfigfile",
                       ],
      dependency_links=['git+git://github.com/pipe-s/jsonconfigfile.git#egg=jsonconfigfile-1.0.0'],
      scripts=scripts
      )

