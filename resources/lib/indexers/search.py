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


from tulip import client, directory, control, cache, cleantitle
from tulip.init import sysaddon
from tulip.compat import urljoin, unquote_plus, iteritems
from resources.lib.indexers import gm
import re, json, live


class Indexer:

    WRAPPER_MOVIES = 0
    WRAPPER_SHOWS = 1

    def __init__(self, argv):

        self.list = [] ; self.data = []
        self.google = 'https://encrypted.google.com/search?as_q={0}&as_sitesearch={1}'
        self.UA = {'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:18.0) Gecko/18.0 Firefox/18.0'}
        self.argv = argv

    def wrapper(self, str_input, mode):

        query = self.google.format(str_input.encode('utf-8'), gm.base_link)

        html = client.request(query.replace(' ', '+'), headers=self.UA)

        items = client.parseDOM(html, 'h3', attrs={'class': 'r'})

        for item in items:

            if mode == 0:
                title = client.parseDOM(item, 'a')[0]
            else:
                title = client.parseDOM(item, 'a')[0].rstrip(u' ‒ Greek-Movies')
            title = client.replaceHTMLCodes(title)
            title = re.sub('</?b>', '', title)

            if '- Greek' in title:
                idx = title.rfind('- Greek')
                title = title[:idx].strip()
            elif u'‒ Greek' in title:
                idx = title.rfind(u'‒ Greek')
                title = title[:idx].strip()

            url = client.parseDOM(item, 'a', ret='href')[0]
            url = unquote_plus(url.partition('=')[2].partition('&amp;')[0])

            if mode == 0:
                if all(['movies.php?m=' not in url, 'theater.php?m=' not in url]):
                    continue
            else:
                if all(['shows.php?s=' not in url, 'series.php?s=' not in url]):
                    continue

            item_html = client.request(url)

            try:
                thumb = client.parseDOM(item_html, 'img', attrs={'class': 'thumbnail.*?'}, ret='src')[0]
            except IndexError:
                thumb = client.parseDOM(item_html, 'IMG', ret='SRC')[0]

            image = urljoin(gm.base_link, thumb)

            year = client.parseDOM(item_html, 'h4', attrs={'style': 'text-indent:10px;'})[0]
            year = int(year.strip(u'Έτος:').strip()[:4])

            if 'text-align: justify' in html:
                plot = client.parseDOM(html, 'p', attrs={'style': 'text-align: justify'})[0]
            elif 'text-justify' in html:
                plot = client.parseDOM(html, 'p', attrs={'class': 'text-justify'})[0]
            else:
                plot = control.lang(30085)

            if mode == 0:
                self.list.append(
                    {
                        'title': title.encode('utf-8'), 'url': url, 'image': image.encode('utf-8'), 'year': year,
                        'plot': plot
                    }
                )

                if control.setting('action_type') == '0' or control.setting('action_type') == '2':
                    for item in self.list:
                        item.update({'action': 'play', 'isFolder': 'False'})
                else:
                    for item in self.list:
                        item.update({'action': 'directory'})

            else:
                self.list.append(
                    {
                        'title': title, 'url': url, 'image': image.encode('utf-8'), 'year': year, 'plot': plot,
                        'action': 'episodes'
                    }
                )

        for item in self.list:
            bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            bookmark['bookmark'] = item['url']
            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            item.update({'cm': [bookmark_cm]})

        if self.list is None:
            return

        self.list = sorted(self.list, key=lambda k: k['title'])

        return self.list

    def search(self):

        choices = [control.lang(30096), control.lang(30097), control.lang(30098)]
        choice = control.selectDialog(heading=control.lang(30095), list=choices)

        if choice == 0:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30096)
            )

            if not str_input:
                return

            try:
                str_input = str_input.decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                pass

            self.list = live.Indexer(argv=self.argv).live_tv(zapping=False, query=str_input.lower())

            directory.add(self.list, argv=self.argv)

        elif choice == 1:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30097)
            )

            try:
                str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                str_input = cleantitle.strip_accents(str_input)

            if not str_input:
                return

            self.list = cache.get(self.wrapper, 12, str_input, self.WRAPPER_MOVIES)

            directory.add(self.list, content='movies', argv=self.argv)

        elif choice == 2:

            str_input = control.dialog.input(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30098)
            )

            if not str_input:

                return

            try:
                str_input = cleantitle.strip_accents(str_input.decode('utf-8'))
            except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
                str_input = cleantitle.strip_accents(str_input)

            self.list = cache.get(self.wrapper, 12, str_input, self.WRAPPER_SHOWS)

            directory.add(self.list, content='movies', argv=self.argv)

        else:

            control.execute('ActivateWindow(videos,"{0}")'.format(sysaddon))
