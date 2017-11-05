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

import urlresolver #, YDStreamExtractor
import random, re
from urlparse import urljoin

from tulip import directory, control, client, cache
from tulip.log import *

from ..indexers.gm import base_link
from tulip.init import sysaddon, syshandle
from ..resolvers import live, m3u8_loader, stream_link, yt_wrapper  # ytdl_wrapper
from ..modules.helpers import thgiliwt, stream_picker
from ..modules.tools import api_keys


def wrapper(url):

    # if urlresolver.HostedMediaFile(url).valid_url():
    #     stream = urlresolver.resolve(url)
    #     return stream

    if 'antenna' in url and not 'live_1' in url:
        return 'plugin://plugin.video.antenna.gr/?action=play&url={}'.format(url)
    elif 'alphatv' in url and not 'live' in url:
        return 'plugin://plugin.video.alphatv.gr/?action=play&url={}'.format(url)
    elif 'ert.gr' in url and not 'ipinfo-geo' in url and not 'ertworld2' in url:
        return 'plugin://plugin.video.ert.gr/?action=play&url={}'.format(url)
    elif 'skai.gr' in url and not 'TVLive' in url:
        return 'plugin://plugin.video.skai.gr/?action=play&url={}'.format(url)

    elif 'ant1iwo' in url:

        link = client.replaceHTMLCodes(url)
        stream = cache.get(live.ant1cy, 12, link)

        return stream

    elif 'megatv.com.cy/live/' in url:

        stream = cache.get(live.megacy, 12, url)
        return stream

    elif 'megatv.com/webtv/' in url:

        link = client.replaceHTMLCodes(url)
        link = cache.get(live.megagr, 24, link)
        stream = urlresolver.resolve(link)
        return stream

    elif 'webtv.ert.gr' in url:

        link = cache.get(live.ert, 12, url)
        stream = urlresolver.resolve(link)
        return stream

    elif 'skai.gr/ajax.aspx' in url:

        link = client.replaceHTMLCodes(url)
        link = cache.get(live.skai, 6, link)
        stream = urlresolver.resolve(link)
        return stream

    elif 'alphatv.gr/webtv/live' in url or 'alphacyprus.com.cy' in url:

        stream = cache.get(live.alphatv, 12, url)
        return stream

    elif 'euronews.com' in url:

        stream = cache.get(live.euronews, 12, url)
        return stream

    elif 'fnetwork.com' in url:

        stream = cache.get(live.fnetwork, 12, url)
        stream = urlresolver.resolve(stream)
        return stream

    elif 'visionip.tv' in url:

        sid = cache.get(live.visioniptv, 12)
        stream = url + sid
        return stream

    elif 'ssh101.com/securelive/' in url:

        stream = cache.get(live.ssh101, 48, url)
        return stream

    # elif 'rythmosfm.gr' in url:
    #
    #     stream = url + client.spoofer(referer=True, ref_str='https://www.rythmosfm.gr/community/top20/')
    #     return stream

    else:
        return url


def source_maker(url):

    if 'episode' in url:  # series & shows

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

    else:  # movies

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


def dialog_picker(hl, sl):

    if len(hl) > 1:

        choice = control.selectDialog(heading=control.lang(30064), list=hl)

        if choice <= len(sl) and not choice == -1:
            popped = sl.pop(choice)
            html = client.request(urljoin(base_link, popped))
            button = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})[0]
            return button
        else:
            return

    else:

        html = client.request(urljoin(base_link, sl[0]))
        button = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})[0]
        control.infoDialog(hl[0])
        return button


def items_directory(url, title, description, genre):

    sources = cache.get(source_maker, 6, url)

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
            title=title.decode('utf-8') + ' - ' + h, url=button, image=image, plot=plot, year=int(year), genre=genre, name=name
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


def player(url, name):

    if url is None:
        log_error('Nothing playable was found')
        return
    else:
        log_notice('Invoked player method')

    result = url.replace('&amp;', '&')
    conditions = ['ustream' in result, 'dailymotion' in result, 'twitch' in result, 'facebook' in result]

    if 'youtu' in result:

        stream = yt_wrapper.wrapper(result)
        directory.resolve(stream[0], dash=stream[1])

        # Alternative method reserved:
        # if 'user' in result or 'channel' in result:
        #
        #     from ..resolvers import yt_wrapper
        #     stream = yt_wrapper.traslate(result, add_base=True)
        #     stream = urlresolver.resolve(stream)
        #     directory.resolve(stream)
        #
        # else:
        #
        #     stream = urlresolver.resolve(result)
        #     directory.resolve(stream, meta={'title': name})

    # if any(conditions) and YDStreamExtractor.mightHaveVideo(result):
    #
    #     stream = ytdl_wrapper.ytdl_session(result)
    #
    #     directory.resolve(stream)

    elif any(conditions):

        stream = stream_link.sl_session(result)

        if stream == 30403:
            control.execute('Dialog.Close(all)')
            control.infoDialog(control.lang(30403))
        else:
            directory.resolve(stream)

    elif urlresolver.HostedMediaFile(result).valid_url() and not 'youtu' in result:

        stream = urlresolver.resolve(result)
        directory.resolve(stream, meta={'title': name})

    elif 'greek-movies.com' in result:

        sources = cache.get(source_maker, 6, result)

        if any(['music' in sources[0], 'view' in sources[0]]):

            print type(control.condVisibility('Window.IsActive(music)'))

            if control.setting('audio_only') == 'true' or control.condVisibility('Window.IsActive(music)') == 1:
                link = sources[1] + '#audio_only'
            else:
                link = sources[1]

            stream = yt_wrapper.wrapper(link)
            directory.resolve(stream)

        else:

            link = dialog_picker(sources[1], sources[2])
            if link is None:
                control.execute('Dialog.Close(all)')
            else:
                stream = wrapper(link)
                try:
                    directory.resolve(stream, meta={'plot': sources[3]})
                except IndexError:
                    directory.resolve(stream)

    else:

        stream = wrapper(result)

        if 'm3u8' in stream and control.setting('m3u8_quality_picker') == '1':

            stream = m3u8_loader.m3u8_picker(stream)

        if stream == 30403:

            control.execute('Dialog.Close(all)')
            control.infoDialog(control.lang(30403))

        else:

            try:
                directory.resolve(stream, meta={'title': name})
            except:
                control.execute('Dialog.Close(all)')
                control.infoDialog(control.lang(30112))
