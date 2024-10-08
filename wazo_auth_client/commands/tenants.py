# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Any

from wazo_lib_rest_client import RESTCommand

from ..types import JSON


class TenantsCommand(RESTCommand):
    resource = 'tenants'
    _ro_headers = {'Accept': 'application/json'}
    _rw_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def add_policy(self, tenant_uuid: str, policy_uuid: str) -> None:
        headers = self._get_headers()
        url = '/'.join([self.base_url, tenant_uuid, 'policies', policy_uuid])
        r = self.session.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, uuid: str, tenant_uuid: str | None = None) -> None:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/{uuid}'
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, tenant_uuid: str, **kwargs: Any) -> JSON:
        headers = self._get_headers()
        url = f'{self.base_url}/{tenant_uuid}'
        r = self.session.put(url, headers=headers, json=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def get(self, tenant_uuid: str) -> JSON:
        headers = self._get_headers()
        url = f'{self.base_url}/{tenant_uuid}'
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list(self, tenant_uuid: str | None = None, **kwargs: Any) -> JSON:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        r = self.session.get(self.base_url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def new(self, **kwargs: Any) -> JSON:
        parent_uuid = kwargs.pop('parent_uuid', None)
        headers = self._get_headers(tenant_uuid=parent_uuid)
        r = self.session.post(self.base_url, headers=headers, json=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def remove_policy(self, tenant_uuid: str, policy_uuid: str) -> None:
        headers = self._get_headers()
        url = '/'.join([self.base_url, tenant_uuid, 'policies', policy_uuid])
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def get_domains(self, tenant_uuid: str) -> JSON:
        url = f'{self.base_url}/{tenant_uuid}/domains'
        r = self.session.get(url)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()
