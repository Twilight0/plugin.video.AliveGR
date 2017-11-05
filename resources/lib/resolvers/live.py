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
import re, urllib


def ant1cy(url):

    referer = 'http://www.ant1iwo.com/webtv/web-tv-live/'

    cookie = client.request(url, output='cookie', close=False)
    result = client.request(url, cookie=cookie, referer=referer)

    return result.strip() + client.spoofer() + '&Referer=' + urllib.quote_plus(referer)


def megacy(url):

    cookie = client.request(url, output='cookie', close=False)
    result = client.request(url, cookie=cookie)

    stream = re.findall('\[\{sources:\[\{file: "(.*?)"', result)[0]

    return stream.strip() + client.spoofer()


def megagr(url):

    html = client.request(url)

    try:

        stream = client.parseDOM(html, 'iframe', ret='src')[0]

        return stream

    except:

        from ..resolvers.yt_wrapper import base_link

        pattern = re.compile('"https?://(?:www\.youtube\.com|youtu\.be)/(?:watch\?v=|embed/|)([\w-]*?)"')

        yt_id = re.findall(pattern, html)[0]

        return base_link + yt_id


def ert(url):

    code = client.request('http://whatismyipaddress.com/')

    if 'Greece' in code:
        GR = True
    else:
        GR = False

    html = client.request(url)

    if GR:
        result = client.parseDOM(html, 'iframe', ret='src')[-1]
    else:
        result = client.parseDOM(html, 'iframe', ret='src')[0]

    return result


def skai(url):

    from ..resolvers.yt_wrapper import base_link

    xml = client.request(url)

    result = re.findall('<File><!\[CDATA\[(.*?)\]\]></File>', xml)[0]

    return base_link + result


def alphatv(url):

    link = client.request(url)
    link = re.findall('(?:\"|\')(http(?:s|)://.+?\.m3u8(?:.*?|))(?:\"|\')', link)[-1]
    link = client.request(link, output='geturl') + client.spoofer()

    return link


def euronews(url):

    import json

    result = client.request(url)
    result = json.loads(result)['url']

    result = client.request(result)
    primary = json.loads(result)['primary']

    return primary


def fnetwork(url):

    html = client.request(url)
    link = client.parseDOM(html, 'iframe', ret='src')[0]

    return link


def ssh101(url):

    html = client.request(url)
    stream = client.parseDOM(html, 'source', attrs={'type': 'application/x-mpegurl'}, ret='src')[0]

    return stream


def visioniptv():

    UA = {'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36'
                        ' (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'}

    url = 'http://tvnetwork.new.visionip.tv/Hellenic_TV'

    cookie = client.request(url, output='cookie', headers=UA)

    return '?' + cookie
