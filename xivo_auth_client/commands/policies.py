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

import urllib
import json

from xivo_lib_rest_client import RESTCommand


class PoliciesCommand(RESTCommand):

    resource = 'policies'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def add_acl_template(self, policy_uuid, acl_template):
        acl_template = urllib.quote(acl_template)
        url = '{}/{}/acl_templates/{}'.format(self.base_url, policy_uuid, acl_template)

        r = self.session.put(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, policy_uuid):
        url = '{}/{}'.format(self.base_url, policy_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, policy_uuid, name, description=None, acl_templates=None):
        url = '{}/{}'.format(self.base_url, policy_uuid)
        args = {'name': name}
        if description:
            args['description'] = description
        if acl_templates:
            args['acl_templates'] = acl_templates

        r = self.session.put(url, headers=self.headers, data=json.dumps(args))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, policy_uuid):
        url = '{}/{}'.format(self.base_url, policy_uuid)

        r = self.session.get(url)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list(self, search=None, order=None, direction=None, limit=None, offset=None):
        params = {}
        if search:
            params['search'] = search
        if order:
            params['order'] = order
        if direction:
            params['direction'] = direction
        if limit:
            params['limit'] = limit
        if offset:
            params['offset'] = offset

        r = self.session.get(
            self.base_url,
            headers=self.headers,
            params=params,
        )

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def new(self, name, description=None, acl_templates=None):
        data = {'name': name}
        if description:
            data['description'] = description
        if acl_templates:
            data['acl_templates'] = acl_templates

        r = self.session.post(
            self.base_url,
            headers=self.headers,
            data=json.dumps(data))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def remove_acl_template(self, policy_uuid, acl_template):
        acl_template = urllib.quote(acl_template)
        url = '{}/{}/acl_templates/{}'.format(self.base_url, policy_uuid, acl_template)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)
