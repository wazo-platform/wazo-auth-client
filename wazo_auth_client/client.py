# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import requests
import requests.auth
from wazo_lib_rest_client.client import BaseClient


class AuthClient(BaseClient):
    namespace = 'wazo_auth_client.commands'

    def __init__(
        self,
        host: str,
        port: int = 443,
        prefix: str | None = '/api/auth',
        version: str = '0.1',
        username: str | None = None,
        password: str | None = None,
        **kwargs,
    ):
        kwargs.pop('key_file', None)
        kwargs.pop('master_tenant_uuid', None)
        super().__init__(host=host, port=port, prefix=prefix, version=version, **kwargs)
        self.username = username
        self.password = password

    def session(self):
        session = super().session()
        if self.username and self.password:
            session.auth = requests.auth.HTTPBasicAuth(
                self.username.encode("utf-8"), self.password.encode("utf-8")
            )
        return session
