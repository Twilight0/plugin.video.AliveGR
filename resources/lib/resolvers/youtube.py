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
from tulip import control
from resources.lib.modules.helpers import stream_picker, addon_version
from resources.lib.modules.constants import yt_prefix

replace_url = control.setting('yt_resolve') == '1'


def wrapper(url):

    if replace_url:

        url = re.sub(
            r'''https?://(?:[0-9A-Z-]+\.)?(?:(youtu\.be|youtube(?:-nocookie)?\.com)/?\S*?[^\w\s-])([\w-]{11})(?=[^\w-]|$)(?![?=&+%\w.-]*(?:['"][^<>]*>|</a>))[?=&+%\w.-]*''',
            yt_prefix + r'\2', url, flags=re.I
        )

        return url

    streams = youtube_resolver.resolve(url)

    try:
        addon_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        addon_enabled = False

    yt_mpd_enabled = control.addon(id='plugin.video.youtube').getSetting('kodion.video.quality.mpd') == 'true'

    if addon_version('xbmc.python') >= 2250 and addon_enabled and yt_mpd_enabled:
        choices = streams
    else:
        choices = [s for s in streams if s['container'] != 'mpd']

    if control.condVisibility('Window.IsVisible(music)') and control.setting('audio_only') == 'true':

        audio_choices = [u for u in choices if 'dash/audio' in u and 'dash/video' not in u]

        if control.setting('yt_quality_picker') == '0':
            resolved = audio_choices[0]['url']
        else:
            qualities = [i['title'] for i in audio_choices]
            urls = [i['url'] for i in audio_choices]

            resolved = stream_picker(qualities, urls)

        return resolved

    elif control.setting('yt_quality_picker') == '1':

        qualities = [i['title'] for i in choices]
        urls = [i['url'] for i in choices]

        resolved = stream_picker(qualities, urls)

        return resolved

    else:

        resolved = choices[0]['url']

        return resolved
