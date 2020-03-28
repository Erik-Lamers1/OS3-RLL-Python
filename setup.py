#!/usr/bin/env python
import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="os3-rocket-league-ladder",
    version="0.1",
    url="https://github.com/Erik-Lamers1/OS3-RRL-Python",
    packages=find_packages(exclude=['tests', 'tests.*']),
    author="Erik Lamers",
    install_requires=['discord', 'unipath'],
    entry_points={
        'console_scripts': [
            'os3-rocket-league-ladder = os3_rrl.rocket_league_ladder:main',
        ],
    },
)
