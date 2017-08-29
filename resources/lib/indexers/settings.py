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

from ..modules.themes import iconname
from tulip import control, directory


class Main:

    def __init__(self):

        self.list = []; self.data = []

    def menu(self):

        self.list = [
            {
                'title': control.lang(30011) + ': ' + control.lang(30003),
                'action': 'openSettings',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30004),
                'action': 'openSettings&query=1.0',
                'icon': iconname('monitor')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30109),
                'action': 'openSettings&query=2.0',
                'icon': iconname('movies')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30138),
                'action': 'openSettings&query=3.0',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30017),
                'action': 'openSettings&query=4.0',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30115),
                'action': 'openSettings&query=5.0',
                'icon': iconname('godmode')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30056),
                'action': 'cache_clear',
                'icon': iconname('empty')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30135),
                'action': 'purge_bookmarks',
                'icon': iconname('empty')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30134),
                'action': 'reset_idx',
                'icon': iconname('settings')
            }
            ,
            {
                'title': 'URLResolver' + ': ' + control.lang(30111).rpartition(' (')[0],
                'action': 'smu_settings&sleep=false',
                'icon': control.addon(id='script.module.urlresolver').getAddonInfo('icon')
            }
        ]

        directory.add(self.list)