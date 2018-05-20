# -*- coding: utf-8 -*-
#
#   Copyright 2017-18 Nick Boultbee
#   This file is part of squeeze-alexa.
#
#   squeeze-alexa is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   See LICENSE for full license

from typing import List


class Error(Exception):

    def __init__(self, msg, e=None):
        super(Error, self).__init__(msg)
        self.message = msg
        self.__cause__ = e


class Transport:
    """Communications transport
    for half-duplex / send-then-maybe-listen mode of communications"""

    def __init__(self) -> None:
        self.is_connected = False

    def communicate(self, data: str, wait=True) -> List[str]:
        """Send `data`, waiting if `wait` is True
        :param data: String to send.
                     A final newlines will be added if not present
        :param wait: Block for response if True
        :return: response lines, if any"""
        raise NotImplementedError()

    @property
    def details(self):
        """Property for connection details"""
        raise NotImplementedError()

    def __str__(self) -> str:
        return self.details

    def __del__(self) -> None:
        self.is_connected = False
