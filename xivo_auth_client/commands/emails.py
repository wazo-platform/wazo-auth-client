# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from xivo_lib_rest_client import RESTCommand


class EmailsCommand(RESTCommand):

    resource = 'emails'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def confirm(self, email_uuid):
        url = '/'.join([self.base_url, email_uuid, 'confirm'])

        r = self.session.put(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)
