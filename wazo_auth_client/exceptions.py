# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

class APIException(Exception):
    def __init__(self, status_code, message, error_id, details=None, resource=None):
        self.status_code = status_code
        self.message = message
        self.id_ = error_id
        self.details = details or {}
        self.resource = resource

class InvalidTokenException(APIException):
    def __init__(self, token, required_access=None, cause=None):
        details = {'invalid_token': token}
        if required_access:
            details['required_access'] = required_access
        if cause:
            details['reason'] = cause
        super(InvalidTokenException, self).__init__(
            status_code=401,
            message='Unauthorized',
            error_id='unauthorized',
            details=details,
        )

class MissingPermissionsTokenException(APIException):
    def __init__(self, token, required_access=None, cause=None):
        details = {'invalid_token': token}
        if required_access:
            details['required_access'] = required_access
        if cause:
            details['reason'] = cause
        super(MissingPermissionsTokenException, self).__init__(
            status_code=401,
            message='Unauthorized',
            error_id='unauthorized',
            details=details,
        )
