# Copyright 2022-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from typing import Any

from wazo_lib_rest_client import RESTCommand

from ..types import JSON


class SAMLConfigCommand(RESTCommand):
    resource = 'backends'

    def get(self, tenant_uuid: str | None = None) -> JSON:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/saml'
        r = self.session.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def create(
        self, tenant_uuid: str | None = None, **saml_config: dict[str, Any]
    ) -> JSON:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        headers['Content-Type'] = 'multipart/form-data'
        url = f'{self.base_url}/saml'
        r = self.session.post(url, headers=headers, **saml_config)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def update(
        self, tenant_uuid: str | None = None, **saml_config: dict[str, Any]
    ) -> None:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        headers['Content-Type'] = 'multipart/form-data'
        url = f'{self.base_url}/saml'
        r = self.session.put(url, headers=headers, **saml_config)

        if r.status_code != 200:
            self.raise_from_response(r)

    def delete(self, tenant_uuid: str | None = None) -> None:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/saml'
        r = self.session.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def get_acs_template(self) -> JSON:
        url = f'{self.base_url}/saml/acs_url_template'
        r = self.session.get(url)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_metadata(self, tenant_uuid: str) -> Any:
        url = f'{self.base_url}/saml/metadata'
        r = self.session.get(url)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.file
