# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client import RESTCommand


class AdminCommand(RESTCommand):

    resource = 'admin'

    def update_user_emails(self, user_uuid, emails):
        headers = self._get_headers()
        url = f'{self.base_url}/users/{user_uuid}/emails'
        body = {'emails': emails}
        r = self.session.put(url, headers=headers, json=body)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
