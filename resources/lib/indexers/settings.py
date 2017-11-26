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
from ..modules.constants import art_id
from tulip import control, directory


class Main:

    def __init__(self):

        self.list = []; self.data = []

    def menu(self):

        self.list = [
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30255),
                'action': 'info',
                'icon': control.addonInfo('icon')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30003),
                'action': 'openSettings',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30005),
                'action': 'openSettings&query=1.0',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30004),
                'action': 'openSettings&query=2.0',
                'icon': iconname('monitor')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30109),
                'action': 'openSettings&query=3.0',
                'icon': iconname('movies')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30138),
                'action': 'openSettings&query=4.0',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30017),
                'action': 'openSettings&query=5.0',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30115),
                'action': 'openSettings&query=6.0',
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
                'title': control.addonInfo('name') + ': ' + control.lang(30110),
                'action': 'changelog',
                'icon': control.addonInfo('icon')
            }
            ,
            {
                'title': 'URLResolver' + ': ' + control.lang(30111).rpartition(' (')[0],
                'action': 'smu_settings&sleep=false',
                'icon': control.addon(id='script.module.urlresolver').getAddonInfo('icon')
            }
        ]

        directory.add(self.list)

    def info(self):

        self.list = [
            {
                'title': control.lang(30105),
                'action': 'dmca',
                'plot': control.addonInfo('disclaimer').decode('utf-8'),
                'icon': control.addonmedia(
                    addonid=art_id, theme='icons', icon='dmca.png', media_subfolder=False
                )
            }
            ,
            {
                'title': control.lang(30260),
                'action': 'none',
                'plot': 'Git repo',
                'icon': control.addonmedia(
                    addonid=art_id, theme='icons', icon='bitbucket.png', media_subfolder=False
                )
            }
            ,
            {
                'title': control.lang(30259),
                'action': 'none',
                'plot': 'RSS feed: https://twitrss.me/twitter_user_to_rss/?user=TwilightZer0',
                'icon': control.addonmedia(addonid=art_id, theme='icons', icon='twitter.png', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30256).format(control.addonInfo('version')),
                'action': 'force',
                'plot': control.lang(30265),
                'icon': control.addonInfo('icon')
            }
            ,
            {
                'title': control.lang(30257).format(control.addon('script.module.tulip').getAddonInfo('version')),
                'action': 'force',
                'plot': control.lang(30265),
                'icon': control.addon('script.module.tulip').getAddonInfo('icon')
            }
            ,
            {
                'title': control.lang(30264).format(control.addon('script.module.urlresolver').getAddonInfo('version')),
                'action': 'force',
                'plot': control.lang(30265),
                'icon': control.addon('script.module.urlresolver').getAddonInfo('icon')
            }
            ,
            {
                'title': control.lang(30258).format(control.addon('xbmc.addon').getAddonInfo('version').rpartition('.')[0]),
                'action': 'system_info',
                'plot': control.lang(30263),
                'icon': control.addonmedia(addonid=art_id, theme='icons', icon='kodi.png', media_subfolder=False)
            }
        ]

        control.execute('Container.SetViewMode(50)')
        directory.add(self.list, content='movies')
