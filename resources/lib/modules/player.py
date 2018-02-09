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

import random
import re
from urlparse import urljoin
from urllib import quote_plus

from tulip import directory, client, cache, control
import resolveurl as urlresolver
# import YDStreamExtractor
from ..resolvers import stream_link
import m3u8_loader
from tulip.log import *
from tulip.init import sysaddon
from ..indexers.gm import base_link
from ..resolvers import various, youtu
from ..modules.constants import yt_url, play_action
from youtube_plugin.youtube.youtube_exceptions import YouTubeException


def router(url):

    def yt_router(uri):

        if len(uri) == 11:

            uri = yt_url + uri

        try:
            yt_stream = youtu.wrapper(uri)
        except YouTubeException:
            try:
                yt_stream = stream_link.sl_session(uri)
            except:
                return

        return yt_stream

        # Reserved as failsafe:
        # if YDStreamExtractor.mightHaveVideo(url):
        #
        #     stream = ytdl_wrapper.session(url)
        #
        #     return stream

    if 'youtu' in url and not '#youtu_translator' in url:

        return yt_router(url)

        # Alternative method reserved:
        # if 'user' in url or 'channel' in url:
        #
        #     from ..resolvers import youtu
        #     stream = youtu.traslate(url, add_base=True)
        #     stream = urlresolver.resolve(stream)
        #     directory.resolve(stream)
        #
        # else:
        #
        #     stream = urlresolver.resolve(url)
        #     directory.resolve(stream, meta={'title': name})

    elif any(stream_link.sl_hosts(url)):

        stream = stream_link.sl_session(url)

        if stream == 30403:
            control.execute('Dialog.Close(all)')
            control.infoDialog(control.lang(30403))
        else:
            return stream

    elif urlresolver.HostedMediaFile(url).valid_url():

        stream = urlresolver.resolve(url)
        return stream

    elif 'antenna' in url and not '/live' in url.lower():
        return 'plugin://plugin.video.antenna.gr/?action=play&url={}'.format(url)
    elif 'alphatv' in url and not 'live' in url:
        return 'plugin://plugin.video.alphatv.gr/?action=play&url={}'.format(url)
    elif 'ert.gr' in url and not 'ipinfo-geo' in url and not 'ertworld2' in url:
        return 'plugin://plugin.video.ert.gr/?action=play&url={}'.format(url)
    elif 'skai.gr' in url and not 'tvlive' in url.lower():
        return 'plugin://plugin.video.skai.gr/?action=play&url={}'.format(url)

    elif '#youtu_translator' in url:

        remove_fragment = url.partition('#')[0]
        link = cache.get(youtu.traslate, 12, remove_fragment)
        stream = youtu.wrapper(link)
        return stream

    elif 'ant1iwo' in url:

        stream = cache.get(various.ant1cy, 12, url)

        return stream

    elif 'antenna.gr' in url:

        stream = cache.get(various.ant1gr, 12, url)

        return stream

    elif 'megatv.com.cy/live/' in url:

        stream = cache.get(various.megacy, 12, url)
        return stream

    elif 'webtv.ert.gr' in url:

        link = cache.get(various.ert, 12, url)

        return yt_router(link)

    elif 'skai.gr' in url:

        vid = cache.get(various.skai, 6, url)
        stream = youtu.wrapper(vid)
        return stream

    elif 'alphatv.gr/webtv/live' in url or 'alphacyprus.com.cy' in url:

        stream = cache.get(various.alphatv, 12, url)
        return stream

    elif 'euronews.com' in url:

        stream = cache.get(various.euronews, 12, url)
        return stream

    elif 'visionip.tv' in url:

        sid = cache.get(various.visioniptv, 12)
        stream = url + sid
        return stream

    elif 'ssh101.com/securelive/' in url:

        stream = cache.get(various.ssh101, 48, url)
        return stream

    elif '#dacast' in url:

        remove_fragment = url.partition('#')[0]
        stream = various.dacast(remove_fragment)
        return stream

    else:

        return url


def gm_source_maker(url):

    if 'episode' in url:

        html = client.request(url=url.partition('?')[0], post=url.partition('?')[2])
        links = client.parseDOM(html, 'a', ret='href')
        links = [urljoin(base_link, link) for link in links]
        hl = client.parseDOM(html, 'a')
        hosts = [host.replace('προβολή στο '.decode('utf-8'), control.lang(30015)) for host in hl]

        return 'episode', hosts, links

    elif 'view' in url:

        html = client.request(url)
        link = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})[0]

        return 'view', link

    elif 'music' in url:

        html = client.request(url)
        link = client.parseDOM(html, 'iframe', ret='src', attrs={"class": "embed-responsive-item"})[0]
        return 'music', link

    else:

        html = client.request(url)

        try:
            info = client.parseDOM(html, 'h4', attrs={'style': 'text-indent:10px;'})
            if ',' in info[1]:
                genre = info[1].lstrip('Είδος:'.decode('utf-8')).split(',')
                genre = random.choice(genre)
                genre = genre.strip()
            else:
                genre = info[1].lstrip('Είδος:'.decode('utf-8')).strip()
        except:
            genre = control.lang(30147)

        links = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})
        links = [urljoin(base_link, link) for link in links]
        hl = client.parseDOM(html, 'a', attrs={"class": "btn btn-primary"})

        hosts = [host.replace(
            'προβολή στο '.decode('utf-8'), control.lang(30015)
        ).replace(
            'προβολή σε '.decode('utf-8'), control.lang(30015)
        ) for host in hl]

        if 'text-align: justify' in html:
            plot = client.parseDOM(html, 'p', attrs={'style': 'text-align: justify'})[0]
        elif 'text-justify' in html:
            plot = client.parseDOM(html, 'p', attrs={'class': 'text-justify'})[0]
        else:
            plot = control.lang(30085)

        return 'movies', hosts, links, plot, genre


def gm_debris(link):

    html = client.request(urljoin(base_link, link))
    button = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})[0]
    return button


def playlist_maker(hl, sl, title, image):

    title = title.decode('utf-8')

    vids = [
        sysaddon + play_action + cache.get(gm_debris, 12, i) + '&image=' + image.decode('utf-8') + '&title=' + title for i in sl
    ]
    videos = zip(hl, vids)

    if control.setting('randomize_items') == 'true':
        random.shuffle(videos)
    play_list = [u'#EXTM3U\n'] + [u'#EXTINF:0,{0}\n'.format(title + u' - ' + h) + v + u'\n' for h, v in videos]
    m3u_playlist = u''.join(play_list)

    m3u_file = control.join(control.transPath('special://temp'), 'pl_action.m3u')
    with open(m3u_file, 'w') as f:
        f.write(m3u_playlist.encode('utf-8'))

    return m3u_file


def mini_picker(hl, sl, title, image):

    if len(hl) == 1:

        stream = cache.get(gm_debris, 12, sl[0])

        if control.setting('action_type') == '2':
            if control.setting('auto_play') == 'true':
                play_url = sysaddon + play_action + quote_plus(stream) + '&image=' + quote_plus(image) + '&title=' + quote_plus(title)
                control.execute('PlayMedia("{0}")'.format(play_url))
            else:
                m3u_file = playlist_maker(hl, sl, title, image)
                control.playlist.load(m3u_file)
                control.openPlaylist()
        else:
            control.infoDialog(hl[0])
            return stream

    elif control.setting('action_type') == '2':

        m3u_file = playlist_maker(hl, sl, title, image)

        control.playlist.load(m3u_file)

        if control.setting('auto_play') == 'true':
            control.execute('Action(Play)')
        else:
            control.openPlaylist()
        return

    else:

        choice = control.selectDialog(heading=control.lang(30064), list=hl)

        if choice <= len(sl) and not choice == -1:
            popped = sl[choice]
            return cache.get(gm_debris, 12, popped)
        else:
            return


def items_directory(url, title, description, genre):

    sources = cache.get(gm_source_maker, 6, url)

    lists = zip(sources[1], sources[2])

    items = []

    if description is None:
        try:
            description = sources[3]
        except IndexError:
            description = control.lang(30085)

    if genre is None:
        try:
            genre = sources[4]
        except IndexError:
            genre = control.lang(30147)

    try:
        description = description.decode('utf-8')
    except:
        description = description

    for h, l in lists:

        html = client.request(l)
        button = client.parseDOM(html, 'a', attrs={'role': 'button'}, ret='href')[0]
        image = client.parseDOM(html, 'img', attrs={'class': 'thumbnail img-responsive'}, ret='src')[0]
        image = urljoin(base_link, image.encode('utf-8'))
        name = client.parseDOM(html, 'h3')[0]
        year = re.findall('[ΈΕ]τος: ?(\d{4})', html, re.U)[0]
        plot = name + '\n' + control.lang(30090) + ': ' + year + '\n' + description

        data = dict(
            label=title.decode('utf-8') + ' - ' + h, title=title.decode('utf-8'), url=button, image=image, plot=plot, year=int(year), genre=genre, name=name
        )

        items.append(data)

    return items


def directory_picker(url, title, description, genre):

    items = cache.get(items_directory, 12, url, title, description, genre)

    if items is None:
        return

    for i in items:

        add_to_playlist = {'title': 30226, 'query': {'action': 'add_to_playlist'}}
        clear_playlist = {'title': 30227, 'query': {'action': 'clear_playlist'}}
        i.update({'cm': [add_to_playlist, clear_playlist], 'action': 'play', 'isFolder': 'False'})

    directory.add(items, content='movies')


def play_m3u(link, title, rename_titles=True, randomize=True):

    m3u_file = control.join(control.transPath('special://temp'), link.rpartition('/')[2])

    play_list = client.request(link)

    if rename_titles:
        videos = play_list.splitlines()[1:][1::2]
    else:
        videos = re.findall('#.+?$\n.+?$', play_list[1:], re.M)

    if randomize and control.setting('randomize_m3u') == 'true':
        random.shuffle(videos)

    if rename_titles:
        m3u_playlist = '#EXTM3U\n#EXTINF:0,{0}\n'.format(title) + '\n#EXTINF:0,{0}\n'.format(title).join(videos)
    else:
        m3u_playlist = '#EXTM3U\n' + '\n'.join(videos)

    with open(m3u_file, 'w') as f: f.write(m3u_playlist)

    control.playlist.load(m3u_file)
    control.execute('Action(Play)')


def player(url, title, image):

    log_debug('Attempting to play this url: ' + url)

    if url is None:
        log_debug('Nothing playable was found')
        return
    else:
        log_debug('Invoked player method')

    link = url.replace('&amp;', '&')

    if 'greek-movies.com' in link:

        sources = cache.get(gm_source_maker, 6, link)

        if any(['music' in sources[0], 'view' in sources[0]]):

            if control.setting('audio_only') == 'true' or control.condVisibility('Window.IsActive(music)') == 1:
                link = sources[1] + '#audio_only'
            else:
                link = sources[1]

            stream = youtu.wrapper(link)

            if len(stream) == 2:
                directory.resolve(stream[0], dash=stream[1])
            else:
                directory.resolve(stream)

        else:

            link = mini_picker(sources[1], sources[2], title, image)

            if link is None:
                control.execute('Dialog.Close(all)')
            else:
                stream = router(link)

                try:
                    if len(stream) == 2:
                        resolved = stream[0]
                        dash = stream[1]
                    else:
                        resolved = stream
                        dash = False
                except TypeError:
                    resolved = stream
                    dash = False

                try:
                    directory.resolve(resolved, meta={'plot': sources[3]}, dash=dash)
                except IndexError:
                    directory.resolve(resolved, dash=dash)
                except:
                    control.execute('Dialog.Close(all)')
                    control.infoDialog(control.lang(30112))

    else:

        stream = router(link)

        try:
            if len(stream) == 2:
                resolved = stream[0]
                dash = stream[1]
            else:
                resolved = stream
                dash = False
        except TypeError:
            resolved = stream
            dash = False

        try:

            if 'm3u8' in resolved and control.setting('m3u8_quality_picker') == '1' and not any(stream_link.sl_hosts(
                    resolved)
            ):

                resolved = m3u8_loader.m3u8_picker(resolved)

        except TypeError:

            pass

        if resolved == 30403:

            control.execute('Dialog.Close(all)')
            control.infoDialog(control.lang(30403))

        else:

            try:
                directory.resolve(resolved, meta={'title': title}, icon=image, dash=dash)
            except:
                control.execute('Dialog.Close(all)')
                control.infoDialog(control.lang(30112))
