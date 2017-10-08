from setuptools import setup

setup(
    name="htmldiffer",
    version="0.25.1",
    author="Anastasia Aizman",
    author_email="anastasia.aizman@gmail.com",
    description=("HTML diff"),
    license="BSD3",
    keywords="html diff",
    url="https://github.com/anastasia/htmldiffer",
    packages=['htmldiffer', 'tests'],
    install_requires=[
          'beautifulsoup4',
      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD3 License",
    ],
    python_requires='>=2.7'
)

