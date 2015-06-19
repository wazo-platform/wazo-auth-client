# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import logging
import subprocess
import unittest
import os

from hamcrest import assert_that
from hamcrest import contains_inanyorder
from hamcrest import equal_to
from hamcrest import is_
from hamcrest import has_key
from requests.exceptions import HTTPError, SSLError

from xivo_auth_client import Client

logger = logging.getLogger(__name__)

ASSET_ROOT = os.path.join(os.path.dirname(__file__), '..', 'assets')
HOST = os.getenv('XIVO_AUTH_CLIENT_TEST_HOST', 'localhost')


class TestXiVOAuthClient(unittest.TestCase):

    asset = 'mock_backend'

    @staticmethod
    def _run_cmd(cmd):
        process = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = process.communicate()
        logger.info('%s', out)

    @classmethod
    def setUpClass(cls):
        asset_path = os.path.join(ASSET_ROOT, cls.asset)
        os.chdir(asset_path)
        cls._run_cmd('docker-compose rm --force')
        cls._run_cmd('docker-compose run sync')

    @classmethod
    def tearDownClass(cls):
        cls._run_cmd('docker-compose kill')

    def setUp(self):
        self.good_client = Client(HOST, username='foo', password='bar')

    def test_new_with_a_successful_login(self):
        token_data = self.good_client.token.new('mock')

        assert_that(token_data['auth_id'], equal_to('a-mocked-uuid'))
        assert_that(token_data, has_key('token'))
        assert_that(token_data, has_key('issued_at'))
        assert_that(token_data, has_key('expires_at'))

    def test_new_with_a_successful_login_wrong_backend(self):
        self.assertRaises(HTTPError, self.good_client.token.new, 'unknown')

    def test_new_with_wrong_credential(self):
        bad_client = Client(HOST, username='foo', password='baz')

        self.assertRaises(HTTPError, bad_client.token.new, 'mock')

    def test_new_verify_certificate_not_configured(self):
        safe_client = Client(HOST, username='foo', password='baz', verify_certificate=True)

        self.assertRaises(SSLError, safe_client.token.new, 'mock')

    def test_new_verify_certificate_configured(self):
        certificate_path = os.path.join(ASSET_ROOT, 'ssl', 'server.crt')
        safe_client = Client(HOST, username='foo', password='baz', verify_certificate=certificate_path)

        safe_client.token.is_valid('abcd')
        # Does not raise

    def test_is_valid_with_an_invalid_token(self):
        response = self.good_client.token.is_valid('abcdef')

        assert_that(response, is_(False))

    def test_is_valid_with_a_valid_token(self):
        token = self.good_client.token.new('mock')['token']

        response = self.good_client.token.is_valid(token)

        assert_that(response, is_(True))

    def test_backends_list(self):
        backends = self.good_client.backends.list()

        assert_that(backends, contains_inanyorder('mock'))

    def test_that_get_returns_the_token_data(self):
        token_data = self.good_client.token.new('mock')

        result = self.good_client.token.get(token_data['token'])

        assert_that(result, equal_to(token_data))

    def test_that_get_raises_an_http_error_on_unknown_token(self):
        self.assertRaises(HTTPError, self.good_client.token.get, 'unknown')

    def test_revoking_a_token(self):
        token = self.good_client.token.new('mock')['token']

        self.good_client.token.revoke(token)

        assert_that(self.good_client.token.is_valid(token), is_(False))
