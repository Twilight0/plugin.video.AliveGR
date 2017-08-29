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

import json
# noinspection PyUnresolvedReferences
from tulip import cache, control, directory, client, ordereddict
from ..modules import sysaddon, syshandle
from ..modules.themes import iconname
from ..modules.helpers import thgiliwt


class Main:

    def __init__(self):

        self.list = []; self.data = []; self.groups = []
        self.alivegr = 'AbthnLydWZ2lGbh9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'
        self.alt_str = ['(1)', '(2)', '(3)', '(4)', '(5)', '(6)', 'BUP']

    def live(self):

        if control.setting('dev_switch') == 'false':

            result = client.request(thgiliwt('==' + self.alivegr))

        else:

            if control.setting('show_dialog') == 'true':
                choice = control.selectDialog(['Load local file', 'Load remote list'])
            else:
                choice = -1

            if choice == 0:
                local = control.setting('local')
                with open(local) as xml:
                    result = xml.read()
                    xml.close()
            elif choice == 1:
                result = client.request(control.setting('remote'))
            else:
                result = client.request(thgiliwt('==' + self.alivegr))

        if control.setting('dev_switch') == 'false':
            channels = client.parseDOM(result, 'channel', attrs={'enable': '1'})
        else:
            channels = client.parseDOM(result, 'channel', attrs={'enable': '1|2'})

        updated = client.parseDOM(result, 'channels', ret='updated')[0]

        for channel in channels:

            name = client.parseDOM(channel, 'name')[0]
            logo = client.parseDOM(channel, 'logo')[0]
            group = client.parseDOM(channel, 'group')[0]
            url = client.parseDOM(channel, 'url')[0]

            info = client.parseDOM(channel, 'info')[0]
            if len(info) == 5 and info[:5].isdigit():
                info = control.lang(int(info))

            data = (
                {
                    'title': name, 'image': logo, 'group': group, 'url': url,
                    'genre': control.lang(30096) + ', ' + group, 'plot': info,
                    'duration': None
                }
            )
            self.list.append(data)
            self.data.append(group)

        self.groups = list(ordereddict.OrderedDict.fromkeys(self.data))

        self.groups.sort()

        return self.list, self.groups, updated

    def switcher(self):

        def seq(choose):

            control.setSetting('live_group', choose)
            control.idle()
            control.sleep(50)
            control.refresh()

        self.data = cache.get(self.live, 24)[1]
        self.groups = [control.lang(30048)] + self.data
        choice = control.selectDialog(heading=control.lang(30049), list=self.groups)

        if choice == 0:
            seq('ALL')
        elif choice <= len(self.groups) and not choice == -1:
            seq(self.groups.pop(choice))
        else:
            control.execute('Dialog.Close(all)')

    def live_tv(self):

        if control.setting('dev_switch') == 'false':
            self.list = cache.get(self.live, 4)[0]
        else:
            self.list = cache.get(self.live, int(control.setting('cache_period')))[0]

        switch = {
            'title': control.lang(30047).format(
                control.lang(30048) if control.setting('live_group') == 'ALL' else control.setting(
                    'live_group'
                ).decode('utf-8')
            ),
            'icon': iconname('switcher'),
            'action': 'live_switcher',
            'plot': control.lang(30034)
        }

        self.data = [
            item for item in self.list if any(
                item['group'] == group for group in [control.setting('live_group')]
            )
        ] if not control.setting('live_group') == 'ALL' else self.list

        if control.setting('live_sort') == 'true':
            if control.setting('live_method') == '0':
                self.list = sorted(self.data, key=lambda k: k['title'].lower())
            elif control.setting('live_method') == '1':
                self.list = sorted(self.data, key=lambda k: k['group'].lower())
        else:
            self.list = self.data

        if control.setting('show-alt') == 'false':
            self.list = [item for item in self.list if not any(alt in item['title'] for alt in self.alt_str)]
        else:
            pass

        for item in self.list:
            item.update({'action': 'play', 'isFolder': 'False'})

        for item in self.list:

            bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
            bookmark['bookmark'] = item['url']

            bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            r_and_c_cm = {'title': 30082, 'query': {'action': 'refresh_and_clear'}}
            pvr_client_cm = {'title': 30084, 'query': {'action': 'pvr_client', 'tvguide': 'true'}}

            if control.condVisibility('Pvr.HasTVChannels'):
                item.update({'cm': [bookmark_cm, r_and_c_cm, pvr_client_cm]})
            else:
                item.update({'cm': [bookmark_cm, r_and_c_cm]})

        if control.setting('show-switcher') == 'true':

            li = control.item(label=switch['title'], iconImage=switch['icon'])
            li.setArt({'fanart': control.addonInfo('fanart')})
            li.setInfo('video', {'plot': switch['plot'] + '\n' + control.lang(30035) + cache.get(self.live, 4)[2]})
            url = '{0}?action={1}'.format(sysaddon, switch['action'])
            control.addItem(syshandle, url, li)

        else:
            pass

        # if control.infoLabel('System.AddonVersion(xbmc.python)') == '2.24.0':
        directory.add(self.list, content='movies')
        # else:
        #     directory.add(self.list)

