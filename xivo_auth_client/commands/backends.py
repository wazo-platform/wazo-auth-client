# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

from xivo_lib_rest_client import RESTCommand


class BackendsCommand(RESTCommand):

    resource = 'backends'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def list(self):
        r = self.session.get(self.base_url, headers=self.headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']
