# -*- coding: utf-8 -*-
# Copyright 2017-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from six.moves.urllib.parse import quote
from wazo_lib_rest_client import RESTCommand


class PoliciesCommand(RESTCommand):

    resource = 'policies'
    _ro_headers = {'Accept': 'application/json'}
    _rw_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def add_access(self, policy_uuid, access):
        access = quote(access)
        url = '{}/{}/acl/{}'.format(self.base_url, policy_uuid, access)

        r = self.session.put(url, headers=self._ro_headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, policy_uuid):
        url = '{}/{}'.format(self.base_url, policy_uuid)

        r = self.session.delete(url, headers=self._ro_headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, policy_uuid, name, **kwargs):
        url = '{}/{}'.format(self.base_url, policy_uuid)
        kwargs['name'] = name
        r = self.session.put(url, headers=self._rw_headers, json=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, policy_uuid):
        url = '{}/{}'.format(self.base_url, policy_uuid)

        r = self.session.get(url)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_tenants(self, policy_uuid, **kwargs):
        url = '/'.join([self.base_url, policy_uuid, 'tenants'])

        r = self.session.get(url, headers=self._ro_headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list(self, tenant_uuid=None, **kwargs):
        headers = dict(self._ro_headers)

        tenant_uuid = tenant_uuid or self._client.tenant()
        if tenant_uuid:
            headers['Wazo-Tenant'] = str(tenant_uuid)

        r = self.session.get(self.base_url, headers=headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def new(self, name, tenant_uuid=None, **kwargs):
        headers = dict(self._rw_headers)

        tenant_uuid = tenant_uuid or self._client.tenant()
        if tenant_uuid:
            headers['Wazo-Tenant'] = str(tenant_uuid)

        kwargs['name'] = name
        r = self.session.post(self.base_url, headers=headers, json=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def remove_access(self, policy_uuid, access):
        access = quote(access)
        url = '{}/{}/acl/{}'.format(self.base_url, policy_uuid, access)

        r = self.session.delete(url, headers=self._ro_headers)

        if r.status_code != 204:
            self.raise_from_response(r)
