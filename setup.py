#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='slowclap',
    version='0.1.0',
    description='Simple event listing app.',
    author='Kirill Borisov',
    author_email='borisov@bars-open.ru',
    url='https://github.com/lensvol/slowclap',
    packages=[
        'slowclap',
        'slowclap.migrations',
        'slowclap.management',
        'slowclap.management.commands'
    ],
    package_dir={'slowclap': 'slowclap'},
    include_package_data=True,
    install_requires=[
        'Django>=1.5.5',
        'south',
        'pytz',
        'djangorestframework',
        'markdown',
        'django-filter',
        'mock'
    ],
    license="MIT",
    zip_safe=False,
    keywords='slowclap',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
