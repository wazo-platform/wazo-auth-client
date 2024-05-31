# Copyright 2020-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from wazo_lib_rest_client import RESTCommand

from ..types import SSOResponseDict


class SAMLCommand(RESTCommand):
    resource = 'saml'

    def sso(self, domain: str, redirect_url: str) -> SSOResponseDict:
        data = {}
        data['redirect_url'] = redirect_url
        data['domain'] = domain
        headers = self._get_headers()
        url = f'{self.base_url}/sso'
        r = self.session.post(url, headers=headers, json=data)
        if r.status_code != 200:
            self.raise_from_response(r)
        return r.json()

    def acs(self, saml_response: str, relay_state: str) -> str:
        data = {}
        data['RelayState'] = relay_state
        data['SAMLResponse'] = saml_response
        headers = self._get_headers()
        url = f'{self.base_url}/acs'
        r = self.session.post(url, headers=headers, data=data, allow_redirects=False)
        if r.status_code != 302:
            self.raise_from_response(r)
        return r.headers['Location']
