# -*- coding: utf-8 -*-
# Copyright 2015-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests

from wazo_lib_rest_client import RESTCommand

from ..exceptions import InvalidTokenException, MissingPermissionsTokenException


class TokenCommand(RESTCommand):

    resource = 'token'
    _user_agent = 'Wazo Python auth client'

    def new(
        self,
        backend=None,
        expiration=None,
        session_type=None,
        user_agent=None,
        access_type=None,
        client_id=None,
        refresh_token=None,
        username=None,
        password=None,
        tenant_id=None,
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
        if tenant_id:
            data['tenant_id'] = tenant_id

        headers = self._get_headers()
        headers['User-Agent'] = self._user_agent
        if session_type:
            headers['Wazo-Session-Type'] = session_type
        if user_agent:
            headers['User-Agent'] = user_agent

        auth = self.session.auth
        if username and password:
            auth = requests.auth.HTTPBasicAuth(username, password)
        r = self.session.post(self.base_url, headers=headers, json=data, auth=auth)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']

    def delete(self, user_uuid, client_id, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url('users', user_uuid, 'tokens', client_id)
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def revoke(self, token):
        headers = self._get_headers()
        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)
        self.session.delete(url, headers=headers)

    def is_valid(self, token, required_acl=None, tenant=None):
        params = {}
        if required_acl:
            params['scope'] = required_acl
        if tenant:
            params['tenant'] = tenant

        headers = self._get_headers()
        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)
        r = self.session.head(url, headers=headers, params=params)
        if r.status_code == 204:
            return True
        elif r.status_code == 404:
            if not token or self.expiration == 0:
                raise InvalidTokenException(token, required_acl, 'not_found_or_expired')
        elif r.status_code == 403:
            raise MissingPermissionsTokenException(
                token, required_acl, 'missing_permission'
            )
        self.raise_from_response(r)

    def check_scopes(self, token, scopes, tenant=None):
        data = {'scopes': scopes}
        if tenant:
            data['tenant_uuid'] = tenant

        headers = self._get_headers()
        headers['User-Agent'] = self._user_agent
        url = '{base_url}/{token}/scopes/check'.format(
            base_url=self.base_url, token=token
        )
        r = self.session.post(url, headers=headers, json=data)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def get(self, token, required_acl=None, tenant=None):
        params = {}
        if required_acl:
            params['scope'] = required_acl
        if tenant:
            params['tenant'] = tenant

        headers = self._get_headers()
        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)
        r = self.session.get(url, headers=headers, params=params)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()['data']

    def list(self, user_uuid=None, **kwargs):
        if user_uuid is None:
            raise TypeError('user_uuid cannot be None')

        headers = self._get_headers(**kwargs)
        url = self._client.url('users', user_uuid, 'tokens')
        r = self.session.get(url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()
