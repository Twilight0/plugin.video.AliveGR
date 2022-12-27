# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''
from __future__ import absolute_import, unicode_literals

import json

from tulip import control, directory
from tulip.compat import iteritems
from tulip.log import log_debug
from ..modules.themes import iconname
from ..modules.utils import file_to_text, read_from_file, reset_idx as reset
from ..modules.constants import PLAYBACK_HISTORY


class Indexer:

    def __init__(self):

        self.list = []; self.menu = []

    def root(self):

        log_debug("Opening up")

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
            ,
            {
                'title': control.lang(30079),
                'action': 'listing',
                'url': 'http://greek-movies.com/movies.php?g=6&y=&l=&p=',
                'icon': iconname('documentaries'),
                'boolean': control.setting('show_docs') == 'true'
            }
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
                'action': 'search_index',
                'icon': iconname('search'),
                'boolean': control.setting('show_search') == 'true'
            }
            ,
            {
                'title': control.lang(30012),
                'action': 'playback_history',
                'icon': iconname('history'),
                'boolean': control.setting('show_history') == 'true'
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
                'action': 'settings',
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

            if item['action'] == 'live_tv' and control.setting('live_tv_mode') == '1':
                item.update({'isFolder': 'False', 'isPlayable': 'False'})

            refresh = {'title': 30054, 'query': {'action': 'refresh'}}
            cache_clear = {'title': 30056, 'query': {'action': 'cache_clear'}}
            reset_idx = {'title': 30134, 'query': {'action': 'reset_idx', 'query': 'force'}}
            settings = {'title': 30011, 'query': {'action': 'openSettings'}}
            go_to_audio = {'title': 30321, 'query': {'action': 'activate_other_addon', 'url': 'plugin.video.AliveGR', 'query': 'audio'}}
            tools = {'title': 30137, 'query': {'action': 'tools_menu'}}
            ii_cm = {'title': 30255, 'query': {'action': 'call_info'}}
            item.update({'cm': [ii_cm, refresh, cache_clear, reset_idx, settings, go_to_audio, tools]})

        if control.setting('reset_idx') == 'true':
            reset(notify=False)

        directory.add(self.menu)

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

        directory.add(self.list)

    def playback_history(self):

        lines = read_from_file(PLAYBACK_HISTORY)

        if not lines:

            self.list = [{'title': 30110, 'action':  None, 'icon': iconname('empty')}]
            directory.add(self.list)

        else:

            self.list = [json.loads(line) for line in lines]

            for i in self.list:
                bookmark = dict((k, v) for k, v in iteritems(i) if not k == 'next')
                bookmark['bookmark'] = i['url']
                bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
                remove_from_history_cm = {'title': 30485, 'query': {'action': 'delete_from_history', 'query': json.dumps(i)}}
                clear_history_cm = {'title': 30471, 'query': {'action': 'clear_playback_history'}}
                i.update({'cm': [bookmark_cm, remove_from_history_cm, clear_history_cm]})

            directory.add(self.list)

    def generic(self, query, content='videos'):

        self.list = json.loads(query)

        directory.add(self.list, content=content)
