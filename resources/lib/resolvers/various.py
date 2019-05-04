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

from tulip.user_agents import randomagent, spoofer
from tulip import client, cache
from tulip.log import log_debug
import re, json
from streamlink.plugin.api.utils import itertags


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

    live_link_1 = 'https://antennalivesp-lh.akamaihd.net/i/live_1@715138/master.m3u8'
    live_link_2 = 'https://antennalivesp-lh.akamaihd.net/i/live_2@715138/master.m3u8'

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


def omegacy(link):

    """ ALternative method"""

    cookie = client.request(link, close=False, output='cookie')
    html = client.request(link, cookie=cookie)
    tags = list(itertags(html, 'script'))

    m3u8 = [i for i in tags if i.text.startswith(u'var playerInstance')][0].text

    stream = re.findall('"(.+?)"', m3u8)[1]

    return spoofer(url=stream, referer=True, ref_str=link)


def risegr(link):

    html = client.request(link)

    vimeo_id = re.search(r'data-vimeoid="(\d+)"', html).group(1)

    vimeo_url = 'https://player.vimeo.com/video/' + vimeo_id

    return vimeo_url


def ert(url):

    from resources.lib.modules.helpers import geo_loc
    from resources.lib.modules.constants import yt_url

    html = client.request(url)

    iframes = client.parseDOM(html, 'iframe', ret='src')

    try:
        if geo_loc() == 'Greece' and 'HLSLink' in html:
            raise IndexError
        elif geo_loc() != 'Greece':
            result = iframes[0]
        else:
            result = iframes[-1]
        if not result:
            raise IndexError
    except IndexError:
        result = client.parseDOM(html, 'script', attrs={'type': 'text/javascript'})[0]
        result = re.search(r'HLSLink = \'(.+?)\'', result).group(1)
        return result

    vid = result.rpartition('/')[2][:11]

    video = yt_url + vid

    return video


def skai(url):

    log_debug('Playing Skai TV channel: ' + url)

    # html = client.request(url)
    #
    # settings_url = re.search(r'url:"(.+?settings\.php)"', html)
    #
    # if settings_url:
    #
    #     live_json = client.request(settings_url.group(1))
    #
    #     youtu_id = json.loads(live_json)['live_url']
    #
    # else:

    xml_url = 'http://www.skai.gr/ajax.aspx?m=NewModules.LookupMultimedia&amp;mmid=/Root/TVLive'

    xml_file = client.request(xml_url)

    cdata = client.parseDOM(xml_file, 'File')[0]

    youtu_id = re.search(r'([\w-]{11})', cdata)

    youtu_id = youtu_id.group(1)

    return youtu_id


def alphatv(url):

    """ Deprecated method"""

    link = client.request(url)
    link = re.findall(r'(?:\"|\')(http(?:s|)://.+?\.m3u8(?:.*?|))(?:\"|\')', link)[-1]
    link = client.request(link, output='geturl') + spoofer()

    return link


def euronews(url):

    """ Deprecated method"""

    result = client.request(url)
    result = json.loads(result)['url']

    if result.startswith('//'):
        result = 'http:' + result

    result = client.request(result)
    primary = json.loads(result)['primary']

    if primary.startswith('//'):
        primary = 'http:' + primary

    return primary


def ssh101(url):

    """Deprecated method"""

    html = client.request(url)
    stream = client.parseDOM(html, 'source', attrs={'type': 'application/x-mpegurl'}, ret='src')[0]

    return stream


def periscope_search(url):

    html = client.request(url)

    container = client.parseDOM(html, 'div', attrs={'id': 'page-container'}, ret='data-store')[0]

    search = re.search('https?://www\.pscp\.tv/w/(\w+)', container)

    link = search.group()

    return link


def kineskop(url):

    """Deprecated method"""

    html = client.request(url)

    stream = re.search(r"getURLParam\('src','(.+?)'", html).group(1)

    headers = {'User-Agent': cache.get(randomagent, 12), 'Origin': 'http://kineskop.tv', 'Referer': url}

    output = stream + spoofer(headers=headers)

    return output
