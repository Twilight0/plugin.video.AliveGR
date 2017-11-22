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


from tulip import client, directory, control, cache
from tulip.init import sysaddon
import gm
import re, urllib, urlparse, json


class Main:

    def __init__(self):

        self.list = [] ; self.data = []
        self.google = 'https://encrypted.google.com/search?as_q={0}&as_sitesearch={1}'
        self.UA = {'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:18.0) Gecko/18.0 Firefox/18.0'}

    def search(self):

        def strip_accents(s):

            import unicodedata

            result = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

            return result

        choices = [control.lang(30096), control.lang(30097), control.lang(30098)]
        choice = control.selectDialog(heading=control.lang(30095), list=choices)

        if choice == 0:

            str_input = control.inputDialog(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30096)
            )

            if bool(str_input):

                import live

                self.data = cache.get(live.Main().live, 4)[0]

                for item in self.data:
                    item.update({'action': 'play', 'isFolder': 'False'})

                self.list = [item for item in self.data if str_input.lower().decode('utf-8') in item['title'].lower()]

                if self.list is None:
                    return

                for item in self.list:
                    bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
                    bookmark['bookmark'] = item['url']
                    bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
                    item.update({'cm': [bookmark_cm]})

                self.list = sorted(self.list, key=lambda k: k['title'].lower())

                directory.add(self.list)

            else:

                return

        elif choice == 1:

            import documentaries

            str_input = control.inputDialog(
                heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30097)
            )

            str_input = strip_accents(str_input.decode('utf-8'))

            if bool(str_input):

                query = self.google.format(str_input.encode('utf-8'), gm.base_link)

                html = client.request(query.replace(' ', '+'), headers=self.UA)

                items = client.parseDOM(html, 'h3', attrs={'class': 'r'})

                for item in items:

                    title = client.parseDOM(item, 'a')[0]
                    title = client.replaceHTMLCodes(title)
                    title = re.sub('</?b>', '', title)

                    if '- Greek' in title:
                        idx = title.rfind('- Greek')
                        title = title[:idx].strip()
                    elif u'‒ Greek' in title:
                        idx = title.rfind(u'‒ Greek')
                        title = title[:idx].strip()

                    url = client.parseDOM(item, 'a', ret='href')[0]
                    url = urllib.unquote_plus(url.partition('=')[2].partition('&amp;')[0])

                    if all(['movies.php?m=' not in url, 'theater.php?m=' not in url]):
                        continue

                    item_html = client.request(url)

                    try:
                        thumb = client.parseDOM(item_html, 'img', attrs={'class': 'thumbnail.*?'}, ret='src')[0]
                    except IndexError:
                        thumb = client.parseDOM(item_html, 'IMG', ret='SRC')[0]

                    image = urlparse.urljoin(gm.base_link, thumb)

                    year = client.parseDOM(item_html, 'h4', attrs={'style': 'text-indent:10px;'})[0]
                    year = int(year.strip(u'Έτος:').strip()[:4])

                    if 'text-align: justify' in html:
                        plot = client.parseDOM(html, 'p', attrs={'style': 'text-align: justify'})[0]
                    elif 'text-justify' in html:
                        plot = client.parseDOM(html, 'p', attrs={'class': 'text-justify'})[0]
                    else:
                        plot = control.lang(30085)

                    self.data.append(
                        {
                            'title': title.encode('utf-8'), 'url': url, 'image': image.encode('utf-8'), 'year': year,
                            'plot': plot
                        }
                    )

                dl = [
                    item for item in cache.get(
                        documentaries.Main().items_list, 48
                    ) if str_input.lower() in strip_accents(item['title'].decode('utf-8')).lower()
                ]

                for item in dl:
                    item.update({'action': 'play', 'isFolder': 'False'})

                if control.setting('dialog_type') == '0':
                    for item in self.data:
                        item.update({'action': 'play', 'isFolder': 'False'})
                else:
                    for item in self.data:
                        item.update({'action': 'directory'})

                self.list = self.data + dl

                for item in self.list:
                    bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
                    bookmark['bookmark'] = item['url']
                    bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
                    item.update({'cm': [bookmark_cm]})

                if self.list is None:
                    return

                self.list = sorted(self.list, key=lambda k: k['title'])

                directory.add(self.list, content='movies')

            else:
                return

        elif choice == 2:

            str_input = control.inputDialog(heading=control.lang(30095).partition(' ')[0] + control.lang(30100) + control.lang(30098))

            if bool(str_input):

                query = self.google.format(str_input, gm.base_link)

                html = client.request(query.replace(' ', '+'), headers=self.UA)

                items = client.parseDOM(html, 'h3', attrs={'class': 'r'})

                for item in items:

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
                    url = urllib.unquote_plus(url.partition('=')[2].partition('&amp;')[0])

                    if all(['shows.php?s=' not in url, 'series.php?s=' not in url]):
                        continue

                    item_html = client.request(url)

                    try:
                        thumb = client.parseDOM(item_html, 'img', attrs={'class': 'thumbnail.*?'}, ret='src')[0]
                    except IndexError:
                        thumb = client.parseDOM(item_html, 'IMG', ret='SRC')[0]

                    image = urlparse.urljoin(gm.base_link, thumb)

                    year = client.parseDOM(item_html, 'h4', attrs={'style': 'text-indent:10px;'})[0]
                    year = int(year.strip(u'Έτος:').strip()[:4])

                    if 'text-align: justify' in html:
                        plot = client.parseDOM(html, 'p', attrs={'style': 'text-align: justify'})[0]
                    elif 'text-justify' in html:
                        plot = client.parseDOM(html, 'p', attrs={'class': 'text-justify'})[0]
                    else:
                        plot = control.lang(30085)

                    self.list.append(
                        {
                            'title': title, 'url': url, 'image': image.encode('utf-8'), 'year': year, 'plot': plot,
                            'action': 'episodes'
                        }
                    )

                if self.list is None:
                    return

                for item in self.list:
                    bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
                    bookmark['bookmark'] = item['url']
                    bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
                    item.update({'cm': [bookmark_cm]})

                directory.add(self.list, content='movies')

            else:
                return

        else:

            control.execute('ActivateWindow(10025, "{0}")'.format(sysaddon))
