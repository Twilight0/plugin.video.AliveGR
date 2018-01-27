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

import json

from tulip import bookmarks, directory, control
from tulip.log import *
from ..modules.themes import iconname
from .gm import movies_link, theater_link, shortfilms_link


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

                if i['url'].startswith((movies_link, theater_link, shortfilms_link)):
                    if control.setting('action_type') == '1':
                        try:
                            del i['isFolder']
                        except:
                            pass
                        action = 'directory'
                    elif control.setting('action_type') == '2' and control.setting('auto_play') == 'false':
                        try:
                            del i['isFolder']
                        except:
                            pass
                        action = i['action']
                    else:
                        action = i['action']
                else:
                    action = i['action']

                i['action'] = action

                item = dict((k, v) for k, v in i.iteritems() if not k == 'next')
                item['delbookmark'] = i['url']
                i.update({'cm': [{'title': 30081, 'query': {'action': 'deleteBookmark', 'url': json.dumps(item)}}]})

            self.list = sorted(self.data, key=lambda k: k['title'].lower())

            directory.add(self.list)
