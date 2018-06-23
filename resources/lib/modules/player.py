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
from urllib import quote

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
from resources.lib import params


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

    if 'youtu' in url:

        return yt_router(url)

    elif 'greek-movies.com' in url:

        sources = cache.get(gm_source_maker, 6, url)

        if any(['music' in sources[0], 'view' in sources[0]]):

            stream = youtu.wrapper(sources[1])

            return stream

        else:

            link = mini_picker(sources[1], sources[2])

            if link is None:
                control.execute('Dialog.Close(all)')
            else:
                stream = router(link)

                try:
                    return stream, sources[3]
                except IndexError:
                    return stream

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

        if '.m3u8' in link:
            return link
        else:
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
        hosts = [host.replace(u'προβολή στο ', control.lang(30015)) for host in hl]

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
                genre = info[1].lstrip(u'Είδος:').split(',')
                genre = random.choice(genre)
                genre = genre.strip()
            else:
                genre = info[1].lstrip(u'Είδος:').strip()
        except:
            genre = control.lang(30147)

        links = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})
        hl = client.parseDOM(html, 'a', attrs={"class": "btn btn-primary"})
        if not links or not hl:
            buttons = client.parseDOM(html, 'div', attrs={"class": "btn-group"})
            hl = [
                client.stripTags(
                    client.parseDOM(h, 'button', attrs={"type": "button"})[0]
                ).strip('"') + p for h in buttons for p in client.parseDOM(
                    h, 'a', attrs={'target': '_blank'}
                )
            ]
            links = [l for b in buttons for l in client.parseDOM(b, 'a', ret='href')]
        links = [urljoin(base_link, link) for link in links]

        hosts = [host.replace(
            u'προβολή στο ', control.lang(30015)
        ).replace(
            u'προβολή σε ', control.lang(30015)
        ).replace(
            u'μέρος ', ', ' + control.lang(30225)
        ) for host in hl]

        if 'text-align: justify' in html:
            plot = client.parseDOM(html, 'p', attrs={'style': 'text-align: justify'})[0]
        elif 'text-justify' in html:
            plot = client.parseDOM(html, 'p', attrs={'class': 'text-justify'})[0]
        else:
            plot = control.lang(30085)

        code = None
        imdb_code = re.search('imdb.+?/title/([\w]+?)/', html)
        if imdb_code:
            code = imdb_code.group(1)

        return 'movies', hosts, links, plot, genre, code


def gm_debris(link):

    html = client.request(urljoin(base_link, link))
    button = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})[0]
    return button


def playlist_maker(hl, sl, title, image):

    vids = [
        sysaddon + play_action + cache.get(gm_debris, 12, i) + '&image=' + quote(image) + '&title=' + quote(title)
        for i in sl
    ]
    videos = zip(hl, vids)

    if control.setting('randomize_items') == 'true':
        random.shuffle(videos)
    play_list = [u'#EXTM3U\n'] + [u'#EXTINF:0,{0}\n'.format(title.decode('utf-8') + u' - ' + h) + v + u'\n' for h, v in videos]
    m3u_playlist = u''.join(play_list)

    m3u_file = control.join(control.transPath('special://temp'), 'pl_action.m3u')
    with open(m3u_file, 'w') as f:
        f.write(m3u_playlist.encode('utf-8'))

    return m3u_file


def mini_picker(hl, sl):

    image = params.get('image').encode('latin-1')
    title = params.get('title').encode('latin-1')

    if len(hl) == 1:

        stream = cache.get(gm_debris, 12, sl[0])

        if control.setting('action_type') == '2':
            if control.setting('auto_play') == 'true':
                play_url = sysaddon + play_action + quote(stream) + '&image=' + quote(image) + '&title=' + quote(title)
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


def items_directory(url):

    sources = cache.get(gm_source_maker, 6, url)

    lists = zip(sources[1], sources[2])

    items = []

    try:
        description = sources[3]
    except IndexError:
        description = params.get('plot').encode('latin-1')
        if not description:
            description = control.lang(30085)

    try:
        genre = sources[4]
    except IndexError:
        genre = control.lang(30147)

    for h, l in lists:

        html = client.request(l)
        button = client.parseDOM(html, 'a', attrs={'role': 'button'}, ret='href')[0]
        image = client.parseDOM(html, 'img', attrs={'class': 'thumbnail img-responsive'}, ret='src')[0]
        image = urljoin(base_link, image)
        title = client.parseDOM(html, 'h3')[0]
        year = [y[-4:] for y in client.parseDOM(html, 'h4') if str(y[-4:]).isdigit()][0]
        try:
            episode = client.stripTags(client.parseDOM(html, 'h4')[-1])
            episode = episode.partition(': ')[2]
            label = title + ' - ' + episode + ' - ' + h
            title = title + ' - ' + episode
        except IndexError:
            label = title + ' - ' + h
        plot = title + '\n' + control.lang(30090) + ': ' + year + '\n' + description

        data = dict(
            label=label, title=title + ' ({})'.format(year), url=button, image=image, plot=plot,
            year=int(year), genre=genre, name=title
        )

        items.append(data)

    return items


def directory_picker(url):

    # items = cache.get(items_directory, 12, url)
    items = items_directory(url)

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


def player(url):

    if url is None:
        log_debug('Nothing playable was found')
        return
    else:
        log_debug('Invoked player method')

    link = url.replace('&amp;', '&')

    log_debug('Attempting to play this url: ' + link)

    stream = router(link)

    if stream is None:
        log_debug('Failed to resolve this url: ' + link)
        control.execute('Dialog.Close(all)')
        return

    plot = None

    try:

        if len(stream) == 2:
            resolved = stream[0]
            plot = stream[1]
        else:
            resolved = stream
            try:
                plot = params.get('plot').encode('latin-1')
                if not plot:
                    raise BaseException
            except BaseException:
                pass

    except TypeError:

        resolved = stream

    else:

        log_debug('Plot obtained')

    finally:

        log_debug('Stream has been resolved: ' + link)

    try:

        bool_m3u8_quality_picker = control.setting('m3u8_quality_picker') == '1'

        if 'm3u8' in resolved and bool_m3u8_quality_picker and not any(stream_link.sl_hosts(resolved)):

            resolved = m3u8_loader.m3u8_picker(resolved)

    except TypeError:

        pass

    try:
        addon_enabled = control.addon_details('inputstream.adaptive').get('enabled')
    except KeyError:
        addon_enabled = False

    mpeg_dash_on = control.setting('mpeg_dash') == 'true' and addon_enabled

    dash = ('.mpd' in resolved or 'dash' in resolved or '.ism' in resolved or '.hls' in resolved) and mpeg_dash_on

    if dash:

        if '.hls' in resolved:
            manifest_type = 'hls'
        elif '.ism' in resolved:
            manifest_type = 'ism'
        else:
            manifest_type = 'mpd'

        log_debug('Activating MPEG-DASH for this url: ' + resolved)

    else: manifest_type = ''

    image = params.get('image').encode('latin-1')
    title = params.get('title').encode('latin-1')

    meta = {'title': title}
    if plot:
        meta.update({'plot': plot})

    if resolved == 30403:

        control.execute('Dialog.Close(all)')
        control.infoDialog(control.lang(30403))

    else:

        try:
            directory.resolve(resolved, meta=meta, icon=image, dash=dash, manifest_type=manifest_type)
        except:
            control.execute('Dialog.Close(all)')
            control.infoDialog(control.lang(30112))
