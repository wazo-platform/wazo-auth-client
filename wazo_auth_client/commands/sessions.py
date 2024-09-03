# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Any

from wazo_lib_rest_client import RESTCommand

from ..types import JSON


class SessionsCommand(RESTCommand):
    resource = 'sessions'

    def list(self, **kwargs: Any) -> JSON:
        headers = self._get_headers(**kwargs)
        r = self.session.get(self.base_url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def delete(self, session_uuid: str, tenant_uuid: str | None = None) -> None:
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/{session_uuid}'
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)
