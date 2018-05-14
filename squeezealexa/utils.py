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

from __future__ import print_function
import random
import re
import unicodedata
import sys
from squeezealexa.i18n import _

Char = chr
Unicode = str


def print_d(msg, *args, **kwargs):
    text = msg.format(*args, **kwargs)
    print(text)
    return text


print_w = print_d


def english_join(items, final=_("and")):
    """Like join, but in English (no Oxford commas...)
       Kinda works in some other languages (French, German)"""
    items = list(filter(None, items))
    most = ", ".join(items[0:-1])
    sep = " %s " % final.strip()
    return sep.join(filter(None, [most] + items[-1:]))


_SPACIFIES = {i: u' ' for i in range(sys.maxunicode)
              if unicodedata.category(Char(i)).startswith('P')}

_REMOVALS = {ord(i): None for i in ['\'', '!']}

_SANITISE = {'&': ' N ',
             '+': ' N ',
             '$': 's'}


def remove_punctuation(text):
    if not isinstance(text, Unicode):
        text = text.decode('utf-8')
    return text.translate(_REMOVALS).translate(_SPACIFIES)


def sanitise_text(text):
    """Makes a genre / playlist / artist name safer for Alexa output"""
    if not text:
        return ""
    safer = text
    for (bad, good) in _SANITISE.items():
        safer = safer.replace(bad, good)
    no_punc = remove_punctuation(safer)
    return re.sub(r'\s{2,}', ' ', no_punc)


def with_example(template, collection):
    msg = template % len(collection)
    if collection:
        msg += " (e.g. \"%s\")" % random.choice(list(collection))
    return msg


def stronger(k, v, extra_bools=None):
    """Return a stronger-typed version of a value if possible"""
    prefixes = set(extra_bools or [])
    prefixes.update({'has', 'is', 'can'})
    try:
        for prefix in prefixes:
            if k.startswith(prefix):
                return bool(int(v))
        try:
            return int(v)
        except ValueError:
            return float(v)
    except ValueError:
        return None if not v else v
