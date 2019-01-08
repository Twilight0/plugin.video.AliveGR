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

from tulip import control, directory, cache, client, youtube
from tulip.log import log_debug
from tulip.compat import urljoin, iteritems
from resources.lib.modules.themes import iconname
from resources.lib.modules.constants import yt_url, art_id, api_keys
from resources.lib.modules.helpers import thgiliwt
from resources.lib.resolvers.youtube import replace_url
from resources.lib.modules.youtube import thumb_maker
from resources.lib.indexers import gm
from datetime import datetime


# noinspection PyUnboundLocalVariable
class Indexer:

    def __init__(self, argv):

        self.list = []; self.data = []
        self.mgreekz_id = 'UClMj1LyMRBMu_TG1B1BirqQ'
        self.mgreekz_url = 'http://mad.tv/'
        self.rythmos_url = 'https://www.rythmosfm.gr/'
        self.plus_url = 'http://plusradio.gr/top20'
        self.radiopolis_url_gr = 'http://www.radiopolis.gr/elliniko-radio-polis-top-20/'
        self.radiopolis_url_other = 'http://www.radiopolis.gr/to-kseno-polis-top-20/'
        self.rythmos_top20_url = urljoin(self.rythmos_url, 'community/top20/')
        if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)'):
            self.content = 'songs'
            self.infotype = 'music'
        else:
            self.content = 'musicvideos'
            self.infotype = 'video'
        self.argv = argv

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
                    addonid=art_id, theme='networks', icon='mgz_fanart.jpg', media_subfolder=False
                )
            }
            ,
            {
                'title': control.lang(30127),
                'action': 'mgreekz_top10',
                'image': 'https://pbs.twimg.com/profile_images/697098521527328772/VY8e_klm_400x400.png',
                'fanart': control.addonmedia(
                    addonid=art_id, theme='networks', icon='mgz_fanart.jpg', media_subfolder=False
                )
            }
            ,
            {
                'title': control.lang(30128),
                'action': 'top20_list',
                'url': self.rythmos_top20_url,
                'image': 'https://is3-ssl.mzstatic.com/image/thumb/Purple62/v4/3e/a4/48/3ea44865-8cb2-5fec-be70-188a060b712c/source/256x256bb.jpg',
                'fanart': control.addonmedia(
                    addonid=art_id,
                    theme='networks',
                    icon='rythmos_fanart.jpg',
                    media_subfolder=False
                )
            }
            ,
            {
                'title': control.lang(30221),
                'action': 'top20_list',
                'url': self.plus_url,
                'image': 'https://is5-ssl.mzstatic.com/image/thumb/Purple20/v4/e8/99/e8/e899e8ea-0df6-0f60-d66d-b82b8021e8af/source/256x256bb.jpg',
                'fanart': 'https://i.imgur.com/G8koVR8.jpg'
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
                'url': 'https://alivegr.net/raw/top50.xml',
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

        log_debug('Music section loaded')
        directory.add(self.list, argv=self.argv)

    def gm_music(self):

        html = cache.get(gm.root, 96, gm.music_link)

        options = re.compile('(<option  value=.+?</option>)', re.U).findall(html)

        for option in options:

            title = client.parseDOM(option, 'option')[0]
            link = client.parseDOM(option, 'option', ret='value')[0]
            link = urljoin(gm.base_link, link)

            data = {'title': title, 'url': link, 'image': iconname('music'), 'action': 'artist_index'}

            self.list.append(data)

        directory.add(self.list, argv=self.argv)

    def music_list(self, url):

        html = client.request(url)

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
            icon = urljoin(gm.base_link, icon)
        else:
            icon = iconname('music')

        for item in items:

            title = client.parseDOM(item, 'a')[0]
            link = client.parseDOM(item, 'a', ret='href')[0]
            link = urljoin(gm.base_link, link)

            data = {'title': title, 'url': link, 'image': icon, 'artist': artist}

            self.list.append(data)

        return self.list

    def artist_index(self, url):

        self.list = cache.get(self.music_list, 48, url)

        if self.list is None:
            log_debug('Artist\'s section failed to load')
            return
        else:
            log_debug('Artist index section list:' + ' ' + str(self.list))

        for item in self.list:
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            item.update({'cm': [bookmark_cm], 'action': 'album_index'})

        directory.add(self.list, argv=self.argv)

    def album_index(self, url):

        self.list = cache.get(self.music_list, 48, url)

        if self.list is None:
            log_debug('Album index section failed to load successfully')
            return
        else:
            log_debug('Album index section list:' + ' ' + str(self.list))

        for item in self.list:
            item.update(
                {
                    'action': 'songs_index', 'name': item['title'].partition(' (')[0],
                    'year': int(item['title'].partition(' (')[2][:-1])
                }
            )

        directory.add(self.list, content=self.content, infotype=self.infotype, argv=self.argv)

    def songs_index(self, url, album):

        self.list = cache.get(self.music_list, 48, url)

        if self.list is None:
            log_debug('Songs section failed to load')
            return
        else:
            log_debug('Song section list:' + ' ' + str(self.list))

        for item in self.list:
            item.update({'action': 'play', 'isFolder': 'False'})

        for count, item in list(enumerate(self.list, start=1)):
            add_to_playlist = {'title': 30226, 'query': {'action': 'add_to_playlist'}}
            clear_playlist = {'title': 30227, 'query': {'action': 'clear_playlist'}}
            item.update({'cm': [add_to_playlist, clear_playlist], 'album': album.encode('latin-1'), 'tracknumber': count})

        directory.add(self.list, content=self.content, infotype=self.infotype, argv=self.argv)

    def mgreekz_index(self):

        self.data = cache.get(youtube.youtube(key=thgiliwt(api_keys['api_key']), replace_url=replace_url).playlists, 48, self.mgreekz_id)

        for i in self.data:
            i.update(
                {
                    'action': 'mgreekz_list', 'fanart': control.addonmedia(
                    addonid=art_id, theme='networks', icon='mgz_fanart.jpg', media_subfolder=False
                )
                }
            )

        for item in self.data:
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            item.update({'cm': [bookmark_cm]})

        self.list = sorted(self.data, key=lambda k: k['title'].lower())

        directory.add(self.list, argv=self.argv)

    def mgreekz_list(self, url):

        self.list = cache.get(youtube.youtube(key=thgiliwt(api_keys['api_key']), replace_url=replace_url).playlist, 12, url)

        if self.list is None:

            return

        for i in self.list:
            i.update(
                {
                    'action': 'play', 'isFolder': 'False',
                }
            )

        directory.add(self.list, content=self.content, infotype=self.infotype, argv=self.argv)

    def _mgreekz_top10(self):

        from youtube_requests import get_search

        html = client.request(self.mgreekz_url)

        spotify_playlist_url = client.parseDOM(html, 'iframe', ret='src')[0]

        spotify_html = client.request(spotify_playlist_url)

        spotify_object = client.parseDOM(spotify_html, 'script', attrs={'id': 'resource', 'type': 'application/json'})[0]

        json_object = json.loads(spotify_object)

        comment = plot = json_object.get('description')

        tracks = json_object.get('tracks').get('items')

        for track in tracks:

            song = track.get('track')

            title = song.get('name')

            artists = on_label = [i['name'] for i in song.get('artists')]

            if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)'):
                artists = ' / '.join(artists)

            search = get_search(q=title + ' ' + 'official', search_type='video')[0]
            vid = search['id']['videoId']
            link = yt_url + vid
            image = thumb_maker(link.rpartition('/' if 'youtu.be' in link else '=')[2])

            self.list.append(
                {
                    'label': title + ' - ' + ' & '.join(on_label), 'url': link, 'album': 'Mad Greek Top 10',
                    'image': image, 'artist': artists, 'comment': comment, 'plot': plot, 'title': title
                }
            )

        return self.list

    def mgreekz_top10(self):

        self.list = cache.get(self._mgreekz_top10, 24)

        if self.list is None:
            log_debug('Mad Greekz top 10 section failed to load')
            return
        else:
            log_debug('Mad Greekz list:' + ' ' + str(self.list))

        for item in self.list:
            item.update({'action': 'play', 'isFolder': 'False'})

        for count, item in list(enumerate(self.list, start=1)):
            add_to_playlist = {'title': 30226, 'query': {'action': 'add_to_playlist'}}
            clear_playlist = {'title': 30227, 'query': {'action': 'clear_playlist'}}
            item.update(
                {
                    'cm': [add_to_playlist, clear_playlist], 'album': control.lang(30127),
                    'fanart': control.addonmedia(
                        addonid=art_id, theme='networks', icon='mgz_fanart.jpg',
                        media_subfolder=False
                    ), 'tracknumber': count, 'code': count
                }
            )

        control.sortmethods('tracknum', mask='%A')
        directory.add(self.list, content=self.content, infotype=self.infotype, argv=self.argv)

    def _top20(self, url):

        from youtube_requests import get_search

        cookie = client.request(url, close=False, output='cookie')
        html = client.request(url, cookie=cookie)

        if url == self.rythmos_top20_url:
            attributes = {'class': 'va-title'}
        elif url == self.plus_url:
            attributes = {'class': 'element element-itemname first last'}
        elif url == self.radiopolis_url_gr or url == self.radiopolis_url_other:
            attributes = {'class': 'thetopdata'}

        items = client.parseDOM(
            html, 'td' if 'radiopolis' in url else 'div', attrs=attributes
        )

        year = str(datetime.now().year)

        for item in items:

            if url == self.rythmos_top20_url:
                label = client.parseDOM(item, 'span', attrs={'class': 'toptitle'})[0]
                label = client.replaceHTMLCodes(label)
                label = re.sub('\s? ?-\s? ?', ' - ', label)
                image = client.parseDOM(item, 'img', ret='src')[0]
                image = image.replace(' ', '%20')
                title = label.partition(' - ')[2]
                if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)'):
                    artist = label.partition(' - ')[0]
                else:
                    artist = [label.partition(' - ')[0]]
            elif url == self.plus_url:
                label = item.partition('.')[2].strip()
                title = label.partition('-')[2]
                if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)'):
                    artist = label.partition('-')[0]
                else:
                    artist = [label.partition('-')[0]]
            elif url == self.radiopolis_url_gr or url == self.radiopolis_url_other:
                a_href = client.parseDOM(item, 'a')
                a_href = ' - '.join(a_href) if len(a_href) == 2 else a_href[0]
                label = client.stripTags(a_href.replace('\"', '').replace('&amp;', '&').replace('\n', ' - '))
                title = label.partition(' - ')[2]
                if control.setting('audio_only') == 'true' and control.condVisibility('Window.IsVisible(music)'):
                    artist = label.partition(' - ')[0]
                else:
                    artist = [label.partition(' - ')[0]]

            if any([url == self.rythmos_top20_url, url == self.plus_url]):
                search = get_search(q=title + ' ' + 'official', search_type='video')[0]
                description = search['snippet']['description']
                year = search['snippet']['publishedAt'][:4]
                vid = search['id']['videoId']
                image = search['snippet']['thumbnails']['default']['url']
                link = yt_url + vid
            elif url == self.radiopolis_url_gr or url == self.radiopolis_url_other:
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

        self.list = cache.get(self._top20, 24, url)

        if self.list is None:
            log_debug('Top 20 list section failed to load')
            return
        else:
            log_debug('Top 20 list section list:' + ' ' + str(self.list))

        if url == self.rythmos_top20_url:
            fanart = control.addonmedia(
                addonid=art_id, theme='networks', icon='rythmos_fanart.jpg',
                media_subfolder=False
            )
            album = control.lang(30128)
        elif url == self.plus_url:
            fanart = 'https://i.imgur.com/G8koVR8.jpg'
            album = control.lang(30221)
        elif url == self.radiopolis_url_gr or url == self.radiopolis_url_other:
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
        directory.add(self.list, content=self.content, infotype=self.infotype, argv=self.argv)

    def _top50(self, url):

        if control.setting('debug') == 'false':

            playlists = client.request(url)

        else:

            if control.setting('local_remote') == '0':
                local = control.setting('top50_local')
                with open(local) as xml:
                    playlists = xml.read()
                    xml.close()
            elif control.setting('local_remote') == '1':
                playlists = client.request(control.setting('top50_remote'))
            else:
                playlists = client.request(url)

        self.data = client.parseDOM(playlists, 'item')

        for item in self.data:

            title = client.parseDOM(item, 'title')[0]
            url = client.parseDOM(item, 'url')[0]
            image = thumb_maker(url.rpartition('=')[2])
            plot = client.parseDOM(item, 'description')[0]
            duration = client.parseDOM(item, 'duration')[0].split(':')
            duration = (int(duration[0]) * 60) + int(duration[1])

            item_data = (
                {
                    'label': title, 'title': title.partition(' - ')[2], 'image': image, 'url': url, 'plot': plot,
                    'comment': plot, 'duration': duration
                }
            )

            self.list.append(item_data)

        return self.list

    def top50_list(self, url):

        self.list = cache.get(self._top50, 48, url)

        if self.list is None:
            log_debug('Developer\'s picks section failed to load')
            return
        else:
            log_debug('Top 50 list:' + ' ' + str(self.list))

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
        directory.add(self.list, content=self.content, infotype=self.infotype, argv=self.argv)

    def techno_choices(self, url):

        self.list = cache.get(youtube.youtube(key=thgiliwt(api_keys['api_key']), replace_url=replace_url).playlist, 12, url)

        if self.list is None:

            return

        for i in self.list:
            i['label'] = i.pop('title')
            # process stupid descriptions/comments put up by uploaders on labels
            i['label'] = re.sub(r'PREMIERE ?:|\(full version\)\.mp4|\(?(?:Un)?Official.*\)? ?(?:HD)?|\[?HD (?:108|72)0p\]?', '', i['label'], flags=re.IGNORECASE)

        for count, i in list(enumerate(self.list, start=1)):

            if '–' in i['label']:
                sep = '–'
            elif ':' in i['label'] and not '-' in i['label']:
                sep = ':'
            else:
                sep = '-'

            artist, separator, title = i['label'].partition(sep)

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

        directory.add(self.list, content=self.content, infotype=self.infotype, argv=self.argv)
