# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

import json

from xivo_lib_rest_client import RESTCommand


class TokenCommand(RESTCommand):

    resource = 'token'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def new(self, backend, expiration=None):
        data = {'backend': backend}
        if expiration:
            data['expiration'] = expiration
        r = self.session.post(self.base_url,
                              headers=self.headers,
                              data=json.dumps(data))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']

    def revoke(self, token):
        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)

        self.session.delete(url, headers=self.headers)

    def is_valid(self, token, required_acl=None):
        params = {}
        if required_acl:
            params['scope'] = required_acl

        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)

        r = self.session.head(url, headers=self.headers, params=params)

        return r.status_code == 204

    def get(self, token, required_acl=None):
        params = {}
        if required_acl:
            params['scope'] = required_acl

        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)

        r = self.session.get(url, headers=self.headers, params=params)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']
