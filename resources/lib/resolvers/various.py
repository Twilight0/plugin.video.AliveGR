# -*- coding: utf-8 -*-

"""
    AliveGR Add-on
    Author: Thgiliwt

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


def risegr(link):

    html = client.request(link)

    vimeo_id = re.search(r'data-vimeoid="(\d+)"', html).group(1)

    vimeo_url = 'https://player.vimeo.com/video/' + vimeo_id

    return vimeo_url


def ert(url):

    html = client.request(url)
    html = client.parseDOM(html, 'div', attrs={'class': 'videoWrapper'})[-1]
    iframe = client.parseDOM(html, 'iframe', ret='src')[0]

    result = client.request(iframe)

    url = re.search(r'var (?:HLSLink|stream) = [\'"](.+?)[\'"]', result)

    if url:

        url = url.group(1)
        return url

    else:

        iframes = client.parseDOM(result, 'iframe', ret='src')

        return iframes


def skai(url):

    html = client.request(url)

    script = [i for i in client.parseDOM(html, 'script') if 'youtube.com' in i][0]

    vid = re.search(r'watch\?v=([\w-]{11})', script).group(1)

    return vid


def periscope_search(url):

    html = client.request(url)

    container = client.parseDOM(html, 'div', attrs={'id': 'page-container'}, ret='data-store')[0]

    search = re.search(r'https?://www\.pscp\.tv/w/(\w+)', container)

    link = search.group()

    return link
