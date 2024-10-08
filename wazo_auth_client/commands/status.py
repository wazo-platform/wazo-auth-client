# Copyright 2020-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from wazo_lib_rest_client import RESTCommand


class StatusCommand(RESTCommand):
    resource = 'status'

    def check(self) -> None:
        headers = self._get_headers()
        r = self.session.head(self.base_url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
