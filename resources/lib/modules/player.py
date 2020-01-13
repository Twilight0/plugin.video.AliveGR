# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

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
from __future__ import absolute_import, unicode_literals

import random
import re
import json
# import YDStreamExtractor
from tulip.compat import urljoin, parse_qsl, OrderedDict, urlencode, zip

try:
    from resolveurl import resolve as resolve_url
    from resolveurl.hmf import HostedMediaFile
except Exception:
    resolve_url = None
    HostedMediaFile = None

from tulip import directory, client, cache, control
from tulip.log import log_debug

from ..indexers.gm import GM_BASE
from ..resolvers import various, youtube, sl
from .constants import YT_URL
from .helpers import stream_picker, m3u8_picker
from .kodi import addon_version
from youtube_plugin.youtube.youtube_exceptions import YouTubeException


def conditionals(url):

    def yt_conditional(uri):

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

        return yt_conditional(url)

    elif 'greek-movies.com' in url:

        sources = cache.get(gm_source_maker, 6, url)

        link = mini_picker(sources['hosts'], sources['links'])

        if link is None:
            control.execute('Dialog.Close(all)')
        else:
            stream = conditionals(link)

            if 'plot' in sources:
                return stream, sources['plot']
            else:
                return stream

    elif 'gamatokid.com/movies/' in url:

        source = cache.get(gk_debris, 24, url)

        return conditionals(source)

    elif sl.StreamLink(url).hosts:

        stream = sl.StreamLink(url).wrapper()

        log_debug('Resolved with streamlink')

        return stream

    elif HostedMediaFile is not None and HostedMediaFile(url).valid_url() and control.setting('show_alt_vod') == 'true':

        stream = resolve_url(url)

        log_debug('Resolved with resolveurl')

        return stream

    elif 'webtv.ert.gr' in url and 'live' in url:

        link = cache.get(various.ert, 12, url)

        if isinstance(link, list):
            try:
                stream = yt_conditional(link[0])
                if not stream:
                    raise YouTubeException
            except YouTubeException:
                return yt_conditional(link[1])
        else:
            return link

    elif 'skaitv.gr' in url and 'episode' not in url:

        vid = cache.get(various.skai, 3, url)
        stream = youtube.wrapper(vid)
        return stream

    elif 'periscope' in url and 'search' in url:

        stream = sl.wrapper(cache.get(various.periscope_search, 6, url))

        return stream

    elif 'rise.gr' in url:

        link = cache.get(various.risegr, 24, url)

        stream = sl.wrapper(link)

        return stream

    else:

        return url


def gm_source_maker(url):

    if 'episode' in url:

        html = client.request(url=url.partition('?')[0], post=url.partition('?')[2])
    
    else:

        html = client.request(url)

    try:

        html = html.decode('utf-8')
    
    except Exception:

        pass

    if 'episode' in url:

        episodes = re.findall('''(?:<a.+?/a>|<p.+?/p>)''', html)

        hl = []
        links = []

        for episode in episodes:

            if '<p style="margin-top:0px; margin-bottom:4px;">' in episode:

                host = client.parseDOM(episode, 'p')[0].split('<')[0]

                pts = client.parseDOM(episode, 'a')
                lks = client.parseDOM(episode, 'a', ret='href')

                for p in pts:
                    hl.append(u''.join([host, control.lang(30225), p]))

                for l in lks:
                    links.append(l)

            else:

                pts = client.parseDOM(episode, 'a')
                lks = client.parseDOM(episode, 'a', ret='href')

                for p in pts:
                    hl.append(p)

                for l in lks:
                    links.append(l)

        links = [urljoin(GM_BASE, link) for link in links]
        hosts = [host.replace(u'προβολή στο ', control.lang(30015)) for host in hl]

        data = {'links': links, 'hosts': hosts}

        if '<p class="text-muted text-justify">' in html:
            plot = client.parseDOM(html, 'p')[0]
            data.update({'plot': plot})

        return data

    elif 'view' in url:

        link = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})[0]

        return {'links': [link], 'hosts': [''.join([control.lang(30015), 'Youtube'])]}

    elif 'music' in url:

        link = client.parseDOM(html, 'iframe', ret='src', attrs={"class": "embed-responsive-item"})[0]

        return {'links': [link], 'hosts': [''.join([control.lang(30015), 'Youtube'])]}

    else:

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

        buttons = client.parseDOM(html, 'div', attrs={"style": "margin: 0px 0px 10px 10px;"})

        links = []
        hl = []

        for button in buttons:

            if '<ul class="dropdown-menu pull-right">' in button:

                h = client.stripTags(client.parseDOM(button, 'button')).strip()
                parts = client.parseDOM(button, 'li')

                for part in parts:

                    p = client.parseDOM(part, 'a')[0]
                    link = client.parseDOM(part, 'a', ret='href')[0]
                    hl.append(', '.join([h, p]))
                    links.append(link)

            else:

                h = client.parseDOM(button, 'a')[0]
                link = client.parseDOM(button, 'a', ret='href')[0]

                hl.append(h)
                links.append(link)

        links = [urljoin(GM_BASE, link) for link in links]

        hosts = [host.replace(
            u'προβολή στο ', control.lang(30015)
        ).replace(
            u'προβολή σε ', control.lang(30015)
        ).replace(
            u'μέρος ', ', ' + control.lang(30225)
        ) for host in hl]

        data = {'links': links, 'hosts': hosts, 'genre': genre}

        if 'text-align: justify' in html:
            plot = client.parseDOM(html, 'p', attrs={'style': 'text-align: justify'})[0]
        elif 'text-justify' in html:
            plot = client.parseDOM(html, 'p', attrs={'class': 'text-justify'})[0]
        else:
            plot = control.lang(30085)

        data.update({'plot': plot})

        imdb_code = re.search(r'imdb.+?/title/([\w]+?)/', html)
        if imdb_code:
            code = imdb_code.group(1)
            data.update({'code': code})

        return data


def gm_debris(link):

    html = client.request(urljoin(GM_BASE, link))
    button = client.parseDOM(html, 'a', ret='href', attrs={"class": "btn btn-primary"})[0]
    return button


def gk_debris(link):

    html = client.request(link)
    source = client.parseDOM(html, 'iframe', ret='src', attrs={"class": "metaframe rptss"})[0]
    return source


def mini_picker(hl, sl):

    if len(hl) == 1:

        stream = cache.get(gm_debris, 12, sl[0])

        control.infoDialog(hl[0])
        return stream

    else:

        choice = control.selectDialog(heading=control.lang(30064), list=hl)

        if choice <= len(sl) and not choice == -1:
            popped = sl[choice]
            return cache.get(gm_debris, 12, popped)
        else:
            return


def items_directory(url, params):

    sources = cache.get(gm_source_maker, 6, url)

    lists = list(zip(sources[1], sources[2]))

    items = []

    try:
        description = sources[3]
    except IndexError:
        try:
            description = params.get('plot').encode('latin-1')
        except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
            description = params.get('plot')
        if not description:
            description = control.lang(30085)

    try:
        genre = sources[4]
    except IndexError:
        genre = control.lang(30147)

    separator = ' - ' if control.setting('wrap_labels') == '1' else '[CR]'

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
            label = title + ' - ' + episode + separator + h
            title = title + ' - ' + episode
        except IndexError:
            label = title + separator + h
        # plot = title + '[CR]' + control.lang(30090) + ': ' + year + '[CR]' + description

        data = dict(
            label=label, title=title + ' ({})'.format(year), url=button, image=image, plot=description,
            year=int(year), genre=genre, name=title
        )

        items.append(data)

    return items


def directory_picker(url, argv):

    params = dict(parse_qsl(argv[2].replace('?', '')))

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


def dash_conditionals(stream):

    try:

        inputstream_adaptive = control.addon_details('inputstream.adaptive').get('enabled')

    except KeyError:

        inputstream_adaptive = False

    m3u8_dash = ('.hls' in stream or '.m3u8' in stream) and control.setting('m3u8_quality_picker') == '2' and addon_version('xbmc.python') >= 2260 and not 'dailymotion.com' in stream

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


def player(url, params, do_not_resolve=False):

    if url is None:
        log_debug('Nothing playable was found')
        return

    url = url.replace('&amp;', '&')

    log_debug('Attempting to play this url: ' + url)

    if do_not_resolve:
        stream = url
    else:
        stream = conditionals(url)

    if not stream or (len(stream) == 2 and not stream[0]):

        log_debug('Failed to resolve this url: {0}'.format(url))
        control.execute('Dialog.Close(all)')

        return

    plot = None

    try:

        if isinstance(stream, tuple):

            plot = stream[1]
            stream = stream[0]

        else:

            try:
                plot = params.get('plot').encode('latin-1')
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                plot = params.get('plot')

    except TypeError:

        pass

    else:

        log_debug('Plot obtained')

    dash, m3u8_dash, mimetype, manifest_type = dash_conditionals(stream)

    if not m3u8_dash and control.setting('m3u8_quality_picker') == '1' and '.m3u8' in stream:

        try:

            stream = m3u8_picker(stream)

        except TypeError:

            pass

    if isinstance(stream, OrderedDict):

        try:

            try:
                args = stream['best'].args
            except Exception:
                args = None

            try:
                json_dict = json.loads(stream['best'].json)
            except Exception:
                json_dict = None

            for h in args, json_dict:

                try:
                    if 'headers' in h:
                        headers = h['headers']
                        break
                    else:
                        headers = None
                except Exception:
                    headers = None

            if headers:

                try:
                    del headers['Connection']
                    del headers['Accept-Encoding']
                    del headers['Accept']
                except KeyError:
                    pass

                append = ''.join(['|', urlencode(headers)])

            else:

                append = ''

        except AttributeError:

            append = ''

        if control.setting('sl_quality_picker') == '0' or len(stream) == 3:

            stream = stream['best'].to_url() + append

        else:

            keys = list(stream.keys())[::-1]
            values = [u.to_url() + append for u in list(stream.values())][::-1]

            stream = stream_picker(keys, values)

        dash, m3u8_dash, mimetype, manifest_type = dash_conditionals(stream)

    if stream != url:

        log_debug('Stream has been resolved: ' + stream)

    if '|' in stream or '|' in url:

        from tulip.compat import parse_qsl

        log_debug('Appending custom headers: ' + repr(dict(parse_qsl(stream.rpartition('|')[2]))))

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
