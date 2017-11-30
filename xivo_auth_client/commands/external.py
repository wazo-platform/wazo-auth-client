# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

import json

from xivo_lib_rest_client import RESTCommand


class ExternalAuthCommand(RESTCommand):

    resource = 'users'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def create(self, auth_type, user_uuid, data):
        url = self._build_url(auth_type, user_uuid)

        r = self.session.post(url, headers=self.headers, data=json.dumps(data))
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def delete(self, auth_type, user_uuid):
        url = self._build_url(auth_type, user_uuid)

        r = self.session.delete(url, headers=self.headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def get(self, auth_type, user_uuid):
        url = self._build_url(auth_type, user_uuid)

        r = self.session.get(url, headers=self.headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def update(self, auth_type, user_uuid, data):
        url = self._build_url(auth_type, user_uuid)

        r = self.session.put(url, headers=self.headers, data=json.dumps(data))
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def _build_url(self, auth_type, user_uuid):
        return '/'.join([self.base_url, user_uuid, 'external', auth_type])
