# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''
from __future__ import absolute_import, unicode_literals

import re

from tulip.compat import urljoin, parse_qsl, OrderedDict, zip, urlsplit, urlparse, urlencode

try:
    from resolveurl import resolve as resolve_url
    from resolveurl.hmf import HostedMediaFile
except Exception:
    resolve_url = None
    HostedMediaFile = None

from random import shuffle, choice as random_choice
from tulip import directory, client, cache, control, youtube as tulip_youtube
from tulip.parsers import itertags_wrapper
from tulip.log import log_debug

from ..indexers.gm import MOVIES, SHORTFILMS, THEATER, GM_BASE, blacklister, source_maker, Indexer as gm_indexer
from ..indexers.kids import BASE_LINK_GK
from ..resolvers import various, youtube, stream_link
from .kodi import prevent_failure
from .constants import YT_URL, API_KEYS, CACHE_DEBUG
from .helpers import m3u8_picker, thgiliwt
from youtube_plugin.youtube.youtube_exceptions import YouTubeException


skip_directory = False
SEPARATOR = ' - ' if control.setting('wrap_labels') == '1' else '[CR]'


def conditionals(url):

    def yt(uri):

        if uri.startswith('plugin://'):
            return uri

        if len(uri) == 11:

            uri = YT_URL + uri

        try:
            return youtube.wrapper(uri)
        except YouTubeException as exp:
            log_debug('Youtube resolver failure, reason: ' + repr(exp))
            return

    if 'youtu' in url:

        log_debug('Resolved with youtube addon')

        return yt(url)

    elif 'greek-movies.com' in url:

        if CACHE_DEBUG:
            sources = source_maker(url)
        else:
            sources = cache.get(source_maker, 6, url)

        if sources is None:
            return

        link = mini_picker(sources['hosts'], sources['links'])

        if link is None:
            control.execute('Dialog.Close(all)')
        else:
            stream = conditionals(link)
            return stream

    elif BASE_LINK_GK in url:

        if CACHE_DEBUG:
            sources = gk_debris(url)
        else:
            sources = cache.get(gk_debris, 48, url)

        link = mini_picker(sources['hosts'], sources['links'])

        return conditionals(link)

    elif url.startswith('iptv://'):

        if CACHE_DEBUG:
            stream = various.iptv(urlsplit(url).netloc)
        else:
            stream = cache.get(various.iptv, 2, urlsplit(url).netloc)

        return stream

    elif stream_link.StreamLink(url).hosts:

        stream = stream_link.StreamLink(url).passthrough()

        log_debug('Attempting to resolve with streamlink')

        return stream

    elif HostedMediaFile is not None and HostedMediaFile(url).valid_url():

        if control.setting('show_alt_vod') == 'true':

            stream = resolve_url(url)

            log_debug('Attempting to resolve with resolveurl')

            return stream

        else:

            control.infoDialog(control.lang(30354), time=5000)
            return 'https://static.adman.gr/inpage/blank.mp4'

    elif 'periscope' in url and 'search' in url:

        if CACHE_DEBUG:
            stream = stream_link.StreamLink(various.periscope_search(url)).passthrough()
        else:
            stream = stream_link.StreamLink(cache.get(various.periscope_search, 6, url)).passthrough()

        return stream

    elif 'rise.gr' in url:

        if CACHE_DEBUG:
            link = various.risegr(url)
        else:
            link = cache.get(various.risegr, 24, url)

        stream = stream_link.StreamLink(link).passthrough()

        log_debug('Attempting to resolve with streamlink')

        return stream

    else:

        return url


def gm_debris(link):

    html = client.request(urljoin(GM_BASE, link))
    button = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})[0]

    return button


def gk_debris(link):

    html = client.request(link)
    sources = client.parseDOM(html, 'iframe', ret='src', attrs={"class": "metaframe rptss"})
    movie_data = client.parseDOM(html, 'div', {'class': 'data'})[0]
    title = client.parseDOM(movie_data, 'h1')[0]
    year = client.parseDOM(movie_data, 'span', attrs={'class': 'date'})[0][-4:]
    image = itertags_wrapper(html, 'img', {'alt': title.encode('utf-8')}, ret='src')[0]
    hosts = ['- '.join([control.lang(30015), urlparse(s).netloc]) for s in sources]
    duration = client.parseDOM(movie_data, 'span', {'class': 'runtime'})[0]
    duration = re.search(r'(\d{2,3})', duration).group(1)

    data = {
        'links': sources, 'hosts': hosts, 'title': title, 'year': int(year), 'image': image,
        'duration': int(duration) * 60
    }

    return data


def mini_picker(hl, sl):

    if len(hl) == 1 and len(sl) == 1:

        if 'greek-movies.com' in sl[0]:
            if CACHE_DEBUG:
                stream = gm_debris(sl[0])
            else:
                stream = cache.get(gm_debris, 9600, sl[0])
        else:
            stream = sl[0]

        if 'AliveGR' not in control.infoLabel('ListItem.Label') and control.setting('host_notify') == 'true':
            control.infoDialog(hl[0])

        return stream

    else:

        if control.setting('action_type') == '3' or skip_directory:

            url = random_choice(sl)
            idx = sl.index(url)

            if control.setting('action_type') == '3' and 'AliveGR' not in control.infoLabel('ListItem.Label') and control.setting('host_notify') == 'true':

                control.infoDialog(hl[idx])

            if 'greek-movies.com' in sl[idx]:

                if CACHE_DEBUG:
                    return gm_debris(url)
                else:
                    return cache.get(gm_debris, 9600, url)

            else:

                return url

        choice = control.selectDialog(heading=control.lang(30064), list=hl)

        if choice <= len(sl) and not choice == -1:

            popped = sl[choice]

            if 'greek-movies.com' in popped:
                if CACHE_DEBUG:
                    return gm_debris(popped)
                else:
                    return cache.get(gm_debris, 9600, popped)
            else:
                return popped

        else:

            prevent_failure()


def gm_filler(url, params):

    if CACHE_DEBUG:
        sources = source_maker(url)
    else:
        sources = cache.get(source_maker, 6, url)

    lists = list(zip(sources['hosts'], sources['links']))

    items = []

    try:
        description = sources['plot']
    except KeyError:
        try:
            description = params.get('plot').encode('latin-1')
        except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
            description = params.get('plot')
        if not description:
            description = control.lang(30085)

    try:
        genre = sources['genre']
    except KeyError:
        genre = control.lang(30147)

    for h, l in lists:

        html = client.request(l)
        button = client.parseDOM(html, 'a', attrs={'role': 'button'}, ret='href')[0]
        image = client.parseDOM(html, 'img', attrs={'class': 'thumbnail img-responsive'}, ret='src')[0]
        image = urljoin(GM_BASE, image)
        title = client.parseDOM(html, 'h3')[0]
        year = [y[-4:] for y in client.parseDOM(html, 'h4') if str(y[-4:]).isdigit()][0]
        try:
            episode = client.stripTags(client.parseDOM(html, 'h4')[-1])
            if episode[-4:].isdigit():
                raise IndexError
            episode = episode.partition(': ')[2]
            label = title + ' - ' + episode + SEPARATOR + h
            title = title + ' - ' + episode
        except IndexError:
            label = title + SEPARATOR + h
        # plot = title + '[CR]' + control.lang(30090) + ': ' + year + '[CR]' + description

        data = {
            'label': label, 'title': title + ' ({})'.format(year), 'url': button, 'image': image, 'plot': description,
            'year': int(year), 'genre': genre, 'name': title
        }

        items.append(data)

    return items


def gk_filler(url):

    items = []

    if CACHE_DEBUG:
        sources = gk_debris(url)
    else:
        sources = cache.get(gk_debris, 6, url)

    lists = list(
        zip(
            sources['hosts'], sources['links']
        )
    )

    t = sources['title']
    y = sources['year']
    i = sources['image']
    d= sources['duration']

    for h, l in lists:

        label = SEPARATOR.join([t, h])

        data = {
            'label': label, 'title': '{0} ({1})'.format(t, y), 'url': l, 'image': i, 'year': y, 'duration': d
        }

        items.append(data)

    return items


def items_directory(url, params):

    if 'greek-movies.com' in url:

        return gm_filler(url, params)

    else:

        return gk_filler(url)


def directory_picker(url, argv):

    params = dict(parse_qsl(argv[2][1:]))

    if CACHE_DEBUG:
        items = items_directory(url, params)
    else:
        items = cache.get(items_directory, 12, url, params)

    if items is None:
        return

    for i in items:

        add_to_playlist = {'title': 30226, 'query': {'action': 'add_to_playlist'}}
        clear_playlist = {'title': 30227, 'query': {'action': 'clear_playlist'}}
        i.update({'cm': [add_to_playlist, clear_playlist], 'action': 'play', 'isFolder': 'False'})

    directory.add(
        items, content='movies', argv=argv, as_playlist=control.setting('action_type') == '2',
        auto_play=control.setting('auto_play') == 'true'
    )

    prevent_failure()


def dash_conditionals(stream):

    try:

        inputstream_adaptive = control.addon_details('inputstream.adaptive').get('enabled')

    except KeyError:

        inputstream_adaptive = False

    m3u8_dash = ('.hls' in stream or '.m3u8' in stream) and control.setting('m3u8_quality_picker') == '2'

    dash = ('.mpd' in stream or 'dash' in stream or '.ism' in stream or m3u8_dash) and inputstream_adaptive

    mimetype = None
    manifest_type = None

    if dash:

        if '.hls' in stream or '.m3u8' in stream:
            manifest_type = 'hls'
            mimetype = 'application/vnd.apple.mpegurl'
        elif '.ism' in stream:
            manifest_type = 'ism'
        else:
            manifest_type = 'mpd'

        log_debug('Activating adaptive parameters for this url: ' + stream)

    return dash, m3u8_dash, mimetype, manifest_type


def pseudo_live(url):

    _url = url

    if 'youtube' in url:
        url = url.rpartition('/')[2]
    elif url.endswith('fifties'):
        url = '{0}movies.php?y=7&l=&g=&p='.format(GM_BASE)
    elif url.endswith('sixties'):
        url = '{0}movies.php?y=6&l=&g=&p='.format(GM_BASE)
    elif url.endswith('seventies'):
        url = '{0}movies.php?y=5&l=&g=&p='.format(GM_BASE)
    elif url.endswith('eighties'):
        url = '{0}movies.php?y=4&l=&g=&p='.format(GM_BASE)
    else:
        url = '{0}movies.php?g=8&y=&l=&p='.format(GM_BASE)

    if 'channel' in _url:
        movie_list = tulip_youtube.youtube(key=thgiliwt(API_KEYS['api_key']), replace_url=False).videos(url, limit=10)
    elif 'playlist' in _url:
        movie_list = tulip_youtube.youtube(key=thgiliwt(API_KEYS['api_key']), replace_url=False).playlist(url, limit=10)
    else:
        movie_list = gm_indexer().listing(url, get_listing=True)

    if 'youtube' in _url:
        movie_list = [i for i in movie_list if i['duration'] >= 240]

    if not _url.endswith('kids') and 'youtube' not in _url:

        if CACHE_DEBUG:
            bl_urls = blacklister()
        else:
            bl_urls = cache.get(blacklister, 96)

        movie_list = [i for i in movie_list if i['url'] not in bl_urls]

    for i in movie_list:
        i.update({'action': 'play_skipped', 'isFolder': 'False'})

    plot = None

    if control.setting('pseudo_live_mode') == '0':

        choice = random_choice(movie_list)

        meta = {'title': choice['title'], 'image': choice['image']}

        if 'youtube' not in _url:
            if CACHE_DEBUG:
                plot = source_maker(choice['url']).get('plot')
            else:
                plot = cache.get(source_maker, 6, choice['url']).get('plot')

        if plot:
            meta.update({'plot': plot})

        player(choice['url'], meta)

    else:

        shuffle(movie_list)

        directory.add(movie_list, as_playlist=True, auto_play=True)


def player(url, params):

    global skip_directory

    if url is None:
        log_debug('Nothing playable was found')
        return

    if url.startswith('alivegr://'):
        pseudo_live(url)
        return

    url = url.replace('&amp;', '&')
    skip_directory = params.get('action') == 'play_skipped'

    directory_boolean = MOVIES in url or SHORTFILMS in url or THEATER in url or BASE_LINK_GK in url or (
        'episode' in url and GM_BASE in url
    )

    if directory_boolean and control.setting('action_type') == '1' and not skip_directory:
        directory.run_builtin(action='directory', url=url)
        return

    log_debug('Attempting to play this url: ' + url)

    if params.get('action') == 'play_resolved':
        stream = url
    else:
        stream = conditionals(url)

    if not stream:

        log_debug('Failed to resolve this url: {0}'.format(url))

        return control.execute('Dialog.Close(all)')

    try:
        plot = params.get('plot').encode('latin-1')
    except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
        plot = params.get('plot')

    if not plot and 'greek-movies.com' in url:
        if CACHE_DEBUG:
            plot = source_maker(url).get('plot')
        else:
            plot = cache.get(source_maker, 6, url).get('plot')

    if isinstance(stream, OrderedDict):

        stream = stream_link.stream_processor(stream)

        dash, m3u8_dash, mimetype, manifest_type = dash_conditionals(stream)

    else:

        dash, m3u8_dash, mimetype, manifest_type = dash_conditionals(stream)

        if not m3u8_dash and control.setting('m3u8_quality_picker') == '1' and '.m3u8' in stream:

            try:

                stream = m3u8_picker(stream)

            except TypeError:

                pass

    if stream != url:

        log_debug('Stream has been resolved: ' + stream)

    else:

        log_debug('Attempting direct playback: ' + stream)

    # process headers if necessary:
    if '|' in stream:

        stream, sep, headers = stream.rpartition('|')

        headers = dict(parse_qsl(headers))

        log_debug('Appending custom headers: ' + repr(headers))

        stream = sep.join([stream, urlencode(headers)])

    try:

        image = params.get('image').encode('latin-1')
        title = params.get('title').encode('latin-1')

    except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):

        image = params.get('image')
        title = params.get('title')

    meta = {'title': title}

    if plot:

        meta.update({'plot': plot})

    try:

        directory.resolve(stream, meta=meta, icon=image, dash=dash, manifest_type=manifest_type, mimetype=mimetype)

    except:

        control.execute('Dialog.Close(all)')
        control.infoDialog(control.lang(30112))
