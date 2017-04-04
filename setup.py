import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname+'.md')).read()

setup(
    name = "htmldiff",
    version = "0.23",
    author = "Aaron Swartz",
    author_email = "anastasia.aizman@gmail.com",
    description = ("HTML diff"),
    license = "BSD",
    keywords = "html diff",
    url = "http://www.aaronsw.com/2002/diff",
    packages=['htmldiff', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
