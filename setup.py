""" Module setup """
from setuptools import setup, find_packages

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="skam",
    packages=find_packages(),
    description="Webapp to make NRK subs accessible and browsable",
    license="GPLv3",
    version="2.0.0",
    author="Bjørn Snoen",
    author_email="bjorn.snoen@gmail.com",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License Version 3",
        "Operating System :: OS Independent",
    ]
)
