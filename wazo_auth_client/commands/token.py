# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_lib_rest_client import RESTCommand


class TokenCommand(RESTCommand):

    resource = 'token'
    _ro_headers = {'Accept': 'application/json'}
    _rw_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def new(self, backend=None, expiration=None, session_type=None):
        data = {}
        if backend:
            data['backend'] = backend
        if expiration:
            data['expiration'] = expiration

        headers = dict(self._rw_headers)
        if session_type:
            headers['Wazo-Session-Type'] = session_type

        r = self.session.post(self.base_url, headers=headers, json=data)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']

    def revoke(self, token):
        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)

        self.session.delete(url, headers=self._ro_headers)

    def is_valid(self, token, required_acl=None, tenant=None):
        params = {}
        if required_acl:
            params['scope'] = required_acl
        if tenant:
            params['tenant'] = tenant

        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)

        r = self.session.head(url, headers=self._ro_headers, params=params)

        if r.status_code in (204, 403, 404):
            return r.status_code == 204

        self.raise_from_response(r)

    def get(self, token, required_acl=None, tenant=None):
        params = {}
        if required_acl:
            params['scope'] = required_acl
        if tenant:
            params['tenant'] = tenant

        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)

        r = self.session.get(url, headers=self._ro_headers, params=params)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']
