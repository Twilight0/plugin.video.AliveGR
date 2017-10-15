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


from tulip import control
from tulip.init import syshandle


class Main:

    def __init__(self):

        self.list = []

    def news(self):

        networks = [
            {
                'title': control.lang(30118),
                'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='ert_icon.png'),
                'url': 'plugin://plugin.video.ert.gr/?action=episodes&url=http%3a%2f%2fwebtv.ert.gr%2fcategory%2fkatigories%2feidiseis%2f',
                'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='ert_fanart.jpg')
            }
            ,
            {
                'title': control.lang(30119),
                'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='ant1_icon.png'),
                'url': 'plugin://plugin.video.antenna.gr/?action=news',
                'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='ant1_fanart.jpg')
            }
            ,
            {
                'title': control.lang(30120),
                'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='star_icon.png'),
                'url': 'plugin://plugin.video.star.gr/?action=news',
                'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='star_fanart.jpg')
            }
            ,
            {
                'title': control.lang(30122),
                'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='alpha_icon.png'),
                'url': 'plugin://plugin.video.alphatv.gr/?action=news',
                'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='alpha_fanart.jpg')
            }
            ,
            {
                'title': control.lang(30121),
                'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='skai_icon.png'),
                'url': 'plugin://plugin.video.skai.gr/?action=news',
                'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='skai_fanart.jpg')
            }
            ,
            {
                'title': 'Euronews',
                'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='euronews_icon.png'),
                'url': 'plugin://plugin.video.euronews.com/?action=videos&url=%22methodName%22%3a%22content.getThemeDetails%22%2c%22params%22%3a%7b%22tId%22%3a%221%22%7d',
                'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='euronews_fanart.jpg')
            }

        ]

        for network in networks:
            list_item = control.item(label=network['title'])
            list_item.setArt({'icon': network['icon'], 'fanart': network['fanart']})
            url = network['url']
            isFolder = True
            self.list.append((url, list_item, isFolder))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)
