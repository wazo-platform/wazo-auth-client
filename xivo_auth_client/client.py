# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

import requests

from xivo_lib_rest_client.client import BaseClient


class AuthClient(BaseClient):

    namespace = 'auth_client.commands'

    def __init__(self,
                 host,
                 port=9497,
                 version='0.1',
                 username=None,
                 password=None,
                 verify_certificate=True,
                 **kwargs):
        super(AuthClient, self).__init__(
            host=host,
            port=port,
            version=version,
            verify_certificate=verify_certificate,
            **kwargs)
        self.username = username
        self.password = password

    def session(self):
        session = super(AuthClient, self).session()
        if self.username and self.password:
            session.auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        return session
