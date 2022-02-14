# -*- coding: utf-8 -*-
# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client import RESTCommand


class LDAPBackendConfigCommand(RESTCommand):

    resource = 'backends'

    def get(self, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = '{}/ldap'.format(self.base_url)
        r = self.session.get(url, headers=headers)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def update(self, ldap_config, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = '{}/ldap'.format(self.base_url)
        r = self.session.put(url, headers=headers, json=ldap_config)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def delete(self, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = '{}/ldap'.format(self.base_url)
        r = self.session.delete(url, headers=headers)

        if r.status_code != 204:
            self.raise_from_response(r)
