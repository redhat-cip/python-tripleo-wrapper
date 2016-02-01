#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Red Hat, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import setuptools

from rdomhelper import version


def _get_requirements():
    requirements_path = "%s/%s" % (os.path.dirname(os.path.abspath(__file__)),
                                   "requirements.txt")
    with open(requirements_path, "r") as f:
        requirements = f.read()
        return requirements.split("\n")

_README_CONTENT = open("%s/%s" % (os.path.dirname(os.path.abspath(__file__)),
                                  "README.md")).read()

setuptools.setup(
    name='python-rdo-m-helper',
    version=version.__version__,
    packages=setuptools.find_packages(),
    author="Red Hat ci team.",
    author_email="distributed-ci@redhat.com",
    description="A Python helper to drive a TripleO based installer.",
    long_description=_README_CONTENT,
    install_requires=_get_requirements(),
    dependency_links=[
        "https://github.com/redhat-cip/python-dciclient.git"
        "#egg=python-dciclient"
    ],
    url="https://github.com/redhat-cip/python-rdo-m-helper",
    licence="Apache v2.0",
    include_package_data=True,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: System :: Distributed Computing"
    ],
    entry_points={
        "console_scripts": [
            "chainsaw = rdomhelper.shell:main"
        ],
    }
)
