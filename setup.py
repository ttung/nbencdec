#!/usr/bin/env python

import os
import setuptools

install_requires = [line.rstrip() for line in open(os.path.join(os.path.dirname(__file__), "requirements.txt"))]

setuptools.setup(
    name="nbencdec",
    version="0.0.7",
    description="Encode/decode Python Notebook files to .py files.",
    author="Tony Tung",
    author_email="ttung@chanzuckerberg.com",
    license="MIT",
    packages=setuptools.find_packages(),
    package_data={'nbencdec': ['exporters/templates/*.tpl']},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': "nbencdec=nbencdec.cli:main",
        'nbconvert.exporters': [
            'encoded_python = nbencdec.exporters:EncodedPythonExporter',
        ],
    }
)
