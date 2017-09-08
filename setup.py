from setuptools import setup

setup(
    name="htmldiffer",
    version="0.24",
    author="Anastasia Aizman",
    author_email="anastasia.aizman@gmail.com",
    description=("HTML diff"),
    license="BSD",
    keywords="html diff",
    url="https://github.com/anastasia/htmldiff",
    packages=['htmldiff', 'tests'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=2.7'
)

