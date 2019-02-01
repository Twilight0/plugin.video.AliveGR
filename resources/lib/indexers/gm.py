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

import re
import json
from ast import literal_eval as evaluate
from base64 import b64decode

from tulip import cache, client, directory, control
from tulip.log import log_debug
from tulip.compat import urljoin, urlparse, range, iteritems
from resources.lib.modules.themes import iconname
from resources.lib.modules.constants import sdik, bl
from resources.lib.modules.helpers import thgiliwt, dexteni
from tulip.init import syshandle, sysaddon

base_link = 'http://greek-movies.com/'
movies_link = urljoin(base_link, 'movies.php')
shows_link = urljoin(base_link, 'shows.php')
series_link = urljoin(base_link, 'series.php')
animation_link = urljoin(base_link, 'animation.php')
theater_link = urljoin(base_link, 'theater.php')
sports_link = urljoin(base_link, 'sports.php')
shortfilms_link = urljoin(base_link, 'shortfilm.php')
music_link = urljoin(base_link, 'music.php')
episode_link = urljoin(base_link, 'ajax.php?type=episode&epid={0}&view={1}')


def root(url):

    root_list = []
    groups_list = []

    html = client.request(url)

    if url == sports_link:

        sports_index = client.parseDOM(html, 'div', attrs={'class': 'col-xs-6 text-center'})[0]
        return sports_index

    elif url == music_link:

        music_index = client.parseDOM(html, 'div', attrs={'class': 'col-sm-5 col-md-4'})[0]
        return music_index

    else:

        result = client.parseDOM(html, 'div', attrs={'class': 'row', 'style': 'margin-bottom: 20px;'})[0]
        items = re.findall('(<option  ?value=.*?</option>)', result, re.U)

        groups = client.parseDOM(result, 'option', attrs={'selected value': '.+?'})

        for group in groups:
            if group == u'ΑΡΧΙΚΑ':
                group = group.replace(u'ΑΡΧΙΚΑ', '30213')
            elif group == u'ΕΤΟΣ':
                group = group.replace(u'ΕΤΟΣ', '30090')
            elif group == u'ΚΑΝΑΛΙ':
                group = group.replace(u'ΚΑΝΑΛΙ', '30211')
            elif group == u'ΕΙΔΟΣ':
                group = group.replace(u'ΕΙΔΟΣ', '30200')
            elif group == u'ΠΑΡΑΓΩΓΗ':
                group = group.replace(u'ΠΑΡΑΓΩΓΗ', '30212')
            groups_list.append(group)

        for item in items:

            name = client.parseDOM(item, 'option', attrs={'value': '.+?.php.+?'})[0]
            title = name[0].capitalize() + name[1:]
            link = client.parseDOM(item, 'option', ret='value')[0]
            indexer = urlparse(link).query
            index = urljoin(base_link, link)

            if indexer.startswith('l='):
                group = '30213'
            elif indexer.startswith('y='):
                group = '30090'
            elif indexer.startswith('c='):
                group = '30211'
            elif indexer.startswith('g='):
                group = '30200'
            elif indexer.startswith('p='):
                group = '30212'
            else:
                group = ''

            root_list.append({'title': title, 'group': group, 'action': 'listing', 'url': index})

        return root_list, groups_list


def sdik_exist():

    return bool(control.condVisibility('System.HasAddon({0})'.format(sdik)))


def bl_loader():

    comp = client.request(thgiliwt(bl))
    result = dexteni(b64decode(comp))

    bl_list = evaluate(result)

    return bl_list


class Indexer:

    def __init__(self, argv):

        self.list = []; self.data = []; self.years = []

        self.switch = {
            'title': control.lang(30045).format(control.lang(int(control.setting('vod_group')))),
            'icon': iconname('switcher'), 'action': 'vod_switcher&url={0}'
        }

        self.argv = argv

    def vod_switcher(self, url):

        self.data = cache.get(root, 24, url)[1]

        translated = [control.lang(int(i)) for i in self.data]

        choice = control.selectDialog(heading=control.lang(30062), list=translated)

        if choice <= len(self.data) and not choice == -1:
            control.setSetting('vod_group', self.data[choice])
            control.idle()
            control.sleep(100)  # ensure setting has been saved
            control.refresh()
        else:
            control.execute('Dialog.Close(all)')

    def movies(self):

        self.data = cache.get(root, 24, movies_link)[0]

        self.list = [
            item for item in self.data if any(
                group in item['group'] for group in [control.setting('vod_group')]
            )
        ]

        if (sdik_exist() and control.setting('hide_cartoons') == 'true') or not sdik_exist():
            self.list = [i for i in self.list if u'Κινουμένων σχεδίων' not in i['title']]

        for item in self.list:
            item.update({'icon': iconname('movies')})

        li = control.item(label=self.switch['title'], iconImage=self.switch['icon'])
        li.setArt({'fanart': control.addonInfo('fanart')})
        url = '{0}?action={1}'.format(sysaddon, self.switch['action'].format(movies_link))
        control.addItem(syshandle, url, li)

        directory.add(self.list, argv=self.argv)

    def short_films(self):

        self.data = cache.get(root, 24, shortfilms_link)[0]

        self.list = [
            item for item in self.data if any(
                group in item['group'] for group in [control.setting('vod_group')]
            )
        ]

        if (sdik_exist() and control.setting('hide_cartoons') == 'true') or not sdik_exist():
            self.list = [i for i in self.list if u'Κινουμένων σχεδίων' not in i['title']]

        for item in self.list:
            item.update({'icon': iconname('short')})

        li = control.item(label=self.switch['title'], iconImage=self.switch['icon'])
        li.setArt({'fanart': control.addonInfo('fanart')})
        url = '{0}?action={1}'.format(sysaddon, self.switch['action'].format(shortfilms_link))
        control.addItem(syshandle, url, li)

        directory.add(self.list, argv=self.argv)

    def series(self):

        self.data = cache.get(root, 24, series_link)[0]

        self.list = [
            item for item in self.data if any(
                group in item['group'] for group in [control.setting('vod_group')]
            )
        ]

        for item in self.list:
            item.update({'icon': iconname('series')})

        li = control.item(label=self.switch['title'], iconImage=self.switch['icon'])
        li.setArt({'fanart': control.addonInfo('fanart')})
        url = '{0}?action={1}'.format(sysaddon, self.switch['action'].format(series_link))
        control.addItem(syshandle, url, li)

        directory.add(self.list, argv=self.argv)

    def shows(self):

        self.data = cache.get(root, 24, shows_link)[0]

        self.list = [
            item for item in self.data if any(
                group in item['group'] for group in [control.setting('vod_group')]
            )
        ]

        for item in self.list:
            item.update({'icon': iconname('shows')})

        li = control.item(label=self.switch['title'], iconImage=self.switch['icon'])
        li.setArt({'fanart': control.addonInfo('fanart')})
        url = '{0}?action={1}'.format(sysaddon, self.switch['action'].format(shows_link))
        control.addItem(syshandle, url, li)

        directory.add(self.list, argv=self.argv)

    def cartoons_series(self):

        self.data = cache.get(root, 24, animation_link)[0]

        self.list = [
            item for item in self.data if any(
                group in item['group'] for group in [control.setting('vod_group')]
            )
        ]

        for item in self.list:
            item.update({'icon': iconname('cartoon_series')})

        li = control.item(label=self.switch['title'], iconImage=self.switch['icon'])
        li.setArt({'fanart': control.addonInfo('fanart')})
        url = '{0}?action={1}'.format(sysaddon, self.switch['action'].format(animation_link))
        control.addItem(syshandle, url, li)

        directory.add(self.list, argv=self.argv)

    def theater(self):

        self.data = cache.get(root, 24, theater_link)[0]

        self.list = [
            item for item in self.data if any(
                group in item['group'] for group in [control.setting('vod_group')]
            )
        ]

        for item in self.list:
            item.update({'icon': iconname('theater')})

        li = control.item(label=self.switch['title'], iconImage=self.switch['icon'])
        li.setArt({'fanart': control.addonInfo('fanart')})
        url = '{0}?action={1}'.format(sysaddon, self.switch['action'].format(theater_link))
        control.addItem(syshandle, url, li)

        directory.add(self.list, argv=self.argv)

    def items_list(self, url):

        indexer = urlparse(url).query

        ################################################################################################
        #                                                                                              #
        if 'movies.php' in url:                                                                        #
            length = 9                                                                                 #
        elif all(['shortfilm.php' in url, 'theater.php' in url]):                                      #
            length = 6                                                                                 #
        elif 'animation' in url and not sdik_exist():                                                  #
            return                                                                                     #
        else:                                                                                          #
            length = 2                                                                                 #
        #                                                                                              #
        ################################################################################################

        for year in list(range(1, length)):

            if indexer.startswith('l='):
                equation = 'y=' + str(year) + '&g=&p='
            elif indexer.startswith('g='):
                equation = 'y=' + str(year) + '&l=&p='
            elif indexer.startswith('p='):
                equation = 'y=' + str(year) + '&l=&g='
            elif indexer.startswith('c='):
                equation = 'y=' + str(year) + '&l=&g='
            else:
                equation = ''

            self.years.append(equation)

        if indexer.startswith(
                ('l=', 'g=', 's=', 'p=', 'c=')
        ) and 'movies.php' in url or 'shortfilm.php' in url or 'theater.php' in url:

            for content in self.years:
                links = base_link + url.rpartition('/')[2].partition('&')[0] + '&' + content
                htmls = client.request(links)
                self.data.append(htmls)

            result = ''.join(self.data)

            content = client.parseDOM(result, 'div', attrs={'class': 'col-xs-6 col-sm-4 col-md-3'})

        else:

            html = client.request(url)

            content = client.parseDOM(html, 'div', attrs={'class': 'col-xs-6 col-sm-4 col-md-3'})

        content = ''.join(content)
        items = re.findall('(<a.*?href.*?div.*?</a>)', content, re.U)

        for item in items:

            title = client.parseDOM(item, 'h4')[0]

            if (control.setting('hide_cartoons') == 'true' or not sdik_exist()) and title in cache.get(
                    bl_loader, 24) and all(['movies.php?g=8' not in url, 'shortfilm.php?g=8' not in url]):
                continue

            image = client.parseDOM(item, 'img', ret='src')[0]

            name = title.rpartition(' (')[0]

            image = urljoin(base_link, image)
            link = client.parseDOM(item, 'a', ret='href')[0]
            link = urljoin(base_link, link)
            year = re.findall('.*?\((\d{4})', title, re.U)[0]

            self.list.append(
                {
                    'title': title, 'url': link,
                    'image': image, 'year': int(year), 'name': name
                }
            )

        log_debug('List of vod items ~ ' + repr(self.list))

        return self.list

    def listing(self, url):

        self.list = cache.get(self.items_list, 12, url)

        if self.list is None:
            log_debug('Listing section failed to load, try resetting indexer methods')
            return

        log_debug('Caching was successful, list of vod items ~ ' + repr(self.list))

        if url.startswith((movies_link, theater_link, shortfilms_link)):
            if control.setting('action_type') == '0':
                for item in self.list:
                    item.update({'action': 'play', 'isFolder': 'False'})
            elif control.setting('action_type') == '2':
                for item in self.list:
                    if control.setting('auto_play') == 'false':
                        item.update({'action': 'play'})
                    else:
                        item.update({'action': 'play', 'isFolder': 'False'})
            else:
                for item in self.list:
                    item.update({'action': 'directory'})

        elif url.startswith(sports_link):
            for item in self.list:
                item.update({'action': 'events'})

        else:
            for item in self.list:
                item.update({'action': 'episodes'})

        for item in self.list:
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            refresh_cm = {'title': 30054, 'query': {'action': 'refresh'}}
            unwatched_cm = {'title': 30228, 'query': {'action': 'toggle_watched'}}
            item.update({'cm': [bookmark_cm, refresh_cm, unwatched_cm]})

        control.sortmethods('title')
        control.sortmethods('year')

        progress = len(self.list) >= 100

        if url.startswith((movies_link, theater_link, shortfilms_link)):
            directory.add(self.list, content='movies', argv=self.argv, progress=progress)
        else:
            directory.add(self.list, content='tvshows', argv=self.argv, progress=progress)

    def epeisodia(self, url):

        html = client.request(url)
        image = client.parseDOM(html, 'img', attrs={'class': 'thumbnail.*?'}, ret='src')[0]
        image = urljoin(base_link, image)
        year = client.parseDOM(html, 'h4', attrs={'style': 'text-indent:10px;'})[0]
        year = int(re.findall('\d{4}', year, re.U)[0])
        name = client.parseDOM(html, 'h2')[0]

        result = client.parseDOM(html, 'div', attrs={'style': 'margin:20px 0px 20px 0px;'})[0]

        episodes = re.compile('onclick="loadEpisode(.*?)">(.*?)</button>').findall(result)

        if 'text-justify' in html:
            plot = client.parseDOM(html, 'p', attrs={'class': 'text-justify'})[0]
        else:
            plot = control.lang(30085)

        info = client.parseDOM(html, 'h4', attrs={'style': 'text-indent:10px;'})
        genre = info[1].lstrip(u'Είδος:').strip()

        dictionary = {
            u'Ιαν': '01', u'Φεβ': '02', u'Μάρ': '03',
            u'Απρ': '04', u'Μάι': '05', u'Ιούν': '06',
            u'Ιούλ': '07', 'Αύγ': '08', u'Σεπ': '09',
            u'Οκτ': '10', u'Νοέ': '11', u'Δεκ': '12'
        }

        for eid, title in episodes:

            link = re.compile("'(.+?)'").findall(eid)
            link = episode_link.format(link[0], link[1])

            if '\'n\')' in eid:
                group = '1bynumber'
                if '.' in title:
                    season = int(title.partition('.')[0])
                    episode_num = title.partition('.')[2]
                    title = control.lang(30066) + ' ' + str(season) + ', ' + control.lang(30067) + ' ' + episode_num
                else:
                    title = control.lang(30067) + ' ' + title
            elif '\'d\')' in eid:
                group = '2bydate'
                row = result.split(eid)[0]
                y = re.findall('<h4.+?bold.+?(\d{4})', row, re.U)[-1]
                m = re.findall('width:50px..?>(.+?)<', row, re.U)[-1]
                m = dictionary[m]
                prefix = '0' + title if len(title) == 1 else title
                title = prefix + '-' + m + '-' + y
            else:
                group = '3bytitle'

            separator = ' - ' if control.setting('wrap_labels') == '1' else '[CR]'

            self.list.append(
                {
                    'title': name + separator + title, 'url': link, 'group': group,
                    'name': name, 'image': image, 'plot': plot, 'year': year,
                    'genre': genre
                }
            )

        return self.list

    def episodes(self, url):

        self.list = cache.get(self.epeisodia, 12, url)

        if self.list is None:
            log_debug('Episode section failed to load, try resetting indexer methods')
            return
        else:
            log_debug('List of vod items ~ ' + repr(self.list))

        if control.setting('action_type') == '0':
            for item in self.list:
                item.update({'action': 'play', 'isFolder': 'False'})
        elif control.setting('action_type') == '2':
            for item in self.list:
                if control.setting('auto_play') == 'false':
                    item.update({'action': 'play'})
                else:
                    item.update({'action': 'play', 'isFolder': 'False'})
        else:
            for item in self.list:
                item.update({'action': 'directory'})

        for item in self.list:

            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            refresh_cm = {'title': 30054, 'query': {'action': 'refresh'}}
            unwatched_cm = {'title': 30228, 'query': {'action': 'toggle_watched'}}
            item.update({'cm': [bookmark_cm, refresh_cm, unwatched_cm]})

        if control.setting('episodes_reverse') == 'true':
            self.list = sorted(
                self.list,
                key=lambda k: k['group'] if k['group'] in ['1bynumber', '2bydate'] else k['title'], reverse=True
            )[::-1]
        else:
            self.list = sorted(self.list, key=lambda k: k['group'])

        # control.sortmethods('unsorted')
        # control.sortmethods('title')
        # control.sortmethods('year')

        directory.add(self.list, content='episodes', argv=self.argv, progress=len(self.list) >= 100)

    def gm_sports(self):

        html = cache.get(root, 48, sports_link)
        options = re.compile('(<option value.+?</option>)', re.U).findall(html)

        icons = ['https://www.shareicon.net/data/256x256/2015/11/08/157712_sport_512x512.png',
                 'https://www.shareicon.net/data/256x256/2015/12/07/196797_ball_256x256.png']

        items = zip(options, icons)

        for item, image in items:

            title = client.parseDOM(item, 'option')[0]
            url = client.parseDOM(item, 'option', ret='value')[0]
            url = client.replaceHTMLCodes(url)
            index = urljoin(base_link, url)

            data = {
                'title': title, 'action': 'listing', 'url': index,
                'image': image
            }
            self.list.append(data)

        directory.add(self.list, argv=self.argv)

    def event_list(self, url):

        html = client.request(url)
        items = client.parseDOM(html, 'div', attrs={'style': 'margin-bottom: 10px'})

        for item in items:

            title = client.parseDOM(item, 'a', attrs={'class': 'btn btn-default'})[0]
            image = client.parseDOM(html, 'img', attrs={'class': 'thumbnail img-responsive pull-right'}, ret='src')[0]
            image = urljoin(base_link, image)
            link = client.parseDOM(item, 'a', attrs={'class': 'btn btn-default'}, ret='href')[0]
            link = urljoin(base_link, link)
            plot = client.parseDOM(item, 'span', attrs={'class': 'pull-right'})[0]

            self.list.append(
                {
                    'title': title, 'url': link, 'plot': plot,
                    'image': image
                }
            )

        return self.list

    def events(self, url):

        self.list = cache.get(self.event_list, 12, url)

        if self.list is None:
            log_debug('Events section failed to load, try resetting indexer methods')
            return

        for item in self.list:
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            item.update({'cm': [bookmark_cm], 'action': 'play', 'isFolder': 'False'})

        directory.add(self.list, argv=self.argv)
