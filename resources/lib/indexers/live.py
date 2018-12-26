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
from datetime import datetime
from base64 import b64decode
from tulip import cache, control, directory, client
from tulip.log import log_debug
from tulip.init import sysaddon, syshandle
from tulip.compat import OrderedDict
from resources.lib.modules.themes import iconname
from resources.lib.modules.helpers import thgiliwt, dexteni
from resources.lib.modules.constants import live_groups, logos_id


class Indexer:

    def __init__(self, argv, params=None):

        self.list = []; self.data = []; self.groups = []
        self.alivegr = 'QjNi5SZ2lGbvcXYy9Cdl5mLydWZ2lGbh9yL6MHc0RHa'
        self.argv = argv
        self.params = params

    def switcher(self):

        def seq(group):

            control.setSetting('live_group', str(group))
            control.idle()
            control.sleep(50)
            control.refresh()

        self.groups = cache.get(self.live, 8)[1]
        translated = [control.lang(i) for i in self.groups]
        self.data = [control.lang(30048)] + self.groups
        choice = control.selectDialog(heading=control.lang(30049), list=[control.lang(30048)] + translated)

        if choice == 0:
            seq('ALL')
        elif choice <= len(self.data) and not choice == -1:
            seq(self.data[choice])
        else:
            control.idle()

    def live(self):

        if control.setting('debug') == 'false':

            result = client.request(thgiliwt('=' + self.alivegr))
            result = dexteni(b64decode(result))

        else:

            if control.setting('local_remote') == '0':
                local = control.setting('live_local')
                with open(local) as xml:
                    result = xml.read()
                    xml.close()
            elif control.setting('local_remote') == '1':
                result = client.request(control.setting('live_remote'))
            else:
                result = client.request(thgiliwt('==' + self.alivegr))
                result = dexteni(b64decode(result))

        if control.setting('debug') == 'false':
            channels = client.parseDOM(result, 'channel', attrs={'enable': '1'})
        else:
            channels = client.parseDOM(result, 'channel', attrs={'enable': '1|2'})

        updated = client.parseDOM(result, 'channels', ret='updated')[0]

        for channel in channels:

            title = client.parseDOM(channel, 'name')[0]
            image = client.parseDOM(channel, 'logo')[0]
            if not image.startswith('http'):
                image = control.addonmedia(image, logos_id, theme='logos', media_subfolder=False)
            group = client.parseDOM(channel, 'group')[0]
            group = live_groups[group]
            url = client.parseDOM(channel, 'url')[0]

            website = client.parseDOM(channel, 'website')[0].replace('&amp;', '&')

            info = client.parseDOM(channel, 'info')[0]
            if len(info) == 5 and info[:5].isdigit():
                info = control.lang(int(info))

            if ' - ' in info:
                if control.setting('lang_split') == '0':
                    if 'Greek' in control.infoLabel('System.Language'):
                        info = info.partition(' - ')[2]
                    elif 'English' in control.infoLabel('System.Language'):
                        info = info.partition(' - ')[0]
                    else:
                        info = info
                elif control.setting('lang_split') == '1':
                    info = info.partition(' - ')[0]
                elif control.setting('lang_split') == '2':
                    info = info.partition(' - ')[2]
                else:
                    info = info

            data = (
                {
                    'title': title, 'image': image, 'group': str(group), 'url': url,
                    'genre': control.lang(group), 'plot': info, 'website': website
                }
            )

            self.list.append(data)
            self.data.append(group)

        self.groups = list(OrderedDict.fromkeys(self.data))

        log_debug('Live list uncached' + repr(self.list))

        return self.list, self.groups, updated

    def live_tv(self, zapping=False):

        if control.setting('debug') == 'false':
            self.list = self.live()[0]
        else:
            self.list = cache.get(self.live, int(control.setting('cache_period')))[0]

        if self.list is None:
            log_debug('Live channels list did not load successfully')
            return
        else:
            log_debug('Caching was successful, list of channels ~ ' + repr(self.list))

        switch = {
            'title': control.lang(30047).format(
                control.lang(30048) if control.setting('live_group') == 'ALL' else control.lang(
                    int(control.setting('live_group'))
                )
            ),
            'icon': iconname('switcher'),
            'action': 'live_switcher',
            'plot': control.lang(30034)
        }

        self.list = [
            item for item in self.list if any(
                item['group'] == group for group in [control.setting('live_group')]
            )
        ] if not control.setting('live_group') == 'ALL' else self.list

        if control.setting('show_alt') == 'false':
            self.list = [
                item for item in self.list if not any(['BUP' in item['title'], re.search('\(\d\)', item['title'])])
            ]

        year = datetime.now().year

        for count, item in list(enumerate(self.list, start=1)):
            item.update({'action': 'play_direct' if zapping else 'play', 'isFolder': 'False', 'year': year, 'duration': None, 'code': str(count)})

        if zapping:
            if control.setting('zapping_preresolve') == 'true':
                from resources.lib.modules.player import router
                for item in self.list:
                    try:
                        item.update({'url': router(item['url'], params=self.params)})
                    except Exception as e:
                        log_debug('Skipped ' + item['title'] + ' from resolve, reason: ' + repr(e))
                        continue
            m3u = directory.m3u_maker(self.list, argv=self.argv)
            return m3u

        for item in self.list:

            # bookmark = dict((k, v) for k, v in iteritems(item) if not k == 'next')
            # bookmark['bookmark'] = item['url']
            #
            # bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            r_and_c_cm = {'title': 30082, 'query': {'action': 'refresh_and_clear'}}
            pvr_client_cm = {'title': 30084, 'query': {'action': 'pvr_client', 'query': 'true'}}
            zapping_cm = {'title': 30293, 'query': {'action': 'zapping_mode'}}
            if item['website'] != 'None':
                web_cm = {'title': 30316, 'query': {'action': 'open_link', 'url': item['website']}}
            else:
                web_cm = None

            if control.condVisibility('Pvr.HasTVChannels'):
                item.update({'cm': [r_and_c_cm, pvr_client_cm, zapping_cm, web_cm]})
            else:
                item.update({'cm': [r_and_c_cm, zapping_cm, web_cm]})

        if control.setting('show_switcher') == 'true':

            li = control.item(label=switch['title'], iconImage=switch['icon'])
            li.setArt({'fanart': control.addonInfo('fanart')})
            li.setInfo('video', {'plot': switch['plot'] + '\n' + control.lang(30035) + cache.get(self.live, 8)[2]})
            url = '{0}?action={1}'.format(sysaddon, switch['action'])
            control.addItem(syshandle, url, li)

        else:
            pass

        control.sortmethods('production_code')
        control.sortmethods('title')
        control.sortmethods('genre')

        directory.add(self.list, content='movies', argv=self.argv)

    def modular(self, group):

        if group == '30125':
            fanart = 'https://i.ytimg.com/vi/vtjL9IeowUs/maxresdefault.jpg'
        elif group == '30032':
            fanart = 'http://cdn.iview.abc.net.au/thumbs/i/ls/LS1604H001S005786f5937ded19.22034349_1280.jpg'
        else:
            fanart = control.addonInfo('fanart')

        self.data = cache.get(self.live, 8)[0]
        self.list = [item for item in self.data if item['group'] == group]

        year = datetime.now().year

        for item in self.list:
            item.update({'action': 'play', 'isFolder': 'False'})

        for item in self.list:
            # bookmark = dict((k, v) for k, v in item.iteritems() if not k == 'next')
            # bookmark['bookmark'] = item['url']
            # bookmark_cm = {'title': 30080, 'query': {'action': 'addBookmark', 'url': json.dumps(bookmark)}}
            r_and_c_cm = {'title': 30082, 'query': {'action': 'refresh_and_clear'}}
            item.update(
                {
                    'cm': [r_and_c_cm], 'year': year, 'duration': None, 'fanart': fanart
                }
            )

        self.list = sorted(self.list, key=lambda k: k['title'].lower())

        directory.add(self.list, argv=self.argv)
