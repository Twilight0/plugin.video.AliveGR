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

import json, youtu_be, re, urllib

from tulip import control, directory, cache, client
from urlparse import urljoin
from ..modules.themes import iconname
from ..modules import syshandle
from ..modules.helpers import thgiliwt
from ..modules.tools import api_keys


class Main:

    def __init__(self):

        self.list = []; self.data = []
        self.mgreekz_id = 'UClMj1LyMRBMu_TG1B1BirqQ'
        self.mgreekz_url = 'http://mad.tv/mad-hits-top-10/'
        self.rythmos_url = 'https://www.rythmosfm.gr/'
        self.top20_url = urljoin(self.rythmos_url, 'community/top20/')
        self.rythmos_top20_base = urljoin(self.rythmos_url, 'Userfiles/TopTwentyAudio/')

    def root(self):

        self.list = [
            {
                'title': 30170,
                'action': 'music_live',
                'image': iconname('monitor'),
                'fanart': 'https://i.ytimg.com/vi/vtjL9IeowUs/maxresdefault.jpg'
            }
            ,
            {
                'title': 30124,
                'action': 'gm_music',
                'image': iconname('music'),
                'fanart': 'https://cdn.allwallpaper.in/wallpapers/1280x720/1895/music-hd-1280x720-wallpaper.jpg'
            }
            ,
            {
                'title': 30126,
                'action': 'mgreekz_index',
                'image': 'https://pbs.twimg.com/profile_images/697098521527328772/VY8e_klm_400x400.png',
                'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='mgz_fanart.jpg')
            }
            ,
            {
                'title': 30127,
                'action': 'mgreekz_top10',
                'image': 'https://pbs.twimg.com/profile_images/697098521527328772/VY8e_klm_400x400.png',
                'fanart': control.addonmedia(addonid='script.AliveGR.artwork', theme='networks', icon='mgz_fanart.jpg')
            }
            ,
            {
                'title': 30128,
                'action': 'rythmos_top20',
                'image': 'https://is3-ssl.mzstatic.com/image/thumb/Purple62/v4/3e/a4/48/3ea44865-8cb2-5fec-be70-188a060b712c/source/256x256bb.jpg',
                'fanart': control.addonmedia(
                    addonid='script.AliveGR.artwork',
                    theme='networks',
                    icon='rythmos_fanart.jpg'
                )
            }
        ]

        directory.add(self.list)

    def mgreekz_index(self):

        self.list = youtu_be.yt_playlists(self.mgreekz_id)

        if self.list is None:
            return

        for item in self.list:
            item.update(
                {
                    'fanart': control.addonmedia(
                        addonid='script.AliveGR.artwork',
                        theme='networks',
                        icon='mgz_fanart.jpg'
                    )
                }
            )

        directory.add(self.list)

    def items_top10(self):

        html = client.request(self.mgreekz_url)

        image = 'https://pbs.twimg.com/profile_images/697098521527328772/VY8e_klm_400x400.png'

        items = client.parseDOM(html, 'iframe', attrs={'class': 'youtube-player'}, ret='src')

        for item in items:

            title = html.decode('utf-8').split(item)[0]
            title = client.parseDOM(title, 'strong')[-1].strip()
            title = client.replaceHTMLCodes(title)

            url = item.partition('?')[0]

            self.list.append({'title': title, 'url': url, 'image': image, 'artist': [title.partition(u' – ')[2]]})

        return self.list

    def mgreekz_top10(self):

        self.list = cache.get(self.items_top10, 24)

        if self.list is None:
            return

        for item in self.list:
            item.update(
                {
                    'action': 'play', 'isFolder': 'False', 'album': 'Mad Greekz top 10',
                    'fanart': control.addonmedia(
                        addonid='script.AliveGR.artwork', theme='networks', icon='mgz_fanart.jpg'
                    )
                 }
            )

        self.list = self.list[::-1]

        for count, item in list(enumerate(self.list, start=1)):
            item.setdefault('tracknumber', count)

        directory.add(self.list, content='musicvideos')

    def items_top20(self):

        from youtube_requests import get_search

        cookie = client.request(self.top20_url, close=False, output='cookie')
        html = client.request(self.top20_url, cookie=cookie)

        items = client.parseDOM(html, 'div', attrs={'class': 'va-title'})

        for count, item in list(enumerate(items, start=1)):

            title = client.parseDOM(item, 'span', attrs={'class': 'toptitle'})[0]
            title = client.replaceHTMLCodes(title)
            image = client.parseDOM(item, 'img', ret='src')[0]
            image = image.replace(' ', '%20')
            link = get_search(q=title + ' ' + 'official', search_type='video')[0]
            link = link['snippet']['thumbnails']['default']['url']
            link = re.findall('vi/([\w-]*?)/', link)[0]
            link = urljoin(youtu_be.base_link, link)
            # file_ = client.parseDOM(item, 'span', attrs={'onclick': 'javascript.+?'}, ret='onclick')[0]
            # file_ = file_.encode('utf-8')
            # file_ = re.findall("Audio/(.*?(?:.mp3|.wav))\'", file_)[0]
            # file_ = urljoin(self.rythmos_top20_base, file_.replace(' ', '%20'))

            self.list.append(
                {
                    'title': str(count) + '. ' + title, 'url': link, 'image': image, 'artist': [title.partition(' - ')[0]]
                }
            )

        return self.list

    def rythmos_top20(self):

        self.list = cache.get(self.items_top20, 24)

        if self.list is None:
            return

        for item in self.list:
            item.update(
                {
                    'action': 'play', 'isFolder': 'False', 'album': 'Rytmhos 949 top 20',
                    'fanart': control.addonmedia(
                        addonid='script.AliveGR.artwork',
                        theme='networks',
                        icon='rythmos_fanart.jpg'
                    )
                }
            )

        for count, item in list(enumerate(self.list, start=1)):
            item.setdefault('tracknumber', count)

        directory.add(self.list, content='musicvideos')
