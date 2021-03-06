#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

VERSION = "0.3.2"

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="os3-rocket-league-ladder",
    version=VERSION,
    url="https://github.com/Erik-Lamers1/OS3-RRL-Python",
    packages=find_packages(exclude=["tests", "tests.*", "os3_rll.tests", "os3_rll.tests.*"]),
    author="Erik Lamers, Vincent Breider, Vincent van der Eijk",
    install_requires=["discord.py", "unipath", "colorama", "six", "PyMySQL", "tabulate"],
    entry_points={"console_scripts": ["os3-rocket-league-ladder = os3_rll.rocket_league_ladder:main",],},
)
