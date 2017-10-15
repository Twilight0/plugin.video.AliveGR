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

from tulip import cache, control, client
from tulip.init import sysaddon, syshandle
from ..modules.helpers import thgiliwt


class Main:

    def __init__(self):

        self.list = []
        # self.radios = 's1GeuM3bpRWYy9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'
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

    # def get_radios(self):
    #
    #     xml = client.request(thgiliwt(self.radios))
    #
    #     items = client.parseDOM(xml, 'station', attrs={'enable': '1'})
    #
    #     for item in items:
    #
    #         name = client.parseDOM(item, 'name')[0]
    #         logo = client.parseDOM(item, 'logo')[0]
    #         url = client.parseDOM(item, 'url')[0]
    #
    #         self.list.append({'title': name, 'icon': logo, 'url': url})
    #
    #     self.list.extend(self.addons)
    #
    #     return self.list

    def radio(self):

        # stations = cache.get(self.get_radios, 2)
        stations = self.addons

        self.list = []

        for station in stations:
            li = control.item(label=station['title'], iconImage=station['icon'], thumbnailImage=station['icon'])
            li.setInfo('music', {'title': station['title']})
            li.setArt({'fanart': control.addonInfo('fanart')})
            li.setProperty('IsPlayable', 'true')
            # if station['url'].startswith('plugin://'):
            url = station['url']
            _isFolder = True
            # else:
            #     url = '{0}?action=play&url={1}'.format(sysaddon, station['url'])
            #     _isFolder = False
            self.list.append((url, li, _isFolder))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)
