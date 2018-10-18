#! /usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-subjects',
    version='1.0.0',
    packages=find_packages(exclude=['tests']),
    description='Creates and maintains a collection of subjects.',
    long_description='See the home page for more information.',
    install_requires=[
        'markdown~=3.0.1',
    ],
    url='https://github.com/unt-libraries/django-subjects',
    author='University of North Texas Libraries',
    author_email='mark.phillips@unt.edu',
    license='BSD',
    keywords=[
        'django',
        'app',
        'subjects',
        'UNT',
    ],
    classifiers=[
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2'
        'Programming Language :: Python :: 2.7',
    ]
)
