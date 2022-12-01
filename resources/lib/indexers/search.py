# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''
from __future__ import absolute_import, unicode_literals

import json

from tulip.compat import quote, quote_plus, py2_uni
from tulip import directory, control, cleantitle
from . import gm
from . import live
from ..modules.themes import iconname
from ..modules.utils import add_to_file, read_from_file
from ..modules.constants import QUERY_MAP, SEARCH_HISTORY


class Indexer:

    def __init__(self):

        self.list = []; self.data = []

    def wrapper(self, str_input, category):

        post = 'searchcategory={0}&searchtext={1}'.format(category, quote(str_input.encode('utf-8')))

        if category == 'person':
            self.list = gm.Indexer().persons_index(gm.SEARCH, post=post)
        else:
            self.list = gm.Indexer().listing(gm.SEARCH, post=post, get_listing=True)

        return self.list

    def search_index(self):

        add_to_search_history_cm = {'title': 30486, 'query': {'action': 'add_to_search_history'}}
        refresh_cm = {'title': 30054, 'query': {'action': 'refresh'}}

        self.list = [
            {
                'title': control.lang(30016),
                'action': 'search',
                'icon': iconname('search'),
                'isFolder': 'False', 'isPlayable': 'False',
                'cm': [add_to_search_history_cm, refresh_cm]
            }
        ]

        history = read_from_file(SEARCH_HISTORY)

        if history:

            search_history = [
                {
                    'title': i.split(',')[1] + ' (' + control.lang(QUERY_MAP.get(i.split(',')[0])) + ')',
                    'action': 'search', 'query': i,
                    'cm': [
                        add_to_search_history_cm,
                        {'title': 30485, 'query': {'action': 'delete_from_history', 'query': i}},
                        {'title': 30494, 'query': {'action': 'change_search_term', 'query': i}},
                        refresh_cm
                    ]
                } for i in history
            ]

            for i in search_history:
                if i['query'].split(',')[0] == 'Live TV Channel':
                    i.update({'image': iconname('monitor')})
                elif i['query'].split(',')[0] == 'TV Serie':
                    i.update({'image': iconname('series')})
                elif i['query'].split(',')[0] == 'TV Show':
                    i.update({'image': iconname('shows')})
                elif i['query'].split(',')[0] == 'Movie':
                    i.update({'image': iconname('movies')})
                elif i['query'].split(',')[0] == 'Theater':
                    i.update({'image': iconname('theater')})
                elif i['query'].split(',')[0] == 'Cartoon':
                    i.update({'image': iconname('kids')})
                elif i['query'].split(',')[0] == 'Person':
                    i.update({'image': iconname('user')})

            self.list.extend(search_history)

        directory.add(self.list)

    def search(self, action, query=None):

        if query is not None:
            choice = list(QUERY_MAP.keys()).index(query.split(',')[0])
            str_input = query.split(',')[1]
        else:
            choice = None
            str_input = None

        if choice is None:

            choices = [
                control.lang(30096), control.lang(30031), control.lang(30030), control.lang(30063), control.lang(30068),
                control.lang(30097), control.lang(30101)
            ]

            choice = control.selectDialog(heading=control.lang(30095), list=choices)

        if choice == 0:

            if str_input is None:

                str_input = control.dialog.input(
                    heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30096)
                )

                str_input = py2_uni(str_input)

                if not str_input:
                    return

            add_to_file(SEARCH_HISTORY, u"Live TV Channel,{0}".format(str_input))

            if action == 'add_to_search_history':
                control.refresh()
                return

            self.list = live.Indexer().live_tv(zapping=False, query=str_input.lower())

            if query:
                directory.add(self.list)
            else:
                directory.run_builtin(action='generic_index', query=quote_plus(json.dumps(self.list)))

        elif choice == 1:

            if str_input is None:

                str_input = control.dialog.input(
                    heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30031)
                )

                str_input = cleantitle.strip_accents(py2_uni(str_input))

            if not str_input:
                return

            add_to_file(SEARCH_HISTORY, u"Movie,{0}".format(str_input))

            if action == 'add_to_search_history':
                control.refresh()
                return

            self.list = self.wrapper(str_input, 'movies')

            if query:
                directory.add(self.list, content='movies')
            else:
                directory.run_builtin(action='generic_index', query=quote_plus(json.dumps(self.list)))

        elif choice == 2:

            if str_input is None:

                str_input = control.dialog.input(
                    heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30030)
                )

                if not str_input:

                    return

                str_input = cleantitle.strip_accents(py2_uni(str_input))

            add_to_file(SEARCH_HISTORY, u"TV Serie,{0}".format(str_input))

            if action == 'add_to_search_history':
                control.refresh()
                return

            self.list = self.wrapper(str_input, 'series')

            if query is not None:
                directory.add(self.list, content='tvshows')
            else:
                directory.run_builtin(action='generic_index', query=quote_plus(json.dumps(self.list)))

        elif choice == 3:

            if not str_input:

                str_input = control.dialog.input(
                    heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30063)
                )

                if not str_input:

                    return

                str_input = cleantitle.strip_accents(py2_uni(str_input))

            add_to_file(SEARCH_HISTORY, u"TV Show,{0}".format(str_input))

            if action == 'add_to_search_history':
                control.refresh()
                return

            self.list = self.wrapper(str_input, 'shows')

            if query is not None:
                directory.add(self.list, content='tvshows')
            else:
                directory.run_builtin(action='generic_index', query=quote_plus(json.dumps(self.list)))

        elif choice == 4:

            if str_input is None:

                str_input = control.dialog.input(
                    heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30068)
                )

                if not str_input:

                    return

                try:
                    str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
                except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                    str_input = cleantitle.strip_accents(str_input)

            add_to_file(SEARCH_HISTORY, u"Theater,{0}".format(str_input))

            if action == 'add_to_search_history':
                control.refresh()
                return

            self.list = self.wrapper(str_input, 'theater')

            if query is not None:
                directory.add(self.list, content='movies')
            else:
                directory.run_builtin(action='generic_index', query=quote_plus(json.dumps(self.list)))

        elif choice == 5:

            if str_input is None:
                str_input = control.dialog.input(
                    heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30097)
                )

                if not str_input:

                    return

                str_input = cleantitle.strip_accents(py2_uni(str_input))

            add_to_file(SEARCH_HISTORY, u"Cartoon,{0}".format(str_input))

            if action == 'add_to_search_history':
                control.refresh()
                return

            self.list = self.wrapper(str_input, 'animation')

            if query is not None:
                directory.add(self.list, content='tvshows')
            else:
                directory.run_builtin(action='generic_index', query=quote_plus(json.dumps(self.list)))

        elif choice == 6:

            if str_input is None:

                str_input = control.dialog.input(
                    heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30101)
                )

                if not str_input:

                    return

                str_input = cleantitle.strip_accents(py2_uni(str_input))

            add_to_file(SEARCH_HISTORY, u"Person,{0}".format(str_input))

            if action == 'add_to_search_history':
                control.refresh()
                return

            self.list = self.wrapper(str_input, 'person')

            if query is not None:
                directory.add(self.list)
            else:
                directory.run_builtin(action='generic_index', query=quote_plus(json.dumps(self.list)))

        else:

            control.close_all()
