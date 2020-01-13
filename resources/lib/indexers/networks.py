# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from __future__ import absolute_import, unicode_literals

from tulip import control
from ..modules.constants import ART_ID


class Indexer:

    def __init__(self, argv):

        self.list = []
        self.argv = argv
        self.syshandle = int(self.argv[1])

    def networks(self):

        networks = [
            {
                'title': 'EPT',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='ert_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.ert.gr/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='ert_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'ANT1',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='ant1_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.antenna.gr/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='ant1_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'STAR',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='star_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.star.gr/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='star_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'ALPHA',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='alpha_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.alphatv.gr/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='alpha_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'SKAI',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='skai_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.skai.gr/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='skai_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'EURONEWS',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='euronews_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.euronews.com/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='euronews_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'NOVASPORTS',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='nova_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.novasports.gr/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='nova_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'GREEK VOICE',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='wzra48_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.greekvoice/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='wzra48_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'TORONTO CHANNELS',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='tc_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.Toronto-Channels/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='tc_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'MONTREAL GREEK TV',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='mg_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.montreal.greek-tv/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='mgtv_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'FAROS ON AIR',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='faros_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.faros.on-air/',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='faros_fanart.jpg', media_subfolder=False)
            }
        ]

        for network in networks:

            list_item = control.item(label=network['title'])
            list_item.setArt({'icon': network['icon'], 'fanart': network['fanart']})
            url = network['url']
            self.list.append((url, list_item, True))

        control.addItems(self.syshandle, self.list)
        control.directory(self.syshandle)
