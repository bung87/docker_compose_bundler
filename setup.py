#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import pkg_resources
from setuptools import setup, find_packages
import os
import codecs
import re
import sys


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

install_requires = [
    'PyYAML'
]

extras_require = {
    ":python_version<'3.4'": ['pathlib']
}

try:
    if 'bdist_wheel' not in sys.argv:
        for key, value in extras_require.items():
            if key.startswith(':') and pkg_resources.evaluate_marker(key[1:]):
                install_requires.extend(value)
except Exception as e:
    print("Failed to compute platform dependencies: {}. ".format(e) +
          "All dependencies will be installed as a result.", file=sys.stderr)
    for key, value in extras_require.items():
        if key.startswith(':'):
            install_requires.extend(value)
    extras_require = {}

setup(
    name='docker_compose_bundler',
    version=find_version("docker_compose_bundler", "__init__.py"),
    description='bundle docker images to tarball base on docker-compose.yml that can then be used with docker load.',
    author='bung',
    author_email='crc32@qq.com',
    license='MIT',
    keywords=['docker', 'docker compose', 'bundler', 'command line', 'cli'],
    url='https://github.com/bung87/docker_compose_bundler',
    packages = find_packages(),
    package_dir={'docker_compose_bundler': 'docker_compose_bundler'},
    extras_require=extras_require,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'docker_compose_bundler=docker_compose_bundler.the_bundler:main'
        ],
    },
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
