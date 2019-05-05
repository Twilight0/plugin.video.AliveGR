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

from tulip import control, directory
from resources.lib.modules.constants import art_id, logos_id


class Indexer:

    def __init__(self, argv):

        self.list = []
        self.addons = [
            {
                'title': 'E-RADIO ADDON',
                'image': control.addonmedia('ERADIO.png', logos_id, theme='logos', media_subfolder=False),
                'url': 'plugin.audio.eradio.gr'
            }
            ,
            {
                'title': 'EPT PLAYER RADIO STATIONS',
                'image': control.addonmedia(addonid=art_id, theme='networks', icon='ert_fanart.jpg', media_subfolder=False),
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

        self.argv = argv

    def radio(self):

        stations = self.addons

        for station in stations:
            station.update({'action': 'activate_audio_addon', 'isFolder': 'False', 'isPlayable': 'False' })

        directory.add(stations, argv=self.argv)
