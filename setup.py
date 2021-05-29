#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages, find_namespace_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = [ ]

setup(
    name='PyDeftLariat',
    author="Tyler McMaster",
    author_email='mcmasty@yahoo.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Using PyHamcrest to build a collection of data filters.",
    entry_points={
        'console_scripts': [
            'deft=deftlariat.entrypoints.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    keywords="hamcrest matchers data filters",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    package_data={"deftlariat": ["py.typed"]},
    provides=['deftlariat'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mcmasty/PyDeftLariats',
    version='0.0.1',
    zip_safe=False,
)
