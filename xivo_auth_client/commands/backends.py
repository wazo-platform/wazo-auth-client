# -*- coding: utf-8 -*-
# Copyright 2015-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_lib_rest_client import RESTCommand


class BackendsCommand(RESTCommand):

    resource = 'backends'
    _ro_headers = {'Accept': 'application/json'}

    def list(self):
        r = self.session.get(self.base_url, headers=self._ro_headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']
