#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='django-invoices',
    version='0.1.0',
    description='Invoices for multimetered billing',
    author='Niels Sandholt Busch',
    author_email='niels.busch@gmail.com',
    url='https://github.com/resmio/django-invoices/',
    long_description=open('README', 'r').read(),
    packages=[
        'invoices',
    ],
    requires=[
        'django(>=1.4)',
    ],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 2 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
