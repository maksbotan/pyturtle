#!/usr/bin/env python

__author__="maksbotan"
__date__ ="$27.06.2010 22:47:41$"

from distutils.core import setup

setup (
  name = 'Pyturtle',
  version = '0.0.1',
  description='Cross-toolkit Logo interpreter in Python',
  scripts=['pyturtle'],
  package_dir={'': 'src'},
  packages=['pyturtle'],
  requires=['gtk', 'glib', 'gobject', 'goocanvas', 'notify', 'gtk.glade', 'ply'],
  data_files=[('share/pyturtle', ['src/pyturtle/mainwindow.glade'])],
  url='http://github.com/maksbotan/pyturtle/',
  author='maksbotan',
  author_email='kolmax94@gmail.com',
  license='GPL',
)
