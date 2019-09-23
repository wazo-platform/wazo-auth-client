# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase
from pytest import raises

from mock import Mock

from wazo_auth_client import Client
from ..token import TokenCommand


class TestTokenCommand(TestCase):
    def setUp(self):
        self.client = Client('host')
        self.client.session = Mock()
        self.session = self.client.session.return_value

        self.command = TokenCommand(self.client)


class TestTokenList(TestTokenCommand):
    def test_that_the_user_uuid_is_a_string(self):
        with raises(TypeError, match='user_uuid must be a string'):
            self.command.list()

        self.command.list(user_uuid='me')

        headers = {'Accept': 'application/json'}
        self.session.get.assert_called_once_with(
            'https://host:9497/0.1/users/me/tokens', headers=headers, params={}
        )
