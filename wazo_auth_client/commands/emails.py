# -*- coding: utf-8 -*-
# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client import RESTCommand


class EmailsCommand(RESTCommand):

    resource = 'emails'
    _ro_headers = {'Accept': 'application/json'}

    def confirm(self, email_uuid):
        url = '/'.join([self.base_url, email_uuid, 'confirm'])

        r = self.session.put(url, headers=self._ro_headers)

        if r.status_code != 204:
            self.raise_from_response(r)
