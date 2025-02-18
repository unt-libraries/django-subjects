#! /usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-subjects',
    version='4.0.1',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    package_data={
        'subjects': [
            'templates/subjects/*',
            'static/subjects/css/*',
            'static/subjects/scripts/*',
            'about_markdown.txt',
        ],
    },
    data_files=[
        ('', ['LICENSE.txt', 'README.md', 'CHANGELOG.md']),
    ],
    description='Creates and maintains a collection of subjects.',
    long_description='See the home page for more information.',
    install_requires=[
        'markdown~=3.1.1',
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
        'Framework :: Django :: 4.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
