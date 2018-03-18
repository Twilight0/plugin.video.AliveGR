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


from tulip import client, control


class Indexer:

    def __init__(self):

        self.list = [] ; self.data = []
        self.main_link = 'http://www.greekdocumentary.gr/'

    def root(self):

        self.list = [
            {
                'title': control.lang(30001),
                'action': 'live_tv',
                'icon': iconname('monitor'),
                'id': '30001'
            }
        ]
