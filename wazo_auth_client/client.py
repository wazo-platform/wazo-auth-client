# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests

from wazo_lib_rest_client.client import BaseClient


class AuthClient(BaseClient):

    namespace = 'wazo_auth_client.commands'

    def __init__(
        self,
        host,
        port=443,
        prefix='/api/auth',
        version='0.1',
        username=None,
        password=None,
        **kwargs
    ):
        kwargs.pop('key_file', None)
        kwargs.pop('master_tenant_uuid', None)
        super(AuthClient, self).__init__(
            host=host, port=port, prefix=prefix, version=version, **kwargs
        )
        self.username = username
        self.password = password

    def session(self):
        session = super(AuthClient, self).session()
        if self.username and self.password:
            session.auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        return session
