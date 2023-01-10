# -*- coding: utf-8 -*-

# AliveGR Addon
# Author Twilight0
# SPDX-License-Identifier: GPL-3.0-only
# See LICENSES/GPL-3.0-only for more information.
from __future__ import absolute_import, unicode_literals

from tulip import control
from .constants import ART_ID


def theme():

    icon_theme = control.setting('theme')

    if icon_theme == '0':
        return 'alivegr', '+alivegr.png'
    elif icon_theme == '1':
        return 'twilight', '+twilight.png'


def iconname(name):

    icon = control.addonmedia(
        addonid=ART_ID, theme=theme()[0], icon=name + theme()[1], media_subfolder=False
    )

    return icon
