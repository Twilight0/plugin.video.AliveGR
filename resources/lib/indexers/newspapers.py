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


from tulip import control, client, cache
from tulip.init import syshandle, sysaddon
from ..modules.themes import iconname


class Indexer:

    def __init__(self):

        self.list = []; self.data = []; self.directory = []
        self.fp_link = 'http://www.frontpages.gr'

    @staticmethod
    def switcher():

        def seq(choose):

            control.setSetting('papers_group', choose)
            control.idle()
            control.sleep(50)
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
            html = html.decode('utf-8')
        except AttributeError:
            pass

        groups = client.parseDOM(html, 'div', attrs={'class': 'tabbertab'})

        for group, papers in list(enumerate(groups, start=1)):

            items = client.parseDOM(papers, 'div', attrs={'class': 'thumber'})

            for i in items:

                name = client.parseDOM(i, 'a', attrs={'style': 'font-size:12px;color:white;'})[0]
                headline = client.parseDOM(i, 'img', attrs={'style': 'padding:5px 0;'}, ret='alt')[0]
                if headline == '':
                    headline = u'Πρωτοσέλιδο εφημερίδας'
                title = name + ': ' + headline
                image = client.parseDOM(i, 'img', attrs={'style': 'padding:5px 0;'}, ret='src')[0]
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

        if control.setting('show-switcher') == 'true':

            li = control.item(label=switch['title'], iconImage=switch['icon'])
            li.setArt({'fanart': control.fanart()})
            url = '{0}?action={1}'.format(sysaddon, switch['action'])
            control.addItem(syshandle, url, li)

        else:
            pass

        for i in self.list:

            li = control.item(label=i['title'], iconImage=i['image'])
            li.setArt({'poster': i['image'], 'thumb': i['image'], 'fanart': control.fanart()})
            li.setInfo('image', {'title': i['title'], 'picturepath': i['url']})
            url = i['url']
            isFolder = False
            self.directory.append((url, li, isFolder))

        control.addItems(syshandle, self.directory)
        control.directory(syshandle)
