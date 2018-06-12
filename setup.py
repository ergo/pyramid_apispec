"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

from pyramid_apispec import __version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '{}.{}.{}'.format(__version__['major'],
                            __version__['minor'],
                            __version__['patch'])

setup(
    name='pyramid_apispec',
    version=version,
    description='Pyramid plugin for openapi spec generation ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ergo/pyramid_apispec',  # Optional

    # This should be your name or the name of the organization which owns the
    # project.
    author='Marcin Lulek',
    author_email='marcin@webreactor.eu',
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='pyramid apispec marshmallow rest restful',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['apispec'],
    setup_requires=["pytest-runner"],
    extras_require={
        'dev': ['coverage', 'pytest', 'pyramid', 'tox'],
        'lint': ['black'],
    }
)
