#!/usr/bin/env python

from os import path

from setuptools import find_packages, setup

from wagtail_freezer import __version__


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="wagtail-freezer",
    version=__version__,
    description="Generates static HTML sites from a Wagtail project",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Matt Westcott",
    author_email="matthew@torchbox.com",
    url="",
    packages=find_packages(),
    include_package_data=True,
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 3",
    ],
    install_requires=[
        "Django>=3.0,<4.0",
        "Wagtail>=3.0,<4.0",
        "beautifulsoup4>=4.9,<5.0",
    ],
    extras_require={
        "testing": ["dj-database-url==0.5.0"],
    },
    zip_safe=False,
)
