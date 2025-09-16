#!/usr/bin/env python3
# Copyright 2015-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import find_packages, setup

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
            'backends = wazo_auth_client.commands.backends:BackendsCommand',
            'config = wazo_auth_client.commands.config:ConfigCommand',
            'emails = wazo_auth_client.commands.emails:EmailsCommand',
            'external = wazo_auth_client.commands.external:ExternalAuthCommand',
            'groups = wazo_auth_client.commands.groups:GroupsCommand',
            'idp = wazo_auth_client.commands.idp:IDPCommand',
            'ldap_config = wazo_auth_client.commands.ldap_config:LDAPBackendConfigCommand',
            'policies = wazo_auth_client.commands.policies:PoliciesCommand',
            'refresh_tokens = wazo_auth_client.commands.refresh_tokens:RefreshTokenCommand',
            'saml = wazo_auth_client.commands.saml:SAMLCommand',
            'saml_config = wazo_auth_client.commands.saml_config:SAMLConfigCommand',
            'sessions = wazo_auth_client.commands.sessions:SessionsCommand',
            'status = wazo_auth_client.commands.status:StatusCommand',
            'tenants = wazo_auth_client.commands.tenants:TenantsCommand',
            'token = wazo_auth_client.commands.token:TokenCommand',
            'users = wazo_auth_client.commands.users:UsersCommand',
        ]
    },
    install_requires=[
        "wazo-lib-rest-client@https://github.com/wazo-platform/wazo-lib-rest-client/archive/bookworm.zip",  # noqa: E501
        "requests>=2.28.1",
        "stevedore>=4.0.2",
    ],
)
