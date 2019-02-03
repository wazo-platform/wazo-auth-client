# -*- coding: utf-8 -*-
# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_lib_rest_client import RESTCommand


class TenantsCommand(RESTCommand):

    resource = 'tenants'
    _ro_headers = {'Accept': 'application/json'}
    _rw_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def add_policy(self, tenant_uuid, policy_uuid):
        url = '/'.join([self.base_url, tenant_uuid, 'policies', policy_uuid])

        r = self.session.put(url, headers=self._ro_headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, tenant_uuid):
        url = '{}/{}'.format(self.base_url, tenant_uuid)

        r = self.session.delete(url, headers=self._ro_headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, tenant_uuid, **kwargs):
        url = '{}/{}'.format(self.base_url, tenant_uuid)

        r = self.session.put(url, headers=self._rw_headers, json=kwargs)

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

        r = self.session.get(url, headers=self._ro_headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_users(self, tenant_uuid, **kwargs):
        url = '{}/{}/users'.format(self.base_url, tenant_uuid)

        r = self.session.get(url, headers=self._ro_headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list(self, tenant_uuid=None, **kwargs):
        headers = dict(self._ro_headers)
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        r = self.session.get(
            self.base_url,
            headers=headers,
            params=kwargs,
        )

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def new(self, **kwargs):
        headers = dict(self._rw_headers)

        parent_uuid = kwargs.pop('parent_uuid', self._client.tenant())
        if parent_uuid:
            headers['Wazo-Tenant'] = parent_uuid

        r = self.session.post(self.base_url, headers=headers, json=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def remove_policy(self, tenant_uuid, policy_uuid):
        url = '/'.join([self.base_url, tenant_uuid, 'policies', policy_uuid])

        r = self.session.delete(url, headers=self._ro_headers)

        if r.status_code != 204:
            self.raise_from_response(r)
