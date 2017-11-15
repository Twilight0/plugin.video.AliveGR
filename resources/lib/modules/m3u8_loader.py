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

from tulip import control, client, cache
import m3u8
from helpers import stream_picker
from urlparse import urljoin


def m3u8_picker(url):

    m3u8_playlists = m3u8.load(
        url.partition('|')[0], headers={'User-Agent': cache.get(client.randomagent, 12)}
    ).playlists

    if not m3u8_playlists:
        return url

    qualities = []
    urls = []

    for playlist in m3u8_playlists:

        quality = repr(playlist.stream_info.resolution).strip('()').replace(', ', 'x')
        if quality == 'None':
            quality = 'Auto'
        uri = playlist.uri
        if not uri.startswith('http'):
            uri = urljoin(playlist.base_uri, uri)
        qualities.append(quality)
        urls.append(uri)

    if len(qualities) == 1:
        control.infoDialog(control.lang(30220).format(qualities[0]))
        return url

    return stream_picker(qualities, urls)
