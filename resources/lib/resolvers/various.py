# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from tulip import client
import re
from random import choice
from tulip.parsers import itertags_wrapper
from tulip.compat import urlparse
from tulip.control import lang


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

    hosts = [''.join([lang(30015), urlparse(u[1][:-1]).hostname]) for u in urls]

    urls = [u[1][:-1] for u in urls]

    return hosts, urls
