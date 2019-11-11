#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages

setup(
    name='wazo_auth_client',
    version='0.1',
    description='a simple client library for the wazo-auth HTTP interface',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='http://wazo.community',
    packages=find_packages(),
    entry_points={
        'wazo_auth_client.commands': [
            'admin = wazo_auth_client.commands.admin:AdminCommand',
            'emails = wazo_auth_client.commands.emails:EmailsCommand',
            'external = wazo_auth_client.commands.external:ExternalAuthCommand',
            'token = wazo_auth_client.commands.token:TokenCommand',
            'backends = wazo_auth_client.commands.backends:BackendsCommand',
            'groups = wazo_auth_client.commands.groups:GroupsCommand',
            'policies = wazo_auth_client.commands.policies:PoliciesCommand',
            'refresh_tokens = wazo_auth_client.commands.refresh_tokens:RefreshTokenCommand',
            'tenants = wazo_auth_client.commands.tenants:TenantsCommand',
            'users = wazo_auth_client.commands.users:UsersCommand',
            'sessions = wazo_auth_client.commands.sessions:SessionsCommand',
        ]
    },
)
