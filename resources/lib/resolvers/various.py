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
import re, json


def ant1gr(link):

    try:

        html = client.request(link)

        param = re.findall('\$.getJSON\(\'(.+?)\?', html)[0]
        get_json = 'http://www.antenna.gr' + param
        cookie = client.request(get_json, output='cookie', close=False, referer=link)
        result = client.request(get_json, cookie=cookie, referer=link)
        url = json.loads(result)['url']

        if url.endswith('.mp4'):
            raise BaseException
        else:
            return url

    except BaseException:

        pass

    # Carry on:

    get_live = 'http://mservices.antenna.gr/services/mobile/getLiveStream.ashx?'

    live_link_1 = 'http://antglantennatv-lh.akamaihd.net/i/live_1@421307/master.m3u8'
    live_link_2 = 'http://antglantennatv-lh.akamaihd.net/i/live_2@421307/master.m3u8'

    ###########

    try:

        json_obj = client.request(get_live)

        url = json.loads(json_obj.strip('();'))['data']['stream']

        if url.endswith('.mp4'):
            raise BaseException
        else:
            return url

    except (KeyError, ValueError, BaseException, TypeError):

        if client.request(live_link_1, output='response')[0] == '200':
            return live_link_1
        else:
            return live_link_2


def ant1cy(url):

    token = 'http://www.ant1iwo.com/ajax.aspx?m=Atcom.Sites.Ant1iwo.Modules.TokenGenerator&videoURL='
    failsafe_live_url = 'http://l2.cloudskep.com/antl2/abr/playlist.m3u8'

    if '#' in url:
        referer = url.partition('#')[0]
    else:
        referer = url

    cookie = client.request(url, output='cookie', close=False, referer=referer)
    result = client.request(url, cookie=cookie, referer=referer)

    video = client.parseDOM(result, 'a', attrs={'class': 'playVideo'}, ret='data-video')[0]
    video = client.replaceHTMLCodes(video).strip('[]"')

    if url == token + failsafe_live_url:
        video = url
    else:
        if not video:
            video = re.findall('\'(http.+?\.m3u8)\'', result)[0]
        if not video:
            video = failsafe_live_url

    link = token + video

    generated = client.request(link)

    return generated.strip() + client.spoofer(referer=True, ref_str=referer)


def megacy(url):

    cookie = client.request(url, output='cookie', close=False)
    result = client.request(url, cookie=cookie)

    stream = re.findall('\[{sources:\[{file: "(.*?)"', result)[0]

    return stream.strip() + client.spoofer()


def ert(url):

    from ..modules.helpers import geo_loc
    from ..modules.constants import yt_url

    html = client.request(url)

    if 'Greece' in geo_loc():
        result = client.parseDOM(html, 'iframe', ret='src')[-1]
    else:
        result = client.parseDOM(html, 'iframe', ret='src')[0]

    vid = result.rpartition('/')[2][:11]

    video = yt_url + vid

    return video


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


def dacast(url):

    html = client.request(url)

    if 'iframe.dacast' in html:
        combined_id = client.parseDOM(html, 'iframe', ret='src')[0].partition('/b/')[2]
    else:
        combined_id = client.parseDOM(html, 'script', attrs={'class': 'dacast-video'}, ret='id')[0].replace('_', '/')

    services_url = 'https://services.dacast.com/token/i/b/' + combined_id
    json_url = 'https://json.dacast.com/b/' + combined_id

    json_token = client.request(services_url, output='response')[1]

    token = json.loads(json_token)['token']
    json_obj = client.request(json_url)
    hls_url = 'http:' + json.loads(json_obj)['hls'].replace('\\', '')

    return hls_url + token
