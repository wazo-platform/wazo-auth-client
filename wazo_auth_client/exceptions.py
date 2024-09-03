# Copyright 2022-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


class InvalidTokenException(BaseException):
    pass


class MissingPermissionsTokenException(BaseException):
    pass
