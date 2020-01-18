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

from tulip import control, client, cache
from tulip.init import syshandle
from ..modules.themes import iconname
from ..modules.constants import ART_ID, SYSADDON


class Indexer:

    def __init__(self):

        self.list = []; self.data = []; self.directory = []
        self.fp_link = 'http://www.frontpages.gr'

    def news(self):

        items = [
            {
                'title': control.lang(30230),
                'icon': 'https://www.iconexperience.com/_img/v_collection_png/256x256/shadow/newspaper.png',
                'url': '{0}?action=papers'.format(SYSADDON),
                'fanart': control.addonInfo('fanart')
            }
            ,
            {
                'title': control.lang(30118),
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='ert_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.ert.gr/?action=episodes&url=https%3a%2f%2fwebtv.ert.gr%2fcategory%2feidiseis%2f',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='ert_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30119),
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='ant1_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.antenna.gr/?action=videos&url=https%3a%2f%2fwww.antenna.gr%2fant1news%2fvideos',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='ant1_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30120),
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='star_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.star.gr/?action=news',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='star_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30122),
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='alpha_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.alphatv.gr/?action=news&url=https%3a%2f%2fwww.alphatv.gr%2fnews',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='alpha_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30121),
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='skai_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.skai.gr/?action=news',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='skai_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'Euronews',
                'icon': control.addonmedia(addonid=ART_ID, theme='networks', icon='euronews_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.euronews.com/?action=videos&url=%22methodName%22%3a%22content.getThemeDetails%22%2c%22params%22%3a%7b%22tId%22%3a%221%22%7d',
                'fanart': control.addonmedia(addonid=ART_ID, theme='networks', icon='euronews_fanart.jpg', media_subfolder=False)
            }
        ]

        for item in items:

            list_item = control.item(label=item['title'])
            list_item.setArt({'icon': item['icon'], 'fanart': item['fanart']})
            url = item['url']
            isFolder = True
            self.list.append((url, list_item, isFolder))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    @staticmethod
    def switcher():

        def seq(choose):

            control.setSetting('papers_group', choose)
            control.idle()
            control.sleep(100)
            control.refresh()

        groups = (
            [control.lang(30235), control.lang(30231), control.lang(30232), control.lang(30233), control.lang(30234)],
            ['0', '1', '2', '3', '4']
        )

        choice = control.selectDialog(heading=control.lang(30049), list=groups[0])

        if choice == 0:
            seq('0')
        elif choice <= len(groups[0]) and not choice == -1:
            seq(groups[1][choice])
        else:
            control.execute('Dialog.Close(all)')

    def front_pages(self):

        html = client.request(self.fp_link)

        try:
            groups = client.parseDOM(html.decode('utf-8'), 'div', attrs={'class': 'tabbertab.+?'})
        except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
            groups = client.parseDOM(html, 'div', attrs={'class': 'tabbertab.+?'})

        for group, papers in list(enumerate(groups, start=1)):

            items = client.parseDOM(papers, 'div', attrs={'class': 'thumber'})

            for i in items:

                image = client.parseDOM(i, 'img', attrs={'style': 'padding:5px.+?'}, ret='src')[0]
                title = client.parseDOM(i, 'img', attrs={'style': 'padding:5px.+?'}, ret='alt')[0]
                image = self.fp_link + image
                link = image.replace('B.jpg', 'I.jpg')

                data = {'title': title, 'image': image, 'url': link, 'group': group}

                self.list.append(data)

        return self.list

    def papers_index(self):

        self.data = cache.get(self.front_pages, 12)

        if not self.data:
            return

        for i in self.data:
            i.update({'action': None, 'isFolder': 'False'})

        self.list = [
            item for item in self.data if any(
                item['group'] == group for group in [int(control.setting('papers_group'))]
            )
        ] if not control.setting('papers_group') == '0' else self.data

        if control.setting('papers_group') == '1':
            integer = 30231
        elif control.setting('papers_group') == '2':
            integer = 30232
        elif control.setting('papers_group') == '3':
            integer = 30233
        elif control.setting('papers_group') == '4':
            integer = 30234
        else:
            integer = 30235

        switch = {
            'title': control.lang(30047).format(control.lang(integer)),
            'icon': iconname('switcher'),
            'action': 'papers_switcher'
        }

        if control.setting('show_pic_switcher') == 'true':

            li = control.item(label=switch['title'], iconImage=switch['icon'])
            li.setArt({'fanart': control.addonInfo('fanart')})
            url = '{0}?action={1}'.format(SYSADDON, switch['action'])
            control.addItem(syshandle, url, li)

        for i in self.list:

            li = control.item(label=i['title'], iconImage=i['image'])
            li.setArt({'poster': i['image'], 'thumb': i['image'], 'fanart': control.addonInfo('fanart')})
            li.setInfo('image', {'title': i['title'], 'picturepath': i['url']})
            url = i['url']
            isFolder = False
            self.directory.append((url, li, isFolder))

        control.addItems(syshandle, self.directory)
        control.directory(syshandle)
