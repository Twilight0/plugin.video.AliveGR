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
from __future__ import absolute_import

from tulip import control, directory
from tulip.log import log_debug
from resources.lib.modules.themes import iconname
from resources.lib.modules.helpers import reset_idx as reset


class Indexer:

    def __init__(self, argv):

        self.list = []; self.menu = []
        self.argv = argv

    def root(self):

        self.list = [
            {
                'title': control.lang(30001),
                'action': 'live_tv',
                'icon': iconname('monitor'),
                'boolean': control.setting('show_live') == 'true'
            }
            ,
            {
                'title': control.lang(30036),
                'action': 'pvr_client',
                'icon': iconname('guide'),
                'boolean': control.setting('show_pvr') == 'true',
                'isFolder': 'False', 'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30008),
                'action': 'networks',
                'icon': iconname('networks'),
                'boolean': control.setting('show_networks') == 'true'
            }
            ,
            {
                'title': control.lang(30123),
                'action': 'news',
                'icon': iconname('news'),
                'boolean': control.setting('show_news') == 'true'
            }
            ,
            {
                'title': control.lang(30031),
                'action': 'movies',
                'icon': iconname('movies'),
                'boolean': control.setting('show_movies') == 'true'
            }
            ,
            {
                'title': control.lang(30083),
                'action': 'short_films',
                'icon': iconname('short'),
                'boolean': control.setting('show_short_films') == 'true'
            }
            ,
            {
                'title': control.lang(30030),
                'action': 'series',
                'icon': iconname('series'),
                'boolean': control.setting('show_series') == 'true'
            }
            ,
            {
                'title': control.lang(30063),
                'action': 'shows',
                'icon': iconname('shows'),
                'boolean': control.setting('show_shows') == 'true'
            }
            ,
            {
                'title': control.lang(30068),
                'action': 'theater',
                'icon': iconname('theater'),
                'boolean': control.setting('show_theater') == 'true'
            }
            # ,
            # {
            #     'title': control.lang(30079),
            #     'action': 'documentaries',
            #     'icon': iconname('documentaries'),
            #     'boolean': control.setting('show_docs') == 'true'
            # }
            ,
            {
                'title': control.lang(30094),
                'action': 'sports',
                'icon': iconname('sports'),
                'boolean': control.setting('show_sports') == 'true'
            }
            ,
            {
                'title': control.lang(30032),
                'action': 'kids',
                'icon': iconname('kids'),
                'boolean': control.setting('show_kids') == 'true'
            }
            ,
            {
                'title': control.lang(30012),
                'action': 'miscellany',
                'icon': iconname('miscellany'),
                'boolean': control.setting('show_misc') == 'true'
            }
            ,
            {
                'title': control.lang(30002),
                'action': 'radio',
                'icon': iconname('radios'),
                'boolean': control.setting('show_radio') == 'true'
            }
            ,
            {
                'title': control.lang(30125),
                'action': 'music',
                'icon': iconname('music'),
                'boolean': control.setting('show_music') == 'true'
            }
            ,
            {
                'title': control.lang(30095).partition(' ')[0],
                'action': 'search',
                'icon': iconname('search'),
                'boolean': control.setting('show_search') == 'true',
                'isFolder': 'False', 'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30055),
                'action': 'bookmarks',
                'icon': iconname('bookmarks'),
                'boolean': control.setting('show_bookmarks') == 'true'
            }
            ,
            {
                'title': control.lang(30137),
                'action': 'openSettings&query=0.0' if control.setting('old_settings') == 'true' else 'settings',
                'icon': iconname('settings'),
                'boolean': control.setting('show_settings') == 'true'
            }
            ,
            {
                'title': control.lang(30288),
                'action': 'quit',
                'icon': iconname('quit'),
                'boolean': control.setting('show_quit') == 'true',
                'isFolder': 'False', 'isPlayable': 'False'
            }
        ]

        self.menu = [i for i in self.list if i['boolean']]

        for item in self.menu:

            refresh = {'title': 30054, 'query': {'action': 'refresh'}}
            cache_clear = {'title': 30056, 'query': {'action': 'cache_clear'}}
            reset_idx = {'title': 30134, 'query': {'action': 'reset_idx'}}
            settings = {'title': 30011, 'query': {'action': 'openSettings'}}
            go_to_audio = {'title': 30321, 'query': {'action': 'activate_audio_addon', 'url': 'plugin.video.AliveGR'}}
            tools = {'title': 30137, 'query': {'action': 'tools_menu'}}
            ii_cm = {'title': 30255, 'query': {'action': 'call_info'}}
            item.update({'cm': [ii_cm, refresh, cache_clear, reset_idx, settings, go_to_audio, tools]})

        log_debug('Main menu loaded, have fun...')
        log_debug('Tulip libraries version ~' + ' ' + control.addon('script.module.tulip').getAddonInfo('version'))

        if control.setting('reset-idx') == 'true':
            reset(notify=False)

        directory.add(self.menu, argv=self.argv)

    def audio(self):

        self.list = [
            {
                'title': 30002,
                'action': 'radio',
                'icon': iconname('radios')
            }
            ,
            {
                'title': 30125,
                'action': 'music',
                'icon': iconname('music')
            }
        ]

        for item in self.list:
            refresh = {'title': 30054, 'query': {'action': 'refresh'}}
            cache_clear = {'title': 30056, 'query': {'action': 'cache_clear'}}
            reset_idx = {'title': 30134, 'query': {'action': 'reset_idx'}}
            settings = {'title': 30011, 'query': {'action': 'openSettings'}}
            tools = {'title': 30137, 'query': {'action': 'tools_menu'}}
            item.update({'cm': [refresh, cache_clear, reset_idx, settings, tools]})

        log_debug('Plugin started as music addon, have fun...')
        log_debug('Tulip libraries version ~' + ' ' + control.addon('script.module.tulip').getAddonInfo('version'))

        directory.add(self.list, argv=self.argv)
