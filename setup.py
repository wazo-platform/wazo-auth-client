#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2017 The Wazo Authors  (see the AUTHORS file)
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

setup(
    name='xivo_auth_client',
    version='0.1',

    description='a simple client library for the wazo-auth HTTP interface',

    author='Wazo Authors',
    author_email='dev@wazo.community',

    url='http://wazo.community',

    packages=find_packages(),

    entry_points={
        'auth_client.commands': [
            'token = xivo_auth_client.commands.token:TokenCommand',
            'backends = xivo_auth_client.commands.backends:BackendsCommand',
            'policies = xivo_auth_client.commands.policies:PoliciesCommand',
            'users = xivo_auth_client.commands.users:UsersCommand',
        ],
    }
)
