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

# TODO: add dialog for quality
def resolve(url, quality='best'):

    try:

        session = streamlink.session.Streamlink()
        # session.set_loglevel("debug")
        # session.set_logoutput(sys.stdout)
        plugin = session.resolve_url(url)
        streams = plugin.get_streams()
        streams = repr(streams[quality])
        link = streams.partition('(\'')[2][:-3]

        return link

    except:
        pass

