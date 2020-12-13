#!/usr/bin/env python3
# coding: utf-8

from pathlib import Path
from setuptools import setup

setup(
    name='double-subtitles',
    version='0.1.0',
    description='Creates an Advanced Sub-Station Alpha (ASS) subtitle'
        'to show the contents of two subtitle files simultaneously.',
    long_description=(Path(__file__).parent / 'README.md').read_text(),
    author='Vinícius',
    author_email='matosvb@gmail.com',
    url='https://github.com/viniciusbm/double-subtitles',
    license=(Path(__file__).parent / 'LICENSE').read_text(),
    py_modules=['double_subtitles'],
    entry_points={
        'console_scripts': [
            'double-subtitles=double_subtitles:main',
        ],
    }
)
