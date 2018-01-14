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


class Indexer:

    def __init__(self):

        self.list = []
        self.addons = [
            {
                'title': 'EPT PLAYER RADIO STATIONS',
                'icon': 'http://alivegr.net/logos/ERT%20PLAYER.png',
                'url': 'plugin://plugin.video.ert.gr/?action=radios'
            }
            ,
            {
                'title': 'E-RADIO ADDON',
                'icon': 'http://alivegr.net/logos/ERADIO.png',
                'url': 'plugin://plugin.audio.eradio.gr/'
            }
            ,
            {
                'title': 'TUNE-IN ADDON',
                'icon': 'http://alivegr.net/logos/TUNE%20IN.png',
                'url': 'plugin://plugin.audio.tuneinradio/'
            }
            ,
            {
                'title': 'SOMAFM ADDON',
                'icon': 'http://alivegr.net/logos/SOMAFM.png',
                'url': 'plugin://plugin.audio.somafm.com/'
            }
        ]

    def radio(self):

        stations = self.addons

        self.list = []

        for station in stations:
            li = control.item(label=station['title'], iconImage=station['icon'], thumbnailImage=station['icon'])
            li.setInfo('music', {'title': station['title']})
            li.setArt({'fanart': control.addonInfo('fanart')})
            url = station['url']
            self.list.append((url, li, True))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)
