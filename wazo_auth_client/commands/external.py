# -*- coding: utf-8 -*-
# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client import RESTCommand


class ExternalAuthCommand(RESTCommand):

    resource = 'users'
    _ro_headers = {'Accept': 'application/json'}
    _rw_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def create(self, auth_type, user_uuid, data):
        url = self._build_url(auth_type, user_uuid)

        r = self.session.post(url, headers=self._rw_headers, json=data)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def create_config(self, auth_type, data, tenant_uuid=None):
        url = self._build_config_url(auth_type)
        headers = dict(self._rw_headers)

        tenant_uuid = tenant_uuid or self._client.tenant()
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        r = self.session.post(url, headers=headers, json=data)

        if r.status_code != 201:
            self.raise_from_response(r)

        return r.json()

    def delete(self, auth_type, user_uuid):
        url = self._build_url(auth_type, user_uuid)

        r = self.session.delete(url, headers=self._ro_headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_config(self, auth_type, tenant_uuid=None):
        url = self._build_config_url(auth_type)
        headers = dict(self._rw_headers)

        tenant_uuid = tenant_uuid or self._client.tenant()
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def get(self, auth_type, user_uuid):
        url = self._build_url(auth_type, user_uuid)

        r = self.session.get(url, headers=self._ro_headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_config(self, auth_type, tenant_uuid=None):
        url = self._build_config_url(auth_type)
        headers = dict(self._ro_headers)

        tenant_uuid = tenant_uuid or self._client.tenant()
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list_(self, user_uuid, **kwargs):
        url = '/'.join([self.base_url, user_uuid, 'external'])

        r = self.session.get(url, headers=self._ro_headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def update(self, auth_type, user_uuid, data):
        url = self._build_url(auth_type, user_uuid)

        r = self.session.put(url, headers=self._rw_headers, json=data)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def update_config(self, auth_type, data, tenant_uuid=None):
        url = self._build_config_url(auth_type)
        headers = dict(self._rw_headers)

        tenant_uuid = tenant_uuid or self._client.tenant()
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        r = self.session.put(url, headers=headers, json=data)
        if r.status_code != 204:
            self.raise_from_response(r)

    def _build_url(self, auth_type, user_uuid):
        return '/'.join([self.base_url, user_uuid, 'external', auth_type])

    def _build_config_url(self, auth_type):
        return '/'.join([self._client.url('external'), auth_type, 'config'])
