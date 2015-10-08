#!/usr/bin/env python
"""
colab-superarchives plugin
===================

Super Archives (Mailman) plugin for Colab.
"""
from setuptools import setup, find_packages

install_requires = ['colab']

tests_require = ['mock']

setup(
    name="colab-superarchives",
    version='0.1.0',
    author='Charles Oliveira',
    author_email='18oliveira.charles@gmail.com',
    url='https://github.com/colab/colab-superarchives-plugin',
    description='Super Archives (Mailman) plugin for Colab',
    long_description=__doc__,
    license='GPLv3',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    test_suite="tests.runtests.run",
    tests_require=tests_require,
    extras_require={'test': tests_require},
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
