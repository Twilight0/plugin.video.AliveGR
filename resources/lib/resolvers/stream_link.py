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
# import sys
from tulip import control


def sl_session(url):

    try:

        session = streamlink.session.Streamlink()
        # session.set_loglevel("debug")
        # session.set_logoutput(sys.stdin)
        plugin = session.resolve_url(url)
        streams = plugin.get_streams()

        try:
            del streams['audio_webm']
            del streams['audio_mp4']
        except KeyError:
            pass

        keys = streams.keys()
        values = [repr(u).partition('(\'')[2][:-3] for u in streams.values()]

        if control.setting('quality_picker') == '1':

            return stream_picker(keys, values)

        else:

            return repr(streams['best']).partition('(\'')[2][:-3]

    except:

        pass


def stream_picker(qualities, urls):

    choice = control.selectDialog(heading=control.lang(30064), list=qualities)

    if choice <= len(qualities) and not choice == -1:
        popped = urls.pop(choice)
        return popped
    else:
        return 30403
