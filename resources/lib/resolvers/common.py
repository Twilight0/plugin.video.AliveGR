# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import

from tulip import client
import re
from tulip.parsers import itertags_wrapper
from tulip.compat import urlparse
from tulip.control import lang
from tulip.log import log_debug
from ..modules.constants import cache_function, cache_duration


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


@cache_function(cache_duration(120))
def iptv(name):

    html = client.request('https://www.dailyiptvlist.com/iptv-europe-free-m-3-u/greece-greek/')

    latest = itertags_wrapper(html, 'a', {'class': 'image-link'}, 'href')[0]

    nested = client.request(latest)

    playlists = itertags_wrapper(nested, 'a', {'href': '.+dailyiptvlist.com.+\.m3u'}, 'href')

    m3u = '\n'.join([client.request(i) for i in playlists])

    links = re.findall(r',(.+)$\r?\n(.+)', m3u, re.MULTILINE)

    try:
        result = [i for i in links if name.lower() in i[0].lower().decode('utf-8')]
    except Exception:
        result = [i for i in links if name.lower() in i[0].lower()]

    urls = [u[1][:-1] for u in result if _check_url(u[1][:-1])]

    if not urls:
        log_debug('Did not find alternative links')
        return

    hosts = [''.join([lang(30015), urlparse(url).hostname]) for url in urls]

    return hosts, urls


@cache_function(cache_duration(60))
def _check_url(url):

    try:
        ok = client.request(url, output='response', timeout=10)[0] == u'200'
    except Exception:
        ok = False

    return ok
