# -*- coding: utf-8 -*-

# AliveGR Addon
# Author Twilight0
# SPDX-License-Identifier: GPL-3.0-only
# See LICENSES/GPL-3.0-only for more information.

from __future__ import absolute_import, unicode_literals

from tulip import control, directory
from tulip.init import syshandle
from ..modules.themes import iconname
from ..modules.constants import ART_ID


class Indexer:

    def __init__(self):

        self.list = []; self.data = []

    def sports(self):

        self.list = [
            {
                'title': 30116,
                'action': 'sports_news',
                'icon': iconname('news')
            }
            ,
            {
                'title': 30117,
                'action': 'gm_sports',
                'icon': iconname('sports')
            }
            ]

        directory.add(self.list)

    def sports_news(self):

        self.data = [
            {
                'title': 'ERTflix Sports',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='ert_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.ert.gr/?action=categories&url=https%3a%2f%2fwww.ertflix.gr%2fshow%2fsport',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='ert_fanart.jpg', media_subfolder=False)
            }
            # ,
            # {
            #     'title': 'Ant1 Sports',
            #     'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='ant1_icon.png', media_subfolder=False),
            #     'url': 'plugin://plugin.video.antenna.gr/?action=videos&url=https%3a%2f%2fwww.antenna.gr%2fwebtv%2f3062%2fathlitika%3fshowall',
            #     'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='ant1_fanart.jpg', media_subfolder=False)
            # }
            ,
            {
                'title': 'Alpha Sports',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='alpha_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.alphatv.gr/?action=news_episodes&query=19&title=%ce%91%ce%b8%ce%bb%ce%b7%cf%84%ce%b9%ce%ba%ce%b1',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='alpha_fanart.jpg', media_subfolder=False)
            }
            # ,
            # {
            #     'title': 'NovaSports',
            #     'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='nova_icon.png', media_subfolder=False),
            #     'url': 'plugin://plugin.video.novasports.gr/',
            #     'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='nova_fanart.jpg', media_subfolder=False)
            # }
        ]

        for item in self.data:

            list_item = control.item(label=item['title'])
            list_item.setArt({'icon': item['icon'], 'fanart': item['fanart']})
            _url_ = item['url']
            isFolder = True

            self.list.append((_url_, list_item, isFolder))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)
