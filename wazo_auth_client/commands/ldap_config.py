# Copyright 2022-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from wazo_lib_rest_client import RESTCommand

from .._types import JSON


class LDAPBackendConfigCommand(RESTCommand):
    resource = 'backends'

    def get(self, tenant_uuid: str | None = None) -> JSON:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/ldap'
        r = self.session.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def update(
        self, ldap_config: dict[str, JSON], tenant_uuid: str | None = None
    ) -> JSON:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/ldap'
        r = self.session.put(url, headers=headers, json=ldap_config)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def delete(self, tenant_uuid: str | None = None) -> None:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/ldap'
        r = self.session.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)
