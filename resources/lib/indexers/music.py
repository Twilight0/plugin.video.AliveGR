# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''
from __future__ import absolute_import, unicode_literals

import json, re

from tulip import control, directory, client
from tulip.log import log_debug
from tulip.compat import urljoin, iteritems
from ..modules.themes import iconname
from ..modules.constants import YT_URL, ART_ID, cache_method, cache_duration
from ..modules.utils import thgiliwt, thumb_maker, keys_registration, yt_playlists, yt_playlist
from . import gm
from datetime import datetime
from youtube_requests import get_search


# noinspection PyUnboundLocalVariable
class Indexer:

    def __init__(self):

        self.list = []; self.data = []
        self.mgreekz_id = 'UClMj1LyMRBMu_TG1B1BirqQ'
        self.radiopolis_url_gr = 'https://www.radiopolis.gr/elliniko-radio-polis-top-20/'
        self.radiopolis_url_other = 'https://www.radiopolis.gr/to-kseno-polis-top-20/'
        if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)'):
            self.content = 'songs'
            self.infotype = 'music'
        else:
            self.content = 'musicvideos'
            self.infotype = 'video'
        keys_registration()

    def menu(self):

        self.list = [
            {
                'title': control.lang(30170),
                'action': 'music_live',
                'image': iconname('monitor'),
                'fanart': 'https://i.ytimg.com/vi/vtjL9IeowUs/maxresdefault.jpg'
            }
            ,
            {
                'title': control.lang(30124),
                'action': 'gm_music',
                'image': iconname('music'),
                'fanart': 'https://cdn.allwallpaper.in/wallpapers/1280x720/1895/music-hd-1280x720-wallpaper.jpg'
            }
            ,
            {
                'title': control.lang(30126),
                'action': 'mgreekz_index',
                'image': 'https://pbs.twimg.com/profile_images/697098521527328772/VY8e_klm_400x400.png',
                'fanart': control.addonmedia(
                    addonid=ART_ID, theme='networks', icon='mgz_fanart.jpg', media_subfolder=False
                )
            }
            ,
            {
                'title': control.lang(30222),
                'action': 'top20_list',
                'url': self.radiopolis_url_gr,
                'image': 'http://www.radiopolis.gr/wp-content/uploads/2017/11/noimageavailable.jpg',
                'fanart': 'https://i.ytimg.com/vi/tCupKdpHVx8/maxresdefault.jpg'
            }
            ,
            {
                'title': control.lang(30223),
                'action': 'top20_list',
                'url': self.radiopolis_url_other,
                'image': 'http://www.radiopolis.gr/wp-content/uploads/2017/11/noimageavailable.jpg',
                'fanart': 'https://i.ytimg.com/vi/tCupKdpHVx8/maxresdefault.jpg'
            }
            ,
            {
                'title': control.lang(30269),
                'action': 'top50_list',
                'url': 's1GeuATNw9GdvcXYy9Cdl5mLydWZ2lGbh9yL6MHc0RHa',
                'image': control.addonInfo('icon'),
                'fanart': 'https://i.ytimg.com/vi/vtjL9IeowUs/maxresdefault.jpg'
            }
            ,
            {
                'title': control.lang(30292),
                'action': 'techno_choices',
                'url': 'PLZF-_NNdxpb5s1vjh6YSMTyjjlfiZhgbp',
                'image': control.addonInfo('icon'),
                'fanart': 'https://i.ytimg.com/vi/vtjL9IeowUs/maxresdefault.jpg'
            }
        ]

        if control.condVisibility('Window.IsVisible(music)'):
            del self.list[0]

        directory.add(self.list)

    def gm_music(self):

        html = gm.root(gm.MUSIC)

        options = re.compile(r'(<option  value=.+?</option>)', re.U).findall(html)

        for option in options:

            title = client.parseDOM(option, 'option')[0]
            link = client.parseDOM(option, 'option', ret='value')[0]
            link = urljoin(gm.GM_BASE, link)

            data = {'title': title, 'url': link, 'image': iconname('music'), 'action': 'artist_index'}

            self.list.append(data)

        directory.add(self.list)

    @cache_method(cache_duration(2880))
    def music_list(self, url):

        html = client.request(url)

        try:

            html = html.decode('utf-8')

        except Exception:

            pass

        if 'albumlist' in html:
            artist = [client.parseDOM(html, 'h4')[0].partition(' <a')[0]]
        else:
            artist = None

        if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)') and artist is not None:
            artist = ''.join(artist)

        if 'songlist' in html:
            songlist = client.parseDOM(html, 'div', attrs={'class': 'songlist'})[0]
            items = client.parseDOM(songlist, 'li')
        elif 'albumlist' in html:
            albumlist = client.parseDOM(html, 'div', attrs={'class': 'albumlist'})[0]
            items = client.parseDOM(albumlist, 'li')
        else:
            artistlist = client.parseDOM(html, 'div', attrs={'class': 'artistlist'})[0]
            items = client.parseDOM(artistlist, 'li')

        if 'icon/music' in html:
            icon = client.parseDOM(html, 'img', attrs={'class': 'img-responsive'}, ret='src')[-1]
            icon = urljoin(gm.GM_BASE, icon)
        else:
            icon = iconname('music')

        for item in items:

            title = client.parseDOM(item, 'a')[0]
            link = client.parseDOM(item, 'a', ret='href')[0]
            link = urljoin(gm.GM_BASE, link)

            if 'gapi.client.setApiKey' in html:
                link = gm.source_maker(url)['links'][0]

            data = {'title': title, 'url': link, 'image': icon}

            if artist:

                data.update({'artist': artist})

            self.list.append(data)

        return self.list

    def artist_index(self, url, get_list=False):

        self.list = self.music_list(url)

        for item in self.list:
            item.update({'action': 'album_index'})
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            item.update({'cm': [bookmark_cm]})

        if get_list:
            return self.list
        else:
            directory.add(self.list)

    def album_index(self, url):

        self.list = self.music_list(url)

        for item in self.list:
            item.update(
                {
                    'action': 'songs_index', 'name': item['title'].partition(' (')[0],
                    'year': int(item['title'].partition(' (')[2][:-1])
                }
            )

        directory.add(self.list, content=self.content, infotype=self.infotype)

    def songs_index(self, url, album):

        self.list = self.music_list(url)

        for count, item in list(enumerate(self.list, start=1)):

            item.update({'action': 'play', 'isFolder': 'False'})
            add_to_playlist = {'title': 30226, 'query': {'action': 'add_to_playlist'}}
            clear_playlist = {'title': 30227, 'query': {'action': 'clear_playlist'}}
            item.update({'cm': [add_to_playlist, clear_playlist], 'album': album.encode('latin-1'), 'tracknumber': count})

        directory.add(self.list, content=self.content, infotype=self.infotype)

    def mgreekz_index(self):

        self.data = yt_playlists(self.mgreekz_id)

        for i in self.data:
            i.update(
                {
                    'action': 'mgreekz_list', 'fanart': control.addonmedia(
                    addonid=ART_ID, theme='networks', icon='mgz_fanart.jpg', media_subfolder=False
                )
                }
            )

        for item in self.data:
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            item.update({'cm': [bookmark_cm]})

        self.list = sorted(self.data, key=lambda k: k['title'].lower())

        directory.add(self.list)

    def mgreekz_list(self, url):

        self.list = yt_playlist(url)

        for i in self.list:
            i.update(
                {
                    'action': 'play', 'isFolder': 'False',
                }
            )

        directory.add(self.list, content=self.content, infotype=self.infotype)

    @cache_method(cache_duration(1440))
    def _top20(self, url):

        cookie = client.request(url, close=False, output='cookie')
        html = client.request(url, cookie=cookie)

        attributes = {'class': 'thetopdata'}

        items = client.parseDOM(html, 'td', attrs=attributes)

        year = str(datetime.now().year)

        for item in items:

            a_href = client.parseDOM(item, 'a')
            a_href = ' - '.join(a_href) if len(a_href) == 2 else a_href[0]
            label = client.stripTags(a_href.replace('\"', '').replace('\n', ' - '))
            label = client.replaceHTMLCodes(label)
            title = label.partition(' - ')[2]
            if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)'):
                artist = label.partition(' - ')[0]
            else:
                artist = [label.partition(' - ')[0]]

            links = client.parseDOM(item, 'a', ret='href')
            link = links[1] if len(links) == 2 else links[0]
            image = thumb_maker(link.rpartition('/' if 'youtu.be' in link else '=')[2])
            description = None

            self.list.append(
                {
                    'label': label, 'url': link, 'image': image, 'title': title, 'artist': artist, 'plot': description,
                    'year': int(year)
                }
            )

        return self.list

    def top20_list(self, url):

        self.list = self._top20(url)

        if self.list is None:
            log_debug('Top 20 list section failed to load')
            return

        if url == self.radiopolis_url_gr or url == self.radiopolis_url_other:
            fanart = 'https://i.ytimg.com/vi/tCupKdpHVx8/maxresdefault.jpg'
            album = control.lang(30222)
        else:
            fanart = control.addonInfo('fanart')
            album = 'AliveGR \'s Top Music'

        for count, item in list(enumerate(self.list, start=1)):

            add_to_playlist = {'title': 30226, 'query': {'action': 'add_to_playlist'}}
            clear_playlist = {'title': 30227, 'query': {'action': 'clear_playlist'}}
            item.update(
                {
                    'tracknumber': count, 'cm': [add_to_playlist, clear_playlist], 'album': album, 'fanart': fanart,
                    'action': 'play', 'isFolder': 'False', 'code': count
                }
            )

        control.sortmethods('tracknum', mask='%A')
        directory.add(self.list, content=self.content, infotype=self.infotype)

    @cache_method(cache_duration(2880))
    def _top50(self, url):

        if control.setting('debug') == 'false':

            playlists = client.request(thgiliwt(url), headers={'User-Agent': 'AliveGR, version: ' + control.version()})

        else:

            if control.setting('local_remote') == '0':
                local = control.setting('top50_local')
                try:
                    with open(local, encoding='utf-8') as xml:
                        playlists = xml.read()
                except Exception:
                    with open(local) as xml:
                        playlists = xml.read()
            elif control.setting('local_remote') == '1':
                playlists = client.request(control.setting('top50_remote'))
            else:
                playlists = client.request(url)

        self.data = client.parseDOM(playlists, 'item')

        for item in self.data:

            title = client.parseDOM(item, 'title')[0]
            genre = client.parseDOM(item, 'genre')[0]
            url = client.parseDOM(item, 'url')[0]
            image = thumb_maker(url.rpartition('=')[2])
            plot = client.parseDOM(item, 'description')[0]
            duration = client.parseDOM(item, 'duration')[0].split(':')
            duration = (int(duration[0]) * 60) + int(duration[1])

            item_data = (
                {
                    'label': title, 'title': title.partition(' - ')[2], 'image': image, 'url': url, 'plot': plot,
                    'comment': plot, 'duration': duration, 'genre': genre
                }
            )

            self.list.append(item_data)

        return self.list

    def top50_list(self, url):

        self.list = self._top50(url)

        if self.list is None:
            log_debug('Developer\'s picks section failed to load')
            return

        for count, item in list(enumerate(self.list, start=1)):
            add_to_playlist = {'title': 30226, 'query': {'action': 'add_to_playlist'}}
            clear_playlist = {'title': 30227, 'query': {'action': 'clear_playlist'}}
            item.update(
                {
                    'action': 'play', 'isFolder': 'False', 'cm': [add_to_playlist, clear_playlist],
                    'album': control.lang(30269), 'fanart': 'https://i.ytimg.com/vi/vtjL9IeowUs/maxresdefault.jpg',
                    'tracknumber': count, 'code': count, 'artist': [item['label'].partition(' - ')[0]]
                }
            )

            if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)'):
                item['artist'] = item['artist'][0]

        control.sortmethods('tracknum', mask='%A')
        directory.add(self.list, content=self.content, infotype=self.infotype)

    def techno_choices(self, url):

        self.list = yt_playlist(url)

        if self.list is None:

            return

        for i in self.list:
            i['label'] = i.pop('title')
            # process stupid descriptions/comments put up by uploaders on labels
            i['label'] = re.sub(
                r'PREMIERE ?:|\(full version\)\.mp4|\(?(?:Un)?Official.*\)? ?(?:HD)?|\[?HD (?:108|72)0p\]?|\[HQ\]|\\\\ Free Download',
                '', i['label'], flags=re.IGNORECASE
            )

        for count, i in list(enumerate(self.list, start=1)):

            try:
                i['label'] = i['label'].decode('utf-8')
            except Exception:
                pass

            if u'–' in i['label']:
                sep = u'–'
            elif ':' in i['label'] and not '-' in i['label']:
                sep = ':'
            elif '-' in i['label']:
                sep = '-'
            else:
                sep = ' '

            artist, separator, title = i['label'].partition(sep)

            if sep not in i['label']:

                title = i['label']

            if '&' in artist:
                artists_separator = '&'
            elif ',' in artist:
                artists_separator = ','
            elif 'feat.' in artist:
                artists_separator = 'feat.'
            elif 'feat' in artist:
                artists_separator = 'feat'
            elif 'Feat' in artist:
                artists_separator = 'Feat'
            else:
                artists_separator = None

            if artists_separator:
                artist = [a.strip() for a in artist.split(artists_separator)]
                on_label = ' / '.join(artist)
            else:
                on_label = artist.strip()
                artist = [artist.strip()]

            i.update(
                {
                    'action': 'play', 'isFolder': 'False', 'title': title, 'label': ' '.join([on_label, separator , title]),
                    'album': control.lang(30292), 'fanart': 'https://i.ytimg.com/vi/vtjL9IeowUs/maxresdefault.jpg',
                    'tracknumber': count, 'count': count, 'artist': artist
                }
            )

            if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)'):
                i['artist'] = on_label

        control.sortmethods('tracknum', mask='%A')

        directory.add(self.list, content=self.content, infotype=self.infotype)
