
import os
import sys
from setuptools import setup

from glob import glob
import os.path as op

import mpl_qt


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def setup_package():

    from subprocess import call

    for uifile in glob(op.join('mpl_qt', 'ui', '*.ui')):
        uipyfile = '%s%s' % (uifile[:-2], 'py')
        command = ["pyuic4", "-o", uipyfile, uifile]
        try:
            exitcode = call(command)
            print command, exitcode
        except OSError:
            exitcode = 1
        if exitcode:
            if os.path.exists(uipyfile):
                print >> sys.stderr, \
                    """Warning: unable to recompile '%s' to '%s' using
                    pyuic4 (using existing file).""" % (uifile, uipyfile)
            else:
                print >> sys.stderr, \
                    """ERROR: unable to compile '%s' to '%s' using
                    pyuic4. pyuic4 is included in the PyQt4 development
                    package.""" % (uifile, uipyfile)
                sys.exit(1)

    for rcfile in glob(op.join('poclib', 'qtgui', 'ui', '*.qrc')):
        rcpyfile = '%s%s' % (rcfile[:-4], '_rc.py')
        command = ["pyrcc4", "-o", rcpyfile, rcfile]
        try:
            exitcode = call(command)
            print command, exitcode
        except OSError:
            exitcode = 1
        if exitcode:
            if os.path.exists(rcpyfile):
                print >> sys.stderr, \
                    """Warning: unable to recompile '%s' to '%s' using
                    pyrcc4 (using existing file).""" % (rcfile, rcpyfile)
            else:
                print >> sys.stderr, \
                    """ERROR: unable to compile '%s' to '%s' using
                    pyrcc4. pyrcc4 is included in the PyQt4 development
                    package.""" % (rcfile, rcpyfile)
                sys.exit(1)

    setup(
        name = "mpl_qt",
        version = mpl_qt.__version__,
        author = "dont't ask",
        author_email = "dontask@gmail.com",
        description = ("dont't ask"),
        license = "BSD",
        keywords = "kw",
        url = "url",
        packages=['mpl_qt', 'mpl_qt.ui'],
        scripts=['bin/mpl_qt'],
        package_data={'': ['README.md']},
#        long_description=read('README.md'),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Topic :: Utilities",
            "License :: OSI Approved :: BSD License",
        ],
    )


if __name__ == '__main__':
    setup_package()
