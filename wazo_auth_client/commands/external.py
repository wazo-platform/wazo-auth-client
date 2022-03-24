# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_lib_rest_client import RESTCommand


class ExternalAuthCommand(RESTCommand):

    resource = 'users'

    def create(self, auth_type, user_uuid, data):
        headers = self._get_headers()
        url = self._build_url(auth_type, user_uuid)
        r = self.session.post(url, headers=headers, json=data)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def create_config(self, auth_type, data, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)
        r = self.session.post(url, headers=headers, json=data)
        if r.status_code != 201:
            self.raise_from_response(r)
        return r.json()

    def delete(self, auth_type, user_uuid):
        headers = self._get_headers()
        url = self._build_url(auth_type, user_uuid)
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete_config(self, auth_type, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def get(self, auth_type, user_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_url(auth_type, user_uuid)
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_config(self, auth_type, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def list_(self, user_uuid, **kwargs):
        headers = self._get_headers()
        url = '/'.join([self.base_url, user_uuid, 'external'])
        r = self.session.get(url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def update(self, auth_type, user_uuid, data):
        headers = self._get_headers()
        url = self._build_url(auth_type, user_uuid)
        r = self.session.put(url, headers=headers, json=data)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def update_config(self, auth_type, data, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._build_config_url(auth_type)
        r = self.session.put(url, headers=headers, json=data)
        if r.status_code != 204:
            self.raise_from_response(r)

    def _build_url(self, auth_type, user_uuid):
        return '/'.join([self.base_url, user_uuid, 'external', auth_type])

    def _build_config_url(self, auth_type):
        return '/'.join([self._client.url('external'), auth_type, 'config'])
