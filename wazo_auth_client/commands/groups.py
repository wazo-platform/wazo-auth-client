# Copyright 2017-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from wazo_lib_rest_client import RESTCommand


class GroupsCommand(RESTCommand):
    resource = 'groups'

    def add_policy(self, group_uuid, policy_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._relation_url('policies', group_uuid, policy_uuid)
        r = self.session.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def add_user(self, group_uuid, user_uuid):
        headers = self._get_headers()
        url = self._relation_url('users', group_uuid, user_uuid)
        r = self.session.put(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, group_uuid):
        headers = self._get_headers()
        url = f'{self.base_url}/{group_uuid}'
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, group_uuid, **params):
        headers = self._get_headers()
        url = f'{self.base_url}/{group_uuid}'
        r = self.session.put(url, headers=headers, json=params)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, group_uuid):
        headers = self._get_headers()
        url = f'{self.base_url}/{group_uuid}'
        r = self.session.get(url, headers=headers)
        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_policies(self, group_uuid, tenant_uuid=None, **kwargs):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = f'{self.base_url}/{group_uuid}/policies'

        r = self.session.get(url, headers=headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_users(self, group_uuid, **kwargs):
        headers = self._get_headers()
        url = f'{self.base_url}/{group_uuid}/users'

        r = self.session.get(url, headers=headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list(self, **kwargs):
        headers = self._get_headers(**kwargs)
        r = self.session.get(self.base_url, headers=headers, params=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def new(self, **kwargs):
        headers = self._get_headers(**kwargs)
        r = self.session.post(self.base_url, headers=headers, json=kwargs)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def remove_policy(self, group_uuid, policy_uuid, tenant_uuid=None):
        headers = self._get_headers(tenant_uuid=tenant_uuid)
        url = self._relation_url('policies', group_uuid, policy_uuid)
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def remove_user(self, group_uuid, user_uuid):
        headers = self._get_headers()
        url = self._relation_url('users', group_uuid, user_uuid)
        r = self.session.delete(url, headers=headers)
        if r.status_code != 204:
            self.raise_from_response(r)

    def _relation_url(self, resource, group_uuid, resource_uuid):
        return '/'.join([self.base_url, group_uuid, resource, resource_uuid])
