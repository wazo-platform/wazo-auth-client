# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

from typing import TypedDict, Union

from typing_extensions import TypeAlias


class TokenMetadataDict(TypedDict):
    uuid: str
    tenant_uuid: str
    auth_id: str
    pbx_user_uuid: str
    xivo_uuid: str


class TokenMetadataStackDict(TokenMetadataDict, total=False):
    purpose: str
    admin: str


class TokenDict(TypedDict):
    token: str
    session_uuid: str
    metadata: TokenMetadataDict
    acl: list[str]
    auth_id: str
    xivo_uuid: str
    expires_at: str
    utc_expires_at: str
    issued_at: str
    utc_issued_at: str
    user_agent: str
    remote_addr: str


class SSODict(TypedDict):
    location: str
    saml_session_id: str


JSON: TypeAlias = Union[str, int, float, bool, None, list['JSON'], dict[str, 'JSON']]
