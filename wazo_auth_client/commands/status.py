# -*- coding: utf-8 -*-
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client import RESTCommand


class StatusCommand(RESTCommand):

    resource = 'status'
    _ro_headers = {'Accept': 'application/json'}

    def check(self):
        r = self.session.head(self.base_url, headers=self._ro_headers)

        if r.status_code != 200:
            self.raise_from_response(r)
