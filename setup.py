#!/usr/bin/env python
import os
import re
import codecs

from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, "src", "crashlog", "__init__.py")


def get_version(*file_paths):
    """Retrieves the version from django_mb/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"__version__ = [\"]([^\"]*)[\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def fread(*parts):
    return [l[:-1] for l in codecs.open(os.path.join(ROOT, *parts), encoding="utf-8").readlines() if l[0] != '#']


install_requires = fread('src/requirements', 'install.pip')
tests_require = fread('src/requirements', 'testing.pip')
dev_require = fread('src/requirements', 'develop.pip')

setup(
    name='django-crashlog',
    version=get_version(init),
    url='https://github.com/saxix/django-strategy-field',
    description="Django Database Exception Logger",
    author='sax',
    author_email='sax@os4d.org',
    license='BSD',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
    extras_require={
        'test': tests_require,
        'dev': dev_require + tests_require,
    },
    platforms=['linux'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers'
    ]
)
