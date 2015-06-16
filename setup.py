#!/usr/bin/env python

from distutils.core import setup

setup(name='chord_finder',
        version='0.9.2',
        author='Robert Pearce',
        author_email='siology.io@gmail.com',
        url='https://github.com/robertpearce/chord-finder',
        download_url='https://pypi.python.org/pypi/chord_finder',
        description='Simple linux wxPython gui app that displays chords for 6 string guitar',
        license='GPLv2', 
        classifiers=('Development Status :: 5 - Production/Stable',
                     'Environment :: X11 Applications',
                     'Intended Audience :: End Users/Desktop',
                     'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                     'Programming Language :: Python',
                     'Topic :: Utilities'),
        packages=['chordfinder'],
        requires=['wxPython', 'Pillow'],
        scripts=['chord-finder'],
        data_files=[('/etc/chord-finder', ['data/ChordData.csv','data/favicon.ico','data/welcomeChord.png'])]
      )

