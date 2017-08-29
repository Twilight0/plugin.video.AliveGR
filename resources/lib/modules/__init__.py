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

import sys, urlparse, xbmc

syshandle = int(sys.argv[1])
sysaddon = sys.argv[0]
params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

########################################################################################################################

action = params.get('action', None)
url = params.get('url')
content = params.get('content_type')
image = params.get('image')
title = params.get('title')
name = params.get('name')
query = params.get('query')
tvguide = params.get('tvguide')
plot = params.get('plot')
genre = params.get('genre')

########################################################################################################################

sleep = params.get('sleep')

if sleep is None:
    sleep = True
else:
    sleep = False

########################################################################################################################

fp = xbmc.getInfoLabel('Container.FolderPath')

if 'audio' in fp and action is None:
    action = 'radio'
