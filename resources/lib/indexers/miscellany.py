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


from tulip import cache, control, client
from ..modules import syshandle
from ..modules.helpers import thgiliwt


class Main:

    def __init__(self):

        self.list = [] ; self.data = []
        self.misc = 'AbthnL55WYsxWZjNXat9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'

    def misc_list(self):

        if control.setting('dev_switch') == 'false':

            playlists = client.request(thgiliwt('==' + self.misc))

        else:

            choice = control.selectDialog(['Load local file', 'Load custom remote list'])

            if choice == 0:
                local = control.setting('misc_local')
                with open(local) as xml:
                    playlists = xml.read()
                    xml.close()
            elif choice == 1:
                playlists = client.request(control.setting('misc_remote'))
            else:
                playlists = client.request(thgiliwt(self.misc))

        self.data = client.parseDOM(playlists, 'item')

        for item in self.data:

            title = client.parseDOM(item, 'title')[0]
            icon = client.parseDOM(item, 'icon')[0]
            url = client.parseDOM(item, 'url')[0]

            item_data = (dict(
                title=title, icon=icon, url=url.replace(
                    'https://www.youtube.com/channel', 'plugin://plugin.video.youtube/channel'
                )
            ))
            self.list.append(item_data)

        return self.list

    def miscellany(self):

        if control.setting('dev_switch') == 'true':
            self.data = cache.get(self.misc_list, int(control.setting('cache_period')))
        else:
            self.data = cache.get(self.misc_list, 24)

        if self.data is None:
            return

        self.list = []

        for item in self.data:
            if control.setting('splitter') == 'true':
                if control.setting('lang_split') == '0':
                    li = control.item(label=item['title'].partition('-')[0].strip())
                elif control.setting('lang_split') == '1':
                    li = control.item(label=item['title'].partition('-')[2].strip())
            else:
                li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            url = item['url']
            isFolder = True
            self.list.append((url, li, isFolder))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)
