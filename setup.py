from __future__ import print_function

import os
import os.path as op
import sys
from glob import glob

from setuptools import setup
import mpl_qt


def read(fname):
    return open(op.join(op.dirname(__file__), fname)).read()

def compile_ui_files(uifiles, compiler, extension=".py"):
    from subprocess import call

    for uifile in uifiles:
        uipyfile = "{}{}".format(op.splitext(uifile)[0], extension)
        command = [compiler, "-o", uipyfile, uifile]
        try:
            exitcode = call(command)
            print("{} Status={}".format(" ".join(command), exitcode))
        except OSError:
            exitcode = 1
        if exitcode:
            if op.exists(uipyfile):
                print("Warning: unable to compile '{}' to '{}' using "
                      "{} (using existing file).".format(compiler, uifile,
                                                         uipyfile),
                      file=sys.stderr)
            else:
                print("ERROR: unable to compile '{}' to '{}' using "
                      "{}.".format(compiler, compiler, uifile, uipyfile),
                      file=sys.stderr)
                sys.exit(1)

def compile_ui():
    compile_ui_files(glob(op.join('mpl_qt', 'ui', '*.ui')), "pyside-uic")
    compile_ui_files(glob(op.join('mpl_qt', 'ui', '*.qrc')), "pyside-rcc",
                     extension="_rc.py")

def setup_package():
    setup(
        name = "mpl_qt",
        version = mpl_qt.__version__,
        author = "Michael Haberler",
        author_email = "me@github",
        description = "Example for embedding matplotlib in PySide GUI.",
        license = "BSD",
        keywords = "matplotlib, PySide",
        url = "https://github.com/michaelhaberler/mpl_qt",
        packages=['mpl_qt', 'mpl_qt.ui'],
        scripts=['bin/mpl_qt'],
        package_data={'': ['README.md']},
        long_description=read('README.md'),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "License :: OSI Approved :: BSD License",
        ],
    )


if __name__ == '__main__':
    compile_ui()
    setup_package()
