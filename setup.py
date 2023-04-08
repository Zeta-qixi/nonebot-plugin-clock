#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
requirements = [r.strip() for r in open("requirements.txt", 'r', encoding='utf-8').readlines()]

setup(
    name='nonebot-plugin-clock',
    version='0.7.1',
    author='Zeta',
    author_email='',
    long_description="https://github.com/Zeta-qixi/nonebot-plugin-clock",
    license="MIT Licence",
    url='https://github.com/Zeta-qixi/nonebot-plugin-clock/',
    description='nonebot_plugin about clock',
    packages=['nonebot_plugin_clock'],
    install_requires=requirements,

)
