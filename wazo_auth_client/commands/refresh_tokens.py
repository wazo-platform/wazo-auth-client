# -*- coding: utf-8 -*-
# Copyright 2019-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client import RESTCommand


class RefreshTokenCommand(RESTCommand):

    resource = 'tokens'
    _ro_headers = {'Accept': 'application/json'}
    _rw_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Wazo Python auth client',
    }

    def list(self, **kwargs):
        headers = dict(self._ro_headers)
        tenant_uuid = kwargs.pop('tenant_uuid', self._client.tenant())
        if tenant_uuid:
            headers['Wazo-Tenant'] = str(tenant_uuid)

        r = self.session.get(self.base_url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()
