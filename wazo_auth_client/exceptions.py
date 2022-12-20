# Copyright 2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class InvalidTokenException(BaseException):
    pass


class MissingPermissionsTokenException(BaseException):
    pass
