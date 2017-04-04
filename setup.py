import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

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
