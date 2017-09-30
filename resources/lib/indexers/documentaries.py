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

import json, re

from tulip import youtube, cache, directory, control, workers
from ..modules import syshandle
from ..modules.tools import api_keys
from ..modules.themes import iconname
from ..modules.helpers import thgiliwt


class Main:

    def __init__(self):

        self.list = [] ; self.data = []; self.threads = []
        self.youtube_link1 = 'UC_PpGZM3lLNnMp4kPpMfOqA'
        self.youtube_link2 = 'UCzO7QRrwwscJMGfjf52q_fA'
        self.youtube_link3 = 'UCAv_XZUa_qItspsAiZK8bQg'
        self.youtube_link4 = 'PL1CA7E2691399A724'
        self.youtube_link5 = 'PL6B61F6F5FF763F17'
        self.youtube_link6 = 'PL548D38E101E0A09F'
        self.youtube_link7 = 'PL6FD8970BF53E4CB8'
        self.youtube_link8 = 'PL4qYYh-kGH3ZOHVikP9H3GUylktTkRC4D'
        self.youtube_link9 = 'PLb8uy1Cvcjmx798IHlPWWN130pvrfNeMq'
        # self.youtube_link10 = 'UCXr6dzk36oq5zhiU-8SrWLA'
        self.youtube_extra = u'https://www.youtube.com/watch?v=oLjGJOP9Cb4'

    def documentaries(self):

        self.data = [
            {
                'title': control.lang(30041),
                'url': 'plugin://plugin.video.AliveGR/?action=listing&url=http://greek-movies.com/movies.php?g=6&y=&l=&p=',
                'icon': iconname('documentaries')
            }
            ,
            {
                'title': control.lang(30042),
                'url': 'plugin://plugin.video.AliveGR/?action=yt_documentaries',
                'icon': iconname('documentaries')
            }
            ]

        for item in self.data:
            list_item = control.item(label=item['title'])
            list_item.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            _url_ = item['url']
            isFolder = True
            self.list.append((_url_, list_item, isFolder))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def items_list(self):

        key = thgiliwt(api_keys['api_key'])

        channel1 = youtube.youtube(key=key).videos(self.youtube_link1)

        channel2 = [
            item for item in youtube.youtube(key=key).videos(self.youtube_link2) if 'ΝΤΟΚΙΜΑΝΤΕΡ' in item['title']
        ]

        channel3 = youtube.youtube(key=key).videos(self.youtube_link3)
        channel4 = youtube.youtube(key=key).playlist(self.youtube_link4)
        channel5 = youtube.youtube(key=key).playlist(self.youtube_link5); ch5 = channel5
        channel6 = youtube.youtube(key=key).playlist(self.youtube_link6); ch6 = channel6
        channel7 = youtube.youtube(key=key).playlist(self.youtube_link7); ch7 = channel7
        channel8 = youtube.youtube(key=key).playlist(self.youtube_link8)
        channel9 = youtube.youtube(key=key).playlist(self.youtube_link9)
        # channel10 = youtube.youtube(key=key).videos(self.youtube_link10)

        # dictionary comprehension not compatible with python 2.6:
        # channel1_fixed = [
        #     {key: re.sub('^\d{2} ', '', item[key]) if key == 'title' else value for key, value in item.items()}
        #     for item in channel1
        # ]
        # channel2_fixed = [
        #     {key: item[key].partition(' - ')[2] if key == 'title' else value for key, value in item.items()}
        #     for item in channel2_fixed
        # ]

        ch1 = [dict(
            (
                k, re.sub('^\d{2} ', '', item[k]) if (k == 'title') else v
            ) for k, v in item.items()) for item in channel1]

        ch2 = [dict(
            (
                k, item[k].partition(' - ')[2] if (k == 'title') else v
            ) for k, v in item.items()) for item in channel2]

        ch3 = [item for item in channel3 if int(item['duration']) >= 600]
        ch4 = [item for item in channel4 if int(item['duration']) >= 900]

        ch8 = [dict(
            (
                k, item[k].partition(' (ΝΤΟΚΙΜΑΝΤΕΡ')[0] if (k == 'title') else v
            ) for k, v in item.items()) for item in channel8]

        ch9 = [dict(
            (
                k, re.sub('Discover.+[~:]', '', item[k]).strip() if (k == 'title') else v
            ) for k, v in item.items()) for item in channel9]

        # ch10 = [dict(
        #     (
        #         k, item[k].partition(' (ΝΤΟΚΙΜΑΝΤΕΡ')[0] if (k == 'title') else v
        #     ) for k, v in item.items()) for item in channel10]

        self.list = ch1 + ch2 + ch3 + ch4 + ch5 + ch6 + ch7 + ch8 + ch9

        self.data = [
            {
                'title': 'Η ταχύτητα του φωτός', 'image': u'https://i.ytimg.com/vi/oLjGJOP9Cb4/mqdefault.jpg',
                'url': self.youtube_extra, 'duration': 2629
            }
        ]

        self.list += self.data

        return self.list

    def yt_documentaries(self):

        self.data = cache.get(self.items_list, 48)

        if self.data is None:
            return

        for i in self.data:
            i.update({'action': 'play', 'isFolder': 'False'})

        for item in self.data:
            bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
            bookmark['bookmark'] = item['url']
            item.update({'cm': [{'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}]})

        self.list = sorted(self.data, key=lambda k: k['title'].lower())

        directory.add(self.list, content='movies')
