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

from tulip.compat import quote
from tulip import directory, control, cleantitle
from tulip.init import sysaddon
from . import gm
from . import live


class Indexer:

    def __init__(self):

        self.list = [] ; self.data = []

    def wrapper(self, str_input, category):

        post = 'searchcategory={0}&searchtext={1}'.format(category, quote(str_input.encode('utf-8')))

        if category == 'person':
            self.list = gm.Indexer().persons_index(gm.SEARCH, post=post)
        else:
            self.list = gm.Indexer().listing(gm.SEARCH, post=post, get_listing=True)

        return self.list

    def search(self):

        choices = [
            control.lang(30096), control.lang(30031), control.lang(30030), control.lang(30063), control.lang(30068), control.lang(30097),
            control.lang(30101)  #, control.lang(30125)
        ]

        choice = control.selectDialog(heading=control.lang(30095), list=choices)

        if choice == 0:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30096)
            )

            if not str_input:
                return

            self.list = live.Indexer().live_tv(zapping=False, query=str_input.lower())

            directory.add(self.list)

        elif choice == 1:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30031)
            )

            try:
                str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                str_input = cleantitle.strip_accents(str_input)

            if not str_input:
                return

            self.list = self.wrapper(str_input, 'movies')

            directory.add(self.list, content='movies')

        elif choice == 2:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30030)
            )

            if not str_input:

                return

            try:
                str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                str_input = cleantitle.strip_accents(str_input)

            self.list = self.wrapper(str_input, 'series')

            directory.add(self.list, content='tvshows')

        elif choice == 3:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30063)
            )

            if not str_input:

                return

            try:
                str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                str_input = cleantitle.strip_accents(str_input)

            self.list = self.wrapper(str_input, 'shows')

            directory.add(self.list, content='tvshows')

        elif choice == 4:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30068)
            )

            if not str_input:

                return

            try:
                str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                str_input = cleantitle.strip_accents(str_input)

            self.list = self.wrapper(str_input, 'theater')

            directory.add(self.list, content='tvshows')

        elif choice == 5:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30097)
            )

            if not str_input:

                return

            try:
                str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                str_input = cleantitle.strip_accents(str_input)

            self.list = self.wrapper(str_input, 'animation')

            directory.add(self.list, content='tvshows')

        elif choice == 6:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30101)
            )

            if not str_input:

                return

            try:
                str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                str_input = cleantitle.strip_accents(str_input)

            self.list = self.wrapper(str_input, 'person')

            directory.add(self.list)

        # Will implement later
        # elif choice == 7:
        #
        #     str_input = control.dialog.input(
        #         heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30125)
        #     )
        #
        #     if not str_input:
        #
        #         return
        #
        #     try:
        #         str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
        #     except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
        #         str_input = cleantitle.strip_accents(str_input)
        #
        #     self.list = cache.get(self.wrapper, 12, str_input, 'music')
        #
        #     directory.add(self.list, content='tvshows', )

        else:

            control.execute('ActivateWindow(videos,"{0}")'.format(sysaddon))
