# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

import base64
from contextlib import ExitStack
from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests
from pytest import raises

from wazo_auth_client import Client

from ..token import TokenCommand


class TestTokenCommand(TestCase):
    def setUp(self) -> None:
        self.client = Client('host', port=9497, prefix=None, https=False)
        # NOTE(clanglois): can use patch.object instead of manual monkey patching
        self.client.session = MagicMock()  # type: ignore
        self.session = self.client.session.return_value
        self.command = TokenCommand(self.client)


class TestTokenList(TestTokenCommand):
    def test_that_the_user_uuid_is_a_string(self):
        with raises(TypeError, match='user_uuid cannot be None'):
            self.command.list()

        self.command.list(user_uuid='me')

        headers = {'Accept': 'application/json'}
        self.session.get.assert_called_once_with(
            'http://host:9497/0.1/users/me/tokens', headers=headers, params={}
        )


class TestTokenCreate(TestTokenCommand):
    def setUp(self):
        super().setUp()
        self.session = requests.Session()
        self.stack = ExitStack()
        self.stack.enter_context(patch.object(self.session, 'send'))
        self.client.session = MagicMock(return_value=self.session)  # type: ignore

    def tearDown(self) -> None:
        self.stack.close()
        return super().tearDown()

    def test_token_with_utf_8_username_and_password(self):
        username = 'usernâmê'
        password = 'passŵôŗḑ'
        self.command.new(username=username, password=password)

        request = self.session.send.mock_calls[0].args[0]
        assert 'Authorization' in request.headers, request.headers
        assert 'Basic' in request.headers['Authorization']
        encoded_basic_auth = request.headers['Authorization'].split(' ')[1]
        decoded_basic_auth = base64.b64decode(encoded_basic_auth).decode('utf-8')
        decoded_username, decoded_password = decoded_basic_auth.split(':')
        assert decoded_username == username
        assert decoded_password == password
