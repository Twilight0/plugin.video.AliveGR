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
import re, urlparse, json


def ant1gr(url):

    html = client.request(url)

    param = re.findall('\$.getJSON\(\'(.+?)\?', html)[0]
    get_json = urlparse.urlsplit(url).geturl() + param
    output = client.request(get_json)
    link = json.loads(output)['url']

    return link


def ant1cy(url):

    token = 'http://www.ant1iwo.com/ajax.aspx?m=Atcom.Sites.Ant1iwo.Modules.TokenGenerator&videoURL='

    if '#' in url:
        referer = url.partition('#')[0]
    else:
        referer = url

    cookie = client.request(url, output='cookie', close=False, referer=referer)
    result = client.request(url, cookie=cookie, referer=referer)

    video = client.parseDOM(result, 'a', attrs={'class': 'playVideo'}, ret='data-video')[0]
    video = client.replaceHTMLCodes(video).strip('[]"')

    if not video:
        video = re.findall('\'(http.+?\.m3u8)\'', result)[0]
    if not video:
        video = 'http://l2.cloudskep.com/antl2/abr/playlist.m3u8'

    link = token + video

    generated = client.request(link)

    return generated.strip() + client.spoofer(referer=True, ref_str=referer)


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

        from ..modules.constants import yt_base

        pattern = re.compile('"https?://(?:www\.youtube\.com|youtu\.be)/(?:watch\?v=|embed/|)([\w-]*?)"')

        yt_id = re.findall(pattern, html)[0]

        return yt_base + yt_id


def ert(url):

    from ..modules.helpers import geo_loc

    html = client.request(url)

    if 'Greece' in geo_loc():
        result = client.parseDOM(html, 'iframe', ret='src')[-1]
    else:
        result = client.parseDOM(html, 'iframe', ret='src')[0]

    return result


def skai(url):

    # Keeping xml url for reference
    # http://www.skai.gr/ajax.aspx?m=NewModules.LookupMultimedia&amp;mmid=/Root/TVLive

    html = client.request(url)

    vid = client.parseDOM(html, 'span', attrs={'itemprop': 'contentUrl'}, ret='href')[0]

    return vid


def alphatv(url):

    link = client.request(url)
    link = re.findall('(?:\"|\')(http(?:s|)://.+?\.m3u8(?:.*?|))(?:\"|\')', link)[-1]
    link = client.request(link, output='geturl') + client.spoofer()

    return link


def euronews(url):

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


def ellinikosfm(url):

    html = client.request(url)

    iframe_url = 'http:' + client.parseDOM(html, 'iframe', ret='src')[0]
    services_url = iframe_url.replace('http://iframe.dacast.com', 'https://services.dacast.com/token/i')
    json_url = iframe_url.replace('iframe', 'json')

    json_token = client.request(services_url, output='response')[1]
    token = json.loads(json_token)['token']
    json_obj = client.request(json_url)
    hls_url = 'http:' + json.loads(json_obj)['hls'].replace('\\', '')

    return hls_url + token
