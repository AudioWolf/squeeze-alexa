# -*- coding: utf-8 -*-
#
#   Copyright 2017 Nick Boultbee
#   This file is part of squeeze-alexa.
#
#   squeeze-alexa is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   See LICENSE for full license

from squeezealexa.ssl_wrap import SslSocketWrapper
from squeezealexa.utils import print_d


class FakeSsl(SslSocketWrapper):

    def __init__(self, fake_name='fake', fake_id='1234'):
        self.hostname = 'localhost'
        self.port = 0
        self.failures = 0
        self.is_connected = True
        self.player_name = fake_name
        self.player_id = fake_id

    def communicate(self, data, wait=True):
        print_d("Faking server status...")
        stripped = data.rstrip('\n')
        if data.startswith('serverstatus'):
            return ('{orig} player%20count:1 playerid:{pid} name:{name}\n'
                    .format(orig=stripped, name=self.player_name,
                            pid=self.player_id))
        return stripped + ' OK\n'
