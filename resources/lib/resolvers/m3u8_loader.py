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

import m3u8
from ..modules.helpers import stream_picker
from urlparse import urljoin


def m3u8_picker(url):

    m3u8_playlists = m3u8.load(url).playlists

    if not m3u8_playlists:
        return url

    qualities = []
    uris = []

    for playlist in m3u8_playlists:

        quality = repr(playlist.stream_info[3]).strip('()').replace(', ', 'x')
        if quality == 'None':
            quality = 'Auto'
        uri = playlist.uri
        if not uri.startswith('http'):
            uri = urljoin(playlist.base_uri, uri)
        qualities.append(quality)
        uris.append(uri)

    return stream_picker(qualities, uris)