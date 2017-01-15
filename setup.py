"""Setup for basic_scraper."""

from setuptools import setup

setup(
    name="Basic Scraper",
    description="An implmentation of a basic scraper.",
    version=0.1,
    author="Maelle Vance",
    author_email="maellevance@gmail.com",
    license="MIT",
    py_modules=['scraper'],
    package_dir={'': '.'},
    install_requires=['beautifulsoup4', 'requests'],
    extras_require={
    },
)
