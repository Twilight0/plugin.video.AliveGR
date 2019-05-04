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

from resources.lib.modules.constants import yt_url
import re, youtube_resolver
from tulip import control, client
from resources.lib.modules.helpers import stream_picker
from resources.lib.modules.constants import yt_prefix

replace_url = control.setting('yt_resolve') == '1'


def generic(url, add_base=False):

    html = client.request(url)

    if '<iframe' in html:

        iframes = client.parseDOM(html, 'iframe', ret='src')
        stream = [s for s in iframes if 'youtu' in s][0]

        return stream

    else:

        video_id = re.findall(r"videoId.+?['\"]([\w-]{11})['\"]", html)[0]

        if not add_base:

            return video_id

        else:

            stream = yt_url + video_id
            return stream


def wrapper(url):

    if replace_url:

        result = re.sub(
            r'''https?://(?:[0-9A-Z-]+\.)?(?:(youtu\.be|youtube(?:-nocookie)?\.com)/?\S*?[^\w\s-])([\w-]{11})(?=[^\w-]|$)(?![?=&+%\w.-]*(?:['"][^<>]*>|</a>))[?=&+%\w.-]*''',
            yt_prefix + r'\2', url, flags=re.I
        )

        if url != result:

            return result

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
