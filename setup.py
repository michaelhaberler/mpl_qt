import os
from setuptools import setup

# import build_ui
try:
    from pyqt_distutils import build_ui
    cmdclass = {'build_ui': build_ui}
except ImportError:
    build_ui = None  # user won't have pyqt_distutils when deploying
    cmdclass = {}


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "mpl_qt",
    version = "0.0.1",
    author = "dont't ask",
    author_email = "dontask@gmail.com",
    description = ("dont't ask"),
    license = "BSD",
    keywords = "kw",
    url = "url",
    packages=['mpl_qt'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    cmdclass=cmdclass
)
