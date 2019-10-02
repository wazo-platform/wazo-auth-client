# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_lib_rest_client import RESTCommand


class TokenCommand(RESTCommand):

    resource = 'token'
    _ro_headers = {'Accept': 'application/json'}
    _rw_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Wazo Python auth client',
    }

    def new(
        self,
        backend=None,
        expiration=None,
        session_type=None,
        user_agent=None,
        access_type=None,
        client_id=None,
        refresh_token=None,
    ):
        data = {}
        if backend:
            data['backend'] = backend
        if expiration:
            data['expiration'] = expiration
        if client_id:
            data['client_id'] = client_id
        if refresh_token:
            data['refresh_token'] = refresh_token
        if access_type:
            data['access_type'] = access_type

        headers = dict(self._rw_headers)
        if session_type:
            headers['Wazo-Session-Type'] = session_type
        if user_agent:
            headers['User-Agent'] = user_agent

        r = self.session.post(self.base_url, headers=headers, json=data)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']

    def delete(self, user_uuid, refresh_token_uuid, tenant_uuid=None):
        headers = dict(self._rw_headers)
        tenant_uuid = tenant_uuid or self._client.tenant()
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        url = self._client.url('users', user_uuid, 'tokens', refresh_token_uuid)

        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

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

    def list(self, user_uuid=None, **kwargs):
        if user_uuid is None:
            raise TypeError('user_uuid cannot be None')

        headers = dict(self._ro_headers)
        tenant_uuid = kwargs.pop('tenant_uuid', self._client.tenant())
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        url = self._client.url('users', user_uuid, 'tokens')

        r = self.session.get(url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
