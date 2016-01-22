#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015-2016 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from setuptools import setup
from setuptools import find_packages

requirements = [
    "xivo_lib_rest_client==0.2",
]

dependency_links = [
    'git+https://github.com/xivo-pbx/xivo-lib-rest-client.git#egg=xivo_lib_rest_client-0.2'
]

setup(
    name='xivo_auth_client',
    version='0.1',

    description='a simple client library for the xivo-auth HTTP interface',

    author='Avencall',
    author_email='dev@avencall.com',

    url='https://github.com/xivo-pbx/xivo-auth-client',

    packages=find_packages(),

    entry_points={
        'auth_client.commands': [
            'token = xivo_auth_client.commands.token:TokenCommand',
            'backends = xivo_auth_client.commands.backends:BackendsCommand',
        ],
    },
    install_requires=requirements,
    dependency_links=dependency_links
)
