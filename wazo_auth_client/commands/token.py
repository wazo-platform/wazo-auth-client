# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Any

import requests
import requests.auth
from wazo_lib_rest_client import RESTCommand

from ..exceptions import InvalidTokenException, MissingPermissionsTokenException
from ..types import JSON, TokenDict


class TokenCommand(RESTCommand):
    resource = 'token'
    _user_agent = 'Wazo Python auth client'

    def new(
        self,
        backend: str | None = None,
        expiration: int | None = None,
        session_type: str | None = None,
        user_agent: str | None = None,
        access_type: str | None = None,
        client_id: str | None = None,
        refresh_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        tenant_id: str | None = None,
        domain_name: str | None = None,
    ) -> TokenDict:
        data: dict[str, Any] = {}
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
        if domain_name:
            data['domain_name'] = domain_name

        headers = self._get_headers()
        headers['User-Agent'] = self._user_agent
        if session_type:
            headers['Wazo-Session-Type'] = session_type
        if user_agent:
            headers['User-Agent'] = user_agent

        auth = self.session.auth
        if username and password:
            auth = requests.auth.HTTPBasicAuth(
                username.encode('utf-8'), password.encode('utf-8')
            )
        r = self.session.post(self.base_url, headers=headers, json=data, auth=auth)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']

    def delete(
        self, user_uuid: str, client_id: str, tenant_uuid: str | None = None
    ) -> None:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._client.url('users', user_uuid, 'tokens', client_id)
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def revoke(self, token: str) -> None:
        headers = self._get_headers()
        url = f'{self.base_url}/{token}'
        self.session.delete(url, headers=headers)

    def check(
        self, token: str, required_acl: str | None = None, tenant: str | None = None
    ) -> bool:
        params = {}
        if required_acl:
            params['scope'] = required_acl
        if tenant:
            params['tenant'] = tenant

        headers = self._get_headers()
        url = f'{self.base_url}/{token}'
        r = self.session.head(url, headers=headers, params=params)
        if r.status_code == 204:
            return True
        elif r.status_code == 404:
            raise InvalidTokenException()
        elif r.status_code == 403:
            raise MissingPermissionsTokenException()
        else:
            self.raise_from_response(r)
            return False

    def is_valid(
        self, token: str, required_acl: str | None = None, tenant: str | None = None
    ) -> bool:
        params = {}
        if required_acl:
            params['scope'] = required_acl
        if tenant:
            params['tenant'] = tenant

        headers = self._get_headers()
        url = f'{self.base_url}/{token}'
        r = self.session.head(url, headers=headers, params=params)
        if r.status_code in (204, 403, 404):
            return r.status_code == 204
        else:
            self.raise_from_response(r)
            return False

    def check_scopes(
        self, token: str, scopes: list[str], tenant: str | None = None
    ) -> JSON:
        data: dict[str, Any] = {'scopes': scopes}
        if tenant:
            data['tenant_uuid'] = tenant

        headers = self._get_headers()
        headers['User-Agent'] = self._user_agent
        url = f'{self.base_url}/{token}/scopes/check'
        r = self.session.post(url, headers=headers, json=data)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def get(
        self, token: str, required_acl: str | None = None, tenant: str | None = None
    ) -> TokenDict:
        params = {}
        if required_acl:
            params['scope'] = required_acl
        if tenant:
            params['tenant'] = tenant

        headers = self._get_headers()
        url = f'{self.base_url}/{token}'
        r = self.session.get(url, headers=headers, params=params)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()['data']

    def list(self, user_uuid: str | None = None, **kwargs: Any) -> list[TokenDict]:
        if user_uuid is None:
            raise TypeError('user_uuid cannot be None')

        headers = self._get_headers(**kwargs)
        url = self._client.url('users', user_uuid, 'tokens')
        r = self.session.get(url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()
