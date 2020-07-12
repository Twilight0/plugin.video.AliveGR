# -*- coding: utf-8 -*-

"""
    AliveGR Add-on
    Author: Twilight0

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from tulip import client
import re
from random import choice
from tulip.parsers import itertags_wrapper


def risegr(link):

    html = client.request(link)

    vimeo_id = re.search(r'data-vimeoid="(\d+)"', html).group(1)

    vimeo_url = 'https://player.vimeo.com/video/' + vimeo_id

    return vimeo_url


def periscope_search(url):

    html = client.request(url)

    container = client.parseDOM(html, 'div', attrs={'id': 'page-container'}, ret='data-store')[0]

    search = re.search(r'https?://www\.pscp\.tv/w/(\w+)', container)

    link = search.group()

    return link


def iptv(name):

    html = client.request('https://www.dailyiptvlist.com/european-m3u-iptv/greece-greek/')

    latest = itertags_wrapper(html, 'a', {'title': 'Greece iptv m3u autoupdate links \d{2}.+'}, 'href')[0]

    nested = client.request(latest)

    playlists = itertags_wrapper(nested, 'a', {'href': '.+dailyiptvlist.com.+\.m3u'}, 'href')

    m3u = '\n'.join([client.request(i) for i in playlists])

    links = re.findall(r',(.+)$\r?\n(.+)', m3u, re.MULTILINE)

    try:
        urls = [i for i in links if name.lower() in i[0].lower().decode('utf-8')]
    except Exception:
        urls = [i for i in links if name.lower() in i[0].lower()]

    url = choice(urls)[1][:-1]

    return url
