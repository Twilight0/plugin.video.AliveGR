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

import json

from tulip import cache, directory, youtube
from ..modules.tools import api_keys
from ..modules.helpers import thgiliwt


base_link = 'https://www.youtube.com/watch?v='


def yt_playlists(pid):

    playlists = cache.get(youtube.youtube(key=thgiliwt(api_keys['api_key'])).playlists, 48, pid)

    if playlists is None:
        return

    for playlist in playlists:
        playlist.update({'action': 'youtube'})

    items = sorted(playlists, key=lambda k: k['title'].lower())

    for item in items:
        bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
        bookmark['bookmark'] = item['url']
        bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
        item.update({'cm': [bookmark_cm]})

    return items


def yt_videos(url):

    video_list = cache.get(youtube.youtube(key=thgiliwt(api_keys['api_key'])).playlist, 48, url)

    if video_list is None:
        return

    for v in video_list:
        v.update({'action': 'play', 'isFolder': 'False'})

    directory.add(video_list)