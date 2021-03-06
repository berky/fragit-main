#!/usr/bin/env python
# This file is part of FragIt (http://github.com/FragIt/fragit-main),
# a library to fragment molecules for use in fragment based methods
# in quantum chemistry.
#
# Copyright (C) 2012, Casper Steinmann
#
# FragIt is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# FragIt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
import sys
from distutils.core import setup

# use the source code to get version information
from src.strings import version_str

__doc__="""FragIt: a tool to fragment molecules for fragment based methods.

FragIt is a python based tool that allows you to quickly fragment
a molecule and use the output as an input file in quantum chemistry
programs that supports such fragment based methods.

Currently, only the Fragment Molecular Orbital (FMO) method in GAMESS
is supported, but FragIt has been developed to easily allow for other
output writers to be added quickly."""


# Chosen from http://www.python.org/pypi?:action=list_classifiers
classifiers = """\
Development Status :: 5 - Stable
Environment :: Console
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: GPL2 or later
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering :: Chemistry
Topic :: Software Development :: Libraries :: Python Modules
"""

def setup_fragit():
  doclines = __doc__.split("\n")

  fragit_prefix = 'lib/python%i.%i/site-packages/fragit' %(sys.version_info[0], sys.version_info[1])

  setup(name="fragit",
        version=version_str,
        url = "http://github.com/cstein/quantumpy",
        author = "Casper Steinmann",
        author_email = "steinmann@chem.ku.dk",
        maintainer = "Casper Steinmann",
        maintainer_email = "steinmann@chem.ku.dk",
        license = "GPL2 or later",
        description = doclines[0],
        long_description = "\n".join(doclines[2:]),      
        classifiers = filter(None, classifiers.split("\n")),
        platforms = ["Any."],
        package_dir={'fragit': 'src'},
        packages=['fragit'],
        scripts=['scripts/fragit'],
        data_files=[(fragit_prefix,['INSTALL','README','LICENSE', 'CHANGES']),
                    (fragit_prefix,['src/pymol_template','src/jmol_template'])]
  )

print dir()
if __name__ == '__main__':
  setup_fragit()
