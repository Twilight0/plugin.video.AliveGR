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


from tulip import cache, client, control
from tulip.log import *
from tulip.init import syshandle
from ..modules.helpers import thgiliwt
from ..modules.constants import yt_addon


class Indexer:

    def __init__(self):

        self.list = [] ; self.data = []
        self.misc = 'AbthnL55WYsxWZjNXat9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'

    def misc_list(self):

        if control.setting('debug') == 'false':

            playlists = client.request(thgiliwt('=={0}'.format(self.misc)))

        else:

            if control.setting('local_remote') == '0':
                local = control.setting('misc_local')
                with open(local) as xml:
                    playlists = xml.read()
                    xml.close()
            elif control.setting('local_remote') == '1':
                playlists = client.request(control.setting('misc_remote'))
            else:
                playlists = client.request(thgiliwt('=={0}'.format(self.misc)))

        self.data = client.parseDOM(playlists, 'item')

        for item in self.data:

            title = client.parseDOM(item, 'title')[0]
            icon = client.parseDOM(item, 'icon')[0]
            url = client.parseDOM(item, 'url')[0]

            item_data = (
                dict(title=title, icon=icon, url=url.replace(
                    'https://www.youtube.com/channel', '{0}/channel'.format(yt_addon)
                ))
            )

            self.list.append(item_data)

        return self.list

    def miscellany(self):

        if control.setting('debug') == 'true':
            self.data = cache.get(self.misc_list, int(control.setting('cache_period')))
        else:
            self.data = cache.get(self.misc_list, 24)

        if self.data is None:
            log_debug('Misc channels list did not load successfully')
            return

        self.list = []

        for item in self.data:

            if control.setting('lang_split') == '0':
                if 'Greek' in control.infoLabel('System.Language'):
                    li = control.item(label=item['title'].partition(' - ')[2])
                elif 'English' in control.infoLabel('System.Language'):
                    li = control.item(label=item['title'].partition(' - ')[0])
                else:
                    li = control.item(label=item['title'])
            elif control.setting('lang_split') == '1':
                li = control.item(label=item['title'].partition(' - ')[0])
            elif control.setting('lang_split') == '2':
                li = control.item(label=item['title'].partition(' - ')[2])
            else:
                li = control.item(label=item['title'])

            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            url = item['url']
            isFolder = True
            self.list.append((url, li, isFolder))

        control.execute('Container.SetViewMode(50)')
        control.addItems(syshandle, self.list)
        control.directory(syshandle)
