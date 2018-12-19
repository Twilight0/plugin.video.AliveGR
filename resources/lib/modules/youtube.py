# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Thgiliwt

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

import re
from resources.lib.modules.constants import yt_url
from tulip import client


def thumb_maker(video_id, hq=False):

    if hq:
        return 'http://img.youtube.com/vi/' + video_id + '/maxresdefault.jpg'
    else:
        return 'http://img.youtube.com/vi/' + video_id + '/mqdefault.jpg'


def traslate(url, add_base=False):

    html = client.request(url)

    if 'iframe' in html:

        iframes = client.parseDOM(html, 'iframe', ret='src')
        stream = [s for s in iframes if 'youtu' in s][0]

        return stream

    else:

        video_id = re.findall('videoId.+?"([\w-]{11})', html)[0]

        if not add_base:

            return video_id

        else:

            stream = yt_url + video_id
            return stream
