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
from __future__ import absolute_import, unicode_literals

import json

from tulip.compat import iteritems
from tulip import bookmarks, directory
from tulip.log import log_debug
from ..modules.themes import iconname
from .gm import MOVIES, THEATER, SHORTFILMS, GM_BASE


def directory_boolean(url):

    return MOVIES in url or SHORTFILMS in url or THEATER in url or ('episode' in url and GM_BASE in url)


class Indexer:

    def __init__(self):

        self.list = [] ; self.data = []

    def bookmarks(self):

        self.data = bookmarks.get()

        if not self.data:

            log_debug('Bookmarks list is empty')
            na = [{'title': 30033, 'action':  None, 'icon': iconname('empty')}]
            directory.add(na)

        else:

            for i in self.data:

                item = dict((k, v) for k, v in iteritems(i) if not k == 'next')
                item['delbookmark'] = i['url']
                i.update({'cm': [{'title': 30081, 'query': {'action': 'deleteBookmark', 'url': json.dumps(item)}}]})

                if control.setting('action_type') == '1' and directory_boolean(i['url']):
                    item.update({'isPlayable': 'False'})

            self.list = sorted(self.data, key=lambda k: k['title'].lower())

            directory.add(self.list)
