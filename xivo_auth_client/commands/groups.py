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


class GroupsCommand(RESTCommand):

    resource = 'groups'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def delete(self, group_uuid):
        url = '{}/{}'.format(self.base_url, group_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, group_uuid, **params):
        url = '{}/{}'.format(self.base_url, group_uuid)

        r = self.session.put(url, headers=self.headers, data=json.dumps(params))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, group_uuid):
        url = '{}/{}'.format(self.base_url, group_uuid)

        r = self.session.get(url)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list(self, **kwargs):
        r = self.session.get(
            self.base_url,
            headers=self.headers,
            params=kwargs,
        )

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def new(self, **kwargs):
        r = self.session.post(self.base_url, headers=self.headers, data=json.dumps(kwargs))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
