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
import re, json
from streamlink.plugin.api.utils import itertags


def ant1gr(link):

    """ALternative method"""

    html = client.request(link)

    param = re.search(r'\$.getJSON\(\'(?P<param>.+?)\?', html).group('param')
    get_json = 'http://www.antenna.gr' + param
    cookie = client.request(get_json, output='cookie', close=False, referer=link)
    result = client.request(get_json, cookie=cookie, referer=link)
    url = json.loads(result)['url']

    if url.endswith('.mp4'):
        return
    else:
        return url


def ant1cy(link):

    """Alternative method"""

    api_url = 'https://www.ant1.com.cy/ajax.aspx?m=Atcom.Sites.Ant1iwo.Modules.TokenGenerator&videoURL={0}'

    html = client.request(link)

    m3u8 = re.findall("'(.+?)'", list(itertags(html.text, 'script'))[-2].text)[1]

    stream = client.request(api_url.format(m3u8))

    return stream + spoofer()


def omegacy(link):

    """ALternative method"""

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

    html = client.request(url)

    iframe = client.parseDOM(html, 'iframe', ret='src')[0]

    html = client.request(iframe)

    if '.m3u8' in html:
        stream = re.findall(r'http.+?\.m3u8', html)[0]
    else:
        stream = client.parseDOM(html, 'iframe', ret='src')[-1]

    return stream


def skai(url):

    json_object = json.loads(client.request(url))

    stream = json_object['now']['livestream']

    return stream


def stargr(url):

    """Alternative method"""

    html = client.request(url)

    script = client.parseDOM(html, 'script')[5]

    return re.search(r"'(?P<url>.+?\.m3u8)'", script).group('url')


def alphatv(url):

    link = client.request(url)
    link = re.findall(r'(?:\"|\')(http(?:s|)://.+?\.m3u8(?:.*?|))(?:\"|\')', link)[0]

    return link + spoofer()


def euronews(url):

    """ Alternative method"""

    result = client.request(url)
    result = json.loads(result)['url']

    if result.startswith('//'):
        result = 'http:' + result

    result = client.request(result)
    primary = json.loads(result)['primary']

    if primary.startswith('//'):
        primary = 'http:' + primary

    return primary


def periscope_search(url):

    html = client.request(url)

    container = client.parseDOM(html, 'div', attrs={'id': 'page-container'}, ret='data-store')[0]

    search = re.search(r'https?://www\.pscp\.tv/w/(\w+)', container)

    link = search.group()

    return link


def kineskop(url):

    """Deprecated method"""

    html = client.request(url)

    stream = re.search(r"getURLParam\('src','(.+?)'", html).group(1)

    headers = {'User-Agent': cache.get(randomagent, 12), 'Origin': 'http://kineskop.tv', 'Referer': url}

    output = stream + spoofer(headers=headers)

    return output
