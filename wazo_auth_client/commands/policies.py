# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from urllib.parse import quote

from wazo_lib_rest_client import RESTCommand


class PoliciesCommand(RESTCommand):
    resource = 'policies'

    def add_access(self, policy_uuid, access):
        headers = self._get_headers()
        access = quote(access)
        url = f'{self.base_url}/{policy_uuid}/acl/{access}'
        r = self.session.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, policy_uuid):
        headers = self._get_headers()
        url = f'{self.base_url}/{policy_uuid}'
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, policy_uuid, name, **kwargs):
        headers = self._get_headers()
        url = f'{self.base_url}/{policy_uuid}'
        kwargs['name'] = name
        r = self.session.put(url, headers=headers, json=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def get(self, policy_uuid):
        headers = self._get_headers()
        url = f'{self.base_url}/{policy_uuid}'
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def list(self, tenant_uuid=None, **kwargs):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        r = self.session.get(self.base_url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def new(self, name, tenant_uuid=None, **kwargs):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        kwargs['name'] = name
        r = self.session.post(self.base_url, headers=headers, json=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def remove_access(self, policy_uuid, access):
        headers = self._get_headers()
        access = quote(access)
        url = f'{self.base_url}/{policy_uuid}/acl/{access}'
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)
