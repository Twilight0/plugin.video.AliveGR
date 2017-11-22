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

################################
#### Reserved for later use ####
####    Needs refinement    ####
################################

# import YDStreamExtractor
# from tulip import control
# from ..modules.helpers import stream_picker
#
#
# def session(url):
#
#     qualities = []
#     links = []
#
#     stream = YDStreamExtractor.getVideoInfo(url)
#
#     if stream.hasMultipleStreams() and control.setting('ytdl_quality_picker') == '1':
#
#         for s in stream.streams():
#
#             quality = s['title']
#             qualities.append(quality)
#             links.append(stream.selectStream(quality))
#
#         return stream_picker(qualities, links)
#
#     else:
#
#         try:
#             stream = stream.streamURL()
#             return stream
#         except AttributeError:
#             return 30112
