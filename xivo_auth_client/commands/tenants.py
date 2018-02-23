# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
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


class TenantsCommand(RESTCommand):

    resource = 'tenants'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def add_policy(self, tenant_uuid, policy_uuid):
        url = '/'.join([self.base_url, tenant_uuid, 'policies', policy_uuid])

        r = self.session.put(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def add_user(self, tenant_uuid, user_uuid):
        url = self._user_relation_url(tenant_uuid, user_uuid)

        r = self.session.put(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, tenant_uuid):
        url = '{}/{}'.format(self.base_url, tenant_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, tenant_uuid, **kwargs):
        url = '{}/{}'.format(self.base_url, tenant_uuid)

        r = self.session.put(url, headers=self.headers, data=json.dumps(kwargs))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, tenant_uuid):
        url = '{}/{}'.format(self.base_url, tenant_uuid)

        r = self.session.get(url)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_policies(self, tenant_uuid, **kwargs):
        url = '/'.join([self.base_url, tenant_uuid, 'policies'])

        r = self.session.get(url, headers=self.headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_users(self, tenant_uuid, **kwargs):
        url = '{}/{}/users'.format(self.base_url, tenant_uuid)

        r = self.session.get(url, headers=self.headers, params=kwargs)

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

    def remove_policy(self, tenant_uuid, policy_uuid):
        url = '/'.join([self.base_url, tenant_uuid, 'policies', policy_uuid])

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def remove_user(self, tenant_uuid, user_uuid):
        url = self._user_relation_url(tenant_uuid, user_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def _user_relation_url(self, tenant_uuid, user_uuid):
        return '{}/{}/users/{}'.format(self.base_url, tenant_uuid, user_uuid)
