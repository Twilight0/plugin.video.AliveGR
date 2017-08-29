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
from ..modules.themes import iconname


class Main:

    def __init__(self):

        self.list = [] ; self.data = []
    # TODO
    #     self.switch = {
    #         'title': control.lang(30040).format(control.lang(30005) if control.setting('bookmarks_group') == 'ALL' else control.setting('bookmarks_group')),
    #         'icon': control.addonmedia(addonid='script.AliveGR.artwork', theme=theme()[0], icon='switcher' + theme()[1]),
    #         'action': 'bookmarks_switcher'
    #     }
    #
    # def switcher(self):
    #
    #     self.list = [control.lang(30001), control.lang(30031), control.lang(30030), control.lang(30068), control.lang(30079)]
    #
    #     choice = control.selectDialog(heading=control.lang(30049), list=[])
    #
    #     if choice == 0:
    #         pass
    #     else:
    #         control.execute('Dialog.Close(all)')

    def bookmarks(self):

        self.data = bookmarks.get()

        if not self.data:

            na = [{'title': 30033, 'action':  None, 'icon': iconname('empty')}]
            directory.add(na)

        else:

            for item in self.data:
                bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
                bookmark['delbookmark'] = item['url']
                item.update({'cm': [{'title': 30081, 'query': {'action': 'deleteBookmark', 'url': json.dumps(bookmark)}}]})

            self.list = sorted(self.data, key=lambda k: k['title'].lower())

            directory.add(self.list)
