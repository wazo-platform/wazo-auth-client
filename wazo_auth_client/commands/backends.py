# Copyright 2015-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from wazo_lib_rest_client import RESTCommand


class BackendsCommand(RESTCommand):
    resource = 'backends'

    def list(self):
        headers = self._get_headers()
        r = self.session.get(self.base_url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']
