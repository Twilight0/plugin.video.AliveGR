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

from tulip import control
from tulip import m3u8
from helpers import stream_picker
from tulip.compat import urljoin, parse_qsl


def m3u8_picker(url):

    try:

        if '|' not in url:
            raise TypeError

        headers = dict(parse_qsl(url.rpartition('|')[2]))
        streams = m3u8.load(url.rpartition('|')[0], headers=headers).playlists

    except TypeError:

        streams = m3u8.load(url).playlists

    if not streams:
        return url

    qualities = []
    urls = []

    for stream in streams:

        quality = repr(stream.stream_info.resolution).strip('()').replace(', ', 'x')

        if quality == 'None':
            quality = 'Auto'

        uri = stream.uri

        if not uri.startswith('http'):
            uri = urljoin(stream.base_uri, uri)

        qualities.append(quality)

        try:

            if '|' not in url:
                raise TypeError

            urls.append(uri + ''.join(url.rpartition('|')[1:]))

        except TypeError:
            urls.append(uri)

    if len(qualities) == 1:

        control.infoDialog(control.lang(30220).format(qualities[0]))

        return url

    return stream_picker(qualities, urls)
