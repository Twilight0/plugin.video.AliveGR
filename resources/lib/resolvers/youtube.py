# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

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

from ..modules.constants import YT_URL
import re, youtube_resolver
from tulip import control, client, cache
from ..modules.helpers import stream_picker


def generic(url, add_base=False):

    html = client.request(url)

    try:
        video_id = re.search(r'videoId.+?([\w-]{11})', html).group(1)
    except AttributeError:
        return

    if not add_base:

        return video_id

    else:

        stream = YT_URL + video_id
        return stream


def wrapper(url):

    if url.endswith('/live'):

        url = cache.get(generic, 6, url)

        if not url:

            return

    streams = youtube_resolver.resolve(url)

    try:
        addon_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        addon_enabled = False

    if not addon_enabled:

        streams = [s for s in streams if 'dash' not in s['title'].lower()]

    if control.condVisibility('Window.IsVisible(music)') and control.setting('audio_only') == 'true':

        audio_choices = [u for u in streams if 'dash/audio' in u and 'dash/video' not in u]

        if control.setting('yt_quality_picker') == '0':
            resolved = audio_choices[0]['url']
        else:
            qualities = [i['title'] for i in audio_choices]
            urls = [i['url'] for i in audio_choices]

            resolved = stream_picker(qualities, urls)

        return resolved

    elif control.setting('yt_quality_picker') == '1':

        qualities = [i['title'] for i in streams]
        urls = [i['url'] for i in streams]

        resolved = stream_picker(qualities, urls)

        return resolved

    else:

        resolved = streams[0]['url']

        return resolved
