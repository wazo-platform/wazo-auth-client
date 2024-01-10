# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import builtins
from typing import Any

from wazo_lib_rest_client import RESTCommand

from ..types import JSON


class UsersCommand(RESTCommand):
    resource = 'users'
    _ro_headers = {'Accept': 'application/json'}
    _rw_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def add_policy(
        self, user_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/{user_uuid}/policies/{policy_uuid}'
        r = self.session.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def change_password(self, user_uuid: str, **kwargs: Any) -> None:
        headers = self._get_headers()
        url = '/'.join([self.base_url, user_uuid, 'password'])
        r = self.session.put(url, headers=headers, json=kwargs)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, user_uuid: str, tenant_uuid: str | None = None) -> None:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/{user_uuid}'
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, user_uuid: str, **kwargs: Any) -> JSON:
        headers = self._get_headers(**kwargs)
        url = f'{self.base_url}/{user_uuid}'
        r = self.session.put(url, headers=headers, json=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def get(self, user_uuid: str, tenant_uuid: str | None = None) -> JSON:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/{user_uuid}'
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def get_groups(self, user_uuid: str, **kwargs: Any) -> JSON:
        return self._get_relation('groups', user_uuid, **kwargs)

    def get_policies(self, user_uuid: str, **kwargs: Any) -> JSON:
        return self._get_relation('policies', user_uuid, **kwargs)

    def get_sessions(self, user_uuid: str, **kwargs: Any) -> JSON:
        return self._get_relation('sessions', user_uuid, **kwargs)

    def list(self, **kwargs: Any) -> JSON:
        headers = self._get_headers(**kwargs)
        r = self.session.get(self.base_url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def new(self, **kwargs: Any) -> JSON:
        headers = self._get_headers(**kwargs)
        r = self.session.post(self.base_url, headers=headers, json=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def register(self, **kwargs: Any) -> JSON:
        headers = self._get_headers()
        url = f'{self.base_url}/register'
        r = self.session.post(url, headers=headers, json=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def remove_policy(
        self, user_uuid: str, policy_uuid: str, tenant_uuid: str | None = None
    ) -> None:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/{user_uuid}/policies/{policy_uuid}'
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def remove_session(self, user_uuid: str, session_uuid: str) -> None:
        headers = self._get_headers()
        url = f'{self.base_url}/{user_uuid}/sessions/{session_uuid}'
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def request_confirmation_email(self, user_uuid: str, email_uuid: str) -> None:
        headers = self._get_headers()
        url = f'{self.base_url}/{user_uuid}/emails/{email_uuid}/confirm'
        r = self.session.get(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def reset_password(self, **kwargs: Any) -> None:
        headers = self._get_headers()
        url = f'{self.base_url}/password/reset'
        r = self.session.get(url, headers=headers, params=kwargs)
        if r.status_code != 204:
            self.raise_from_response(r)

    def set_password(
        self, user_uuid: str, password: str, token: str | None = None
    ) -> None:
        url = f'{self.base_url}/password/reset'
        query_string = {'user_uuid': user_uuid}
        body = {'password': password}
        headers = self._get_headers()
        if token:
            headers['X-Auth-Token'] = token

        r = self.session.post(url, headers=headers, params=query_string, json=body)
        if r.status_code != 204:
            self.raise_from_response(r)

    def update_emails(self, user_uuid: str, emails: builtins.list[str]) -> JSON:
        headers = self._get_headers()
        url = f'{self.base_url}/{user_uuid}/emails'
        body = {'emails': emails}
        r = self.session.put(url, headers=headers, json=body)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def _get_relation(
        self,
        resource: str,
        user_uuid: str,
        tenant_uuid: str | None = None,
        **kwargs: Any,
    ) -> Any:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/{user_uuid}/{resource}'
        r = self.session.get(url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()
