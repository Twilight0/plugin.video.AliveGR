# -*- coding: utf-8 -*-

# AliveGR Addon
# Author Twilight0
# SPDX-License-Identifier: GPL-3.0-only
# See LICENSES/GPL-3.0-only for more information.
from __future__ import absolute_import, unicode_literals

import json

from tulip.cleantitle import strip_accents
from tulip.compat import iteritems
from tulip.control import setting
from tulip import bookmarks, directory
from tulip.log import log_debug
from ..modules.themes import iconname


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

            self.list = sorted(self.data, key=lambda k: strip_accents(k['title'].lower()))

            if setting('show_clear_bookmarks') == 'true':

                clear_all = {
                    'title': 30274,
                    'action': 'clear_bookmarks',
                    'icon': iconname('empty')
                }

                self.list.insert(0, clear_all)

            directory.add(self.list)
