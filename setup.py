# -*- coding: utf-8 -*-
from codecs import open
from os import path

from setuptools import find_packages
from setuptools import setup

here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='asynchronizer',
    version='0.2.4',
    description='A simple module to make functions asynchronous',
    long_description=long_description,
    url='https://github.com/Arsh23/asynchronizer',
    download_url='https://github.com/Arsh23/asynchronizer/tarball/0.2.4',
    author='arsh23',
    author_email='programmer.arsh@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4'
    ],

    keywords='async asynchronous gevent',
    packages=find_packages(exclude=[]),
    install_requires=['gevent'],


)
