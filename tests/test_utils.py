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

from unittest import TestCase

from squeezealexa import Settings
from squeezealexa.utils import english_join, sanitise_text, with_example, \
    stronger, print_d, print_w

LOTS = ['foo', 'bar', 'baz', 'quux']


class TestEnglishJoin(TestCase):
    def test_basics(self):
        assert english_join([]) == ''
        assert english_join(['foo']) == 'foo'
        assert english_join(['foo', 'bar']) == 'foo and bar'
        assert english_join(LOTS[:-1]) == 'foo, bar and baz'
        assert english_join(LOTS) == 'foo, bar, baz and quux'

    def test_alternate_join_works(self):
        assert english_join(['foo', 'bar'], 'or') == 'foo or bar'

    def test_tuples_ok(self):
        assert english_join(('foo', 'bar'), 'or') == 'foo or bar'

    def test_skips_falsey(self):
        assert english_join(['foo', None, 'bar', '']) == 'foo and bar'


class TestSanitise(TestCase):
    def test_nothing(self):
        assert sanitise_text("") == ""

    def test_ands(self):
        assert sanitise_text('Drum & Bass') == 'Drum N Bass'
        assert sanitise_text('Drum&Bass') == 'Drum N Bass'
        assert sanitise_text('R&B') == 'R N B'
        assert sanitise_text('Jazz+Funk') == 'Jazz N Funk'

    def test_punctuation(self):
        assert sanitise_text('Alt. Rock') == 'Alt Rock'
        assert sanitise_text('Alt.Rock') == 'Alt Rock'
        assert sanitise_text('Trip-hop') == 'Trip hop'
        assert sanitise_text('Pop/Funk') == 'Pop Funk'

    def test_apostrophes(self):
        assert sanitise_text("10's pop") == '10s pop'

    def test_playlists(self):
        assert sanitise_text("My bad-a$$ playlist") == 'My bad ass playlist'


class TestWithExample(TestCase):
    def test_with_example_zero(self):
        assert with_example("%d words", []) == "0 words"

    def test_with_example(self):
        assert with_example("%d words", ['one']) == '1 words (e.g. "one")'

    def test_with_example_dict(self):
        assert with_example("%d words", {1: 'one'}) == '1 words (e.g. "1")'


class TestStrong(TestCase):
    def test_full(self):
        for (k, v), exp in [(('canpoweroff', '1'), True),
                            (('hasitems', '0'), False),
                            (('duration', '0.0'), 0.0),
                            (('foo', 'bar'), 'bar')]:
            assert stronger(k, v) == exp


class TestLogging(TestCase):
    def test_print_d(self):
        actual = print_d("{foo} - {num:.1f}", foo="bar", num=3.1415)
        assert actual == "bar - 3.1"

    def test_print_w(self):
        assert "Exception" in print_w("{!r}", Exception("bar"))


class FakeSettings(Settings):
    foo = "bar"
    _private = 1234


class TestSettings:
    s = FakeSettings()
    assert "_private" not in str(s)
    assert str(s) == "{'foo': 'bar'}"
