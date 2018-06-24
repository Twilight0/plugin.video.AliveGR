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

import re, youtube_resolver
from tulip import client, control
from ..modules.helpers import stream_picker, addon_version


yt_prefix = 'plugin://plugin.video.youtube/play/?video_id='
base_link = 'https://www.youtube.com/watch?v='


def traslate(url, add_base=False):

    """Translate /user & /channel youtube urls into video ids"""

    html = client.request(url)

    video_id = re.findall('videoId.+?"([\w-]{11})', html)[0]

    if not add_base:

        return video_id

    else:

        stream = base_link + video_id
        return stream


def wrapper(url):

    if '#audio_only' in url:

        no_fragment = url.replace('#audio_only', '')
        streams = youtube_resolver.resolve(no_fragment)

    else:

        streams = youtube_resolver.resolve(url)

    try:
        enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        enabled = False

    if addon_version('xbmc.python') > 225 and enabled:
        choices = streams
    else:
        choices = [s for s in streams if 'dash' not in repr(s)]

    if '#audio_only' in url and control.setting('audio_only') == 'true' or control.condVisibility('Window.IsActive(music)') == 1:

        resolved = choices[-5]['url']
        return resolved, False

    elif control.setting('yt_quality_picker') == '1':

        qualities = [i['title'] for i in choices]
        urls = [i['url'] for i in choices]

        resolved = stream_picker(qualities, urls)

        if 'dash' in resolved:
            return resolved, True
        else:
            return resolved, False

    else:

        resolved = choices[0]['url']

        if addon_version('xbmc.python') > 225 and enabled:

            return resolved, True

        else:

            return resolved, False


