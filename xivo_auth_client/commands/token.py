# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import json

from xivo_lib_rest_client import RESTCommand


class TokenCommand(RESTCommand):

    resource = 'token'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def new(self, backend, expiration=None, backend_args={}):
        data = {'backend': backend}
        if expiration:
            data['expiration'] = expiration
        if backend_args:
            data['backend_args'] = backend_args

        r = self.session.post(self.base_url,
                              headers=self.headers,
                              data=json.dumps(data))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']

    def revoke(self, token):
        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)

        self.session.delete(url, headers=self.headers)

    def is_valid(self, token):
        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)

        r = self.session.head(url, headers=self.headers)

        return r.status_code == 204

    def get(self, token):
        url = '{base_url}/{token}'.format(base_url=self.base_url, token=token)

        r = self.session.get(url, headers=self.headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()['data']
