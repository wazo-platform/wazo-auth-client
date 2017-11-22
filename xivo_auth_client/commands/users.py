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


class UsersCommand(RESTCommand):

    resource = 'users'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def add_policy(self, user_uuid, policy_uuid):
        url = '{}/{}/policies/{}'.format(self.base_url, user_uuid, policy_uuid)

        r = self.session.put(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, user_uuid):
        url = '{}/{}'.format(self.base_url, user_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def get(self, user_uuid):
        url = '{}/{}'.format(self.base_url, user_uuid)

        r = self.session.get(url)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_groups(self, user_uuid, **kwargs):
        return self._get_relation('groups', user_uuid, **kwargs)

    def get_policies(self, user_uuid, **kwargs):
        return self._get_relation('policies', user_uuid, **kwargs)

    def get_tenants(self, user_uuid, **kwargs):
        return self._get_relation('tenants', user_uuid, **kwargs)

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

    def remove_policy(self, user_uuid, policy_uuid):
        url = '{}/{}/policies/{}'.format(self.base_url, user_uuid, policy_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def _get_relation(self, resource, user_uuid, **kwargs):
        url = '{}/{}/{}'.format(self.base_url, user_uuid, resource)

        r = self.session.get(url, headers=self.headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
