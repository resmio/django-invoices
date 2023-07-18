#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-invoices',
    version='2.0.1',
    description='Invoices for multimetered billing',
    author='resmio GmbH',
    author_email='support@resmio.com',
    url='https://github.com/resmio/django-invoices/',
    long_description=open('README', 'r').read(),
    packages=find_packages(
        where='.',
        exclude=['tests*'],
    ),
    requires=[
        'django(>=3.0)',
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
