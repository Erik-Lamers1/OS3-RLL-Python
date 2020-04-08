#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

VERSION = '0.2.1'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="os3-rocket-league-ladder",
    version=VERSION,
    url="https://github.com/Erik-Lamers1/OS3-RRL-Python",
    packages=find_packages(exclude=['tests', 'tests.*']),
    author="Erik Lamers",
    install_requires=['discord', 'unipath', 'colorama', 'six', 'PyMySQL', 'tabulate'],
    entry_points={
        'console_scripts': [
            'os3-rocket-league-ladder = os3_rll.rocket_league_ladder:main',
        ],
    },
)
