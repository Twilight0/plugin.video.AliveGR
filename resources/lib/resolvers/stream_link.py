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
from streamlink.exceptions import NoPluginError, NoStreamsError
from tulip import control, log

openload_regex = r'https?://(?P<domain>o(?:pen)?load\.(?:io|co|tv|stream|win|download|info|icu|fun|pw))/(?:embed|f)/(?P<streamid>[\w-]+)'


def wrapper(url):

    session = streamlink.session.Streamlink()

    custom_plugins = control.join(control.addonPath, 'resources', 'lib', 'resolvers', 'sl_plugins')
    session.load_plugins(custom_plugins)

    if 'omegatv.com.cy' in url:
        session.set_plugin_option('omegacy', 'parse_hls', 'false')
    elif 'ant1.com.cy' in url:
        session.set_plugin_option('ant1cy', 'parse_hls', 'false')
    elif 'antenna.gr' in url:
        session.set_plugin_option('ant1gr', 'parse_hls', 'false')
    elif 'tvopen.gr' in url:
        session.set_plugin_option('opentv', 'parse_hls', 'false')
    elif 'star.gr/tv/live-stream/' in url:
        session.set_plugin_option('stargr', 'parse_hls', 'false')

    try:

        plugin = session.resolve_url(url)

        return plugin.streams()

    except (NoPluginError, NoStreamsError) as e:

        log.log_debug('Streamlink failed due to following reason: ' + e)
        return


def hosts(url):

    return any(
        [
            'dailymotion' in url and control.setting('dm_resolve') == '1', 'twitch' in url, 'facebook' in url, 'ttvnw' in url,
            'periscope' in url and 'search' not in url, 'pscp' in url, 'ant1.com.cy' in url, 'netwix.gr' in url, 'tvopen.gr' in url,
            'gr.euronews.com' in url and 'watchlive.json' not in url, 'filmon.com' in url, 'ellinikosfm.com' in url,
            'kineskop.tv' in url, 'player.vimeo.com' in url, 'antenna.gr' in url, 'star.gr/tv/live-stream/' in url,
            'omegatv' in url and 'live' in url, control.setting('ol_resolve') == '1' and re.search(openload_regex, url)
        ]
    )
