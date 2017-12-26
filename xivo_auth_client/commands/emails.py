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

from xivo_lib_rest_client import RESTCommand


class EmailsCommand(RESTCommand):

    resource = 'emails'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def confirm(self, email_uuid):
        url = '/'.join([self.base_url, email_uuid, 'confirm'])

        r = self.session.put(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)
