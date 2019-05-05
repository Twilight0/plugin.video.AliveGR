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

import streamlink.session
from tulip import control


def sl_session(url):

    custom_plugins = control.join(control.addonPath, 'resources', 'lib', 'resolvers', 'sl_plugins')

    session = streamlink.session.Streamlink()
    session.load_plugins(custom_plugins)

    plugin = session.resolve_url(url)
    streams = plugin.streams()

    if streams:

        return streams


def sl_hosts(url):

    return [
        'ustream' in url, 'dailymotion' in url, 'twitch' in url, 'facebook' in url, 'ttvnw' in url,
        'periscope' in url and not 'search' in url, 'pscp' in url, 'ant1.com.cy' in url,
        'openload' in url and control.setting('ol_resolve') == '1', 'gr.euronews.com' in url and not 'watchlive.json' in url,
        'filmon.com' in url, 'ellinikosfm.com' in url, 'alphatv.gr' in url, 'kineskop.tv' in url, 'player.vimeo.com' in url
    ]
