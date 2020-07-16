# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''
from __future__ import absolute_import, unicode_literals

from tulip import control, directory
from ..modules.constants import ART_ID, LOGOS_ID


class Indexer:

    def __init__(self):

        self.addons = [
            {
                'title': 'E-RADIO ADDON',
                'image': control.addonmedia('ERADIO.png', LOGOS_ID, theme='logos', media_subfolder=False),
                'url': 'plugin.audio.eradio.gr'
            }
            ,
            {
                'title': 'EPT PLAYER RADIO STATIONS',
                'image': control.addonmedia(addonid=ART_ID, theme='networks', icon='ert_fanart.jpg', media_subfolder=False),
                'url': 'plugin.video.ert.gr',
                'query': 'radios'
            }
            ,
            {
                'title': 'SOMAFM ADDON',
                'image': 'https://alivegr.net/logos/SOMAFM.png',
                'url': 'plugin.audio.somafm.com'
            }
        ]

    def radio(self):

        for station in self.addons:
            station.update({'action': 'activate_audio_addon', 'isFolder': 'False', 'isPlayable': 'False' })

        directory.add(self.addons)
