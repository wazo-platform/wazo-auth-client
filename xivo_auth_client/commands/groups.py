# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

import json

from xivo_lib_rest_client import RESTCommand


class GroupsCommand(RESTCommand):

    resource = 'groups'
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def add_policy(self, group_uuid, policy_uuid):
        url = self._relation_url('policies', group_uuid, policy_uuid)

        r = self.session.put(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def add_user(self, group_uuid, user_uuid):
        url = self._relation_url('users', group_uuid, user_uuid)

        r = self.session.put(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def delete(self, group_uuid):
        url = '{}/{}'.format(self.base_url, group_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def edit(self, group_uuid, **params):
        url = '{}/{}'.format(self.base_url, group_uuid)

        r = self.session.put(url, headers=self.headers, data=json.dumps(params))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get(self, group_uuid):
        url = '{}/{}'.format(self.base_url, group_uuid)

        r = self.session.get(url)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_policies(self, group_uuid, **kwargs):
        url = '{}/{}/policies'.format(self.base_url, group_uuid)

        r = self.session.get(url, headers=self.headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def get_users(self, group_uuid, **kwargs):
        url = '{}/{}/users'.format(self.base_url, group_uuid)

        r = self.session.get(url, headers=self.headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def list(self, **kwargs):
        headers = dict(self.headers)
        tenant_uuid = kwargs.pop('tenant_uuid', self._client.tenant())
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        r = self.session.get(self.base_url, headers=headers, params=kwargs)

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def new(self, **kwargs):
        headers = dict(self.headers)
        tenant_uuid = kwargs.pop('tenant_uuid', self._client.tenant())
        if tenant_uuid:
            headers['Wazo-Tenant'] = tenant_uuid

        r = self.session.post(self.base_url, headers=headers, data=json.dumps(kwargs))

        if r.status_code != 200:
            self.raise_from_response(r)

        return r.json()

    def remove_policy(self, group_uuid, policy_uuid):
        url = self._relation_url('policies', group_uuid, policy_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def remove_user(self, group_uuid, user_uuid):
        url = self._relation_url('users', group_uuid, user_uuid)

        r = self.session.delete(url, headers=self.headers)

        if r.status_code != 204:
            self.raise_from_response(r)

    def _relation_url(self, resource, group_uuid, resource_uuid):
        return '/'.join([self.base_url, group_uuid, resource, resource_uuid])
