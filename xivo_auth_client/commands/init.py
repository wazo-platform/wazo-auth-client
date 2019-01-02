# -*- coding: utf-8 -*-
# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

from xivo_lib_rest_client import RESTCommand


class InitCommand(RESTCommand):

    resource = 'init'
    _rw_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def run(self, **kwargs):
        r = self.session.post(self.base_url, headers=self._rw_headers, data=json.dumps(kwargs))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
