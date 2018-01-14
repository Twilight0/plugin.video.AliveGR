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
from tulip.log import *
from ..modules.themes import iconname
from ..modules.helpers import reset_idx as reset


class Indexer:

    def __init__(self):

        self.list = []

    def root(self):

        self.list = [
            {
                'title': control.lang(30001),
                'action': 'live_tv',
                'icon': iconname('monitor'),
                'id': '30001'
            }
            ,
            {
                'title': control.lang(30036),
                'action': 'pvr_client',
                'icon': iconname('guide'),
                'id': '30036'
            }
            ,
            {
                'title': control.lang(30008),
                'action': 'networks',
                'icon': iconname('networks'),
                'id': '30008'
            }
            ,
            {
                'title': control.lang(30123),
                'action': 'news',
                'icon': iconname('news'),
                'id': '30123'
            }
            ,
            {
                'title': control.lang(30031),
                'action': 'movies',
                'icon': iconname('movies'),
                'id': '30031'
            }
            ,
            {
                'title': control.lang(30083),
                'action': 'short_films',
                'icon': iconname('short'),
                'id': '30083'
            }
            ,
            {
                'title': control.lang(30030),
                'action': 'series',
                'icon': iconname('series'),
                'id': '30030'
            }
            ,
            {
                'title': control.lang(30063),
                'action': 'shows',
                'icon': iconname('shows'),
                'id': '30063'
            }
            ,
            {
                'title': control.lang(30068),
                'action': 'theater',
                'icon': iconname('theater'),
                'id': '30068'
            }
            ,
            {
                'title': control.lang(30079),
                'action': 'documentaries',
                'icon': iconname('documentaries'),
                'id': '30079'
            }
            ,
            {
                'title': control.lang(30094),
                'action': 'sports',
                'icon': iconname('sports'),
                'id': '30094'
            }
            ,
            {
                'title': control.lang(30032),
                'action': 'kids',
                'icon': iconname('kids'),
                'id': '30032'
            }
            ,
            {
                'title': control.lang(30012),
                'action': 'miscellany',
                'icon': iconname('miscellany'),
                'id': '30012'
            }
            ,
            {
                'title': control.lang(30002),
                'action': 'radio',
                'icon': iconname('radios'),
                'id': '30002'
            }
            ,
            {
                'title': control.lang(30125),
                'action': 'music',
                'icon': iconname('music'),
                'id': '30125'
            }
            ,
            {
                'title': control.lang(30095).partition(' ')[0],
                'action': 'search',
                'icon': iconname('search'),
                'id': '30095'
            }
            ,
            {
                'title': control.lang(30055),
                'action': 'bookmarks',
                'icon': iconname('bookmarks'),
                'id': '30055'
            }
            ,
            {
                'title': control.lang(30137),
                'action': 'openSettings&query=0.0' if control.setting('settings_method') == 'true' else 'settings',
                'icon': iconname('settings'),
                'id': '30137'
            }
        ]

        if not control.condVisibility('Pvr.HasTVChannels'):
            del self.list[1]

        if control.setting('show_live') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30001']
        if control.setting('show_pvr') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30036']
        if control.setting('show_networks') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30008']
        if control.setting('show_news') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30123']
        if control.setting('show_movies') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30031']
        if control.setting('show_short_films') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30083']
        if control.setting('show_series') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30030']
        if control.setting('show_shows') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30063']
        if control.setting('show_theater') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30068']
        if control.setting('show_docs') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30079']
        if control.setting('show_sports') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30094']
        if control.setting('show_kids') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30032']
        if control.setting('show_misc') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30012']
        if control.setting('show_radio') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30002']
        if control.setting('show_music') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30125']
        if control.setting('show_search') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30095']
        if control.setting('show_bookmarks') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30055']
        if control.setting('show_settings') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30137']

        for item in self.list:
            refresh = {'title': 30054, 'query': {'action': 'refresh'}}
            cache_clear = {'title': 30056, 'query': {'action': 'cache_clear'}}
            reset_idx = {'title': 30134, 'query': {'action': 'reset_idx'}}
            settings = {'title': 30011, 'query': {'action': 'openSettings'}}
            tools = {'title': 30137, 'query': {'action': 'tools_menu'}}
            item.update({'cm': [refresh, cache_clear, reset_idx, settings, tools]})

        from ..modules.tools import checkpoint
        checkpoint()

        log_info('Main menu loaded, have fun...')
        log_info('Tulip libraries version ~' + ' ' + control.addon('script.module.tulip').getAddonInfo('version'))

        if control.setting('reset-idx') == 'true':
            reset(notify=False)

        directory.add(self.list)

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

        log_notice('Plugin started as music addon, have fun...')
        log_info('Tulip libraries version ~' + ' ' + control.addon('script.module.tulip').getAddonInfo('version'))

        directory.add(self.list)
