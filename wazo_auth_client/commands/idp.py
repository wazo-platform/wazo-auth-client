# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from wazo_lib_rest_client import RESTCommand

from ..types import JSON


class IDPCommand(RESTCommand):
    resource = 'idp'
    _ro_headers = {'Accept': 'application/json'}

    def list(self) -> JSON:
        headers = self._get_headers()
        r = self.session.get(self.base_url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def add_user(self, idp_type: str, user_uuid: str) -> None:
        headers = self._get_headers()
        url = self._relation_url('users', idp_type, user_uuid)
        r = self.session.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def add_users(self, idp_type: str, users: JSON) -> None:
        headers = self._get_headers()
        url = self._relation_url('users', idp_type)
        r = self.session.put(url, headers=headers, json={'users': users})
        if r.status_code != 204:
            self.raise_from_response(r)

    def remove_user(self, idp_type: str, user_uuid: str) -> None:
        headers = self._get_headers()
        url = self._relation_url('users', idp_type, user_uuid)
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def _relation_url(
        self,
        resource: str,
        idp_type: str,
        resource_uuid: str | None = None,
    ) -> str:
        if resource_uuid:
            return '/'.join([self.base_url, idp_type, resource, resource_uuid])
        else:
            return '/'.join([self.base_url, idp_type, resource])
