# -*- coding: utf-8 -*-
# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client import RESTCommand


class AdminCommand(RESTCommand):

    resource = 'admin'
    _rw_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def update_user_emails(self, user_uuid, emails):
        url = '{}/users/{}/emails'.format(self.base_url, user_uuid)

        body = {'emails': emails}

        r = self.session.put(url, headers=self._rw_headers, json=body)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
