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

import re
import streamlink.session
from tulip import control

openload_regex = r'https?://(?P<domain>o(?:pen)?load\.(?:io|co|tv|stream|win|download|info|icu|fun|pw))/(?:embed|f)/(?P<streamid>[\w-]+)'


def sl_session(url):

    custom_plugins = control.join(control.addonPath, 'resources', 'lib', 'resolvers', 'sl_plugins')

    session = streamlink.session.Streamlink()
    session.load_plugins(custom_plugins)

    plugin = session.resolve_url(url)
    streams = plugin.streams()

    if streams:

        return streams


def sl_hosts(url):

    return any(
        [
            'dailymotion' in url and control.setting('dm_resolve') == '1', 'twitch' in url, 'facebook' in url, 'ttvnw' in url,
            'periscope' in url and not 'search' in url,
            'pscp' in url, 'ant1.com.cy' in url and 'web-tv-live' in url,
            'gr.euronews.com' in url and not 'watchlive.json' in url, 'filmon.com' in url, 'ellinikosfm.com' in url,
            'alphatv.gr' in url, 'kineskop.tv' in url, 'player.vimeo.com' in url,
            'omegatv' in url and 'live' in url, control.setting('ol_resolve') == '1' and re.search(openload_regex, url)
        ]
    )
