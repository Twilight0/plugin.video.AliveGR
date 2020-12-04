# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from ..modules.constants import YT_URL, CACHE_DEBUG
import re, youtube_resolver
from tulip import control, client, cache
from ..modules.utils import stream_picker


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

        if CACHE_DEBUG:
            url = generic(url)
        else:
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
