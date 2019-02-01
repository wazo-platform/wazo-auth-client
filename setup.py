#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

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
            'admin = xivo_auth_client.commands.admin:AdminCommand',
            'emails = xivo_auth_client.commands.emails:EmailsCommand',
            'external = xivo_auth_client.commands.external:ExternalAuthCommand',
            'init = xivo_auth_client.commands.init:InitCommand',
            'token = xivo_auth_client.commands.token:TokenCommand',
            'backends = xivo_auth_client.commands.backends:BackendsCommand',
            'groups = xivo_auth_client.commands.groups:GroupsCommand',
            'policies = xivo_auth_client.commands.policies:PoliciesCommand',
            'tenants = xivo_auth_client.commands.tenants:TenantsCommand',
            'users = xivo_auth_client.commands.users:UsersCommand',
            'sessions = xivo_auth_client.commands.sessions:SessionsCommand',
        ],
    }
)
