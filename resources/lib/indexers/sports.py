# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Thgiliwt

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

from tulip import control, directory
from ..modules.themes import iconname
from ..modules import syshandle


class Main:

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
                    'title': 'EPT Sports',
                    'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='ert_icon.png'),
                    'url': 'plugin://plugin.video.ert.gr/?action=episodes&url=http%3a%2f%2fwebtv.ert.gr%2fcategory%2fkatigories%2fathlitika%2f',
                    'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='ert_fanart.jpg')
                }
                ,
                {
                    'title': 'Skai Sports',
                    'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='skai_icon.png'),
                    'url': 'plugin://plugin.video.skai.gr/?action=sports',
                    'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='skai_fanart.jpg')
                }
                ,
                {
                    'title': 'Euronews Sports',
                    'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='euronews_icon.png'),
                    'url': 'plugin://plugin.video.euronews.com/?action=videos&url=%22methodName%22%3a%22content.getThemeDetails%22%2c%22params%22%3a%7b%22tId%22%3a%228%22%7d',
                    'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='euronews_fanart.jpg')
                }
                ,
                {
                    'title': 'NovaSports',
                    'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='nova_icon.png'),
                    'url': 'plugin://plugin.video.novasports.gr/',
                    'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='nova_fanart.jpg')
                }
        ]

        for item in self.data:
            list_item = control.item(label=item['title'])
            list_item.setArt({'icon': item['icon'], 'fanart': item['fanart']})
            _url_ = item['url']
            isFolder = True
            self.list.append((_url_, list_item, isFolder))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)
