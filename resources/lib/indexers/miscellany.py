# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''
from __future__ import absolute_import, unicode_literals

from tulip import client, control
from tulip.init import syshandle
from ..modules.utils import thgiliwt
from ..modules.constants import YT_ADDON, cache_duration, cache_method


class Indexer:

    def __init__(self):

        self.list = [] ; self.data = []
        self.misc = 'wWb45SeuFGbsV2YzlWbvcXYy9Cdl5mLydWZ2lGbh9yL6MHc0RHa'

    @cache_method(cache_duration(1440))
    def misc_list(self):

        if control.setting('debug') == 'false':

            playlist = client.request(
                thgiliwt('=' + self.misc), headers={'User-Agent': 'AliveGR, version: ' + control.version()}
            )

        else:

            if control.setting('local_remote') == '0':
                local = control.setting('misc_local')
                try:
                    with open(local, encoding='utf-8') as xml:
                        playlist = xml.read()
                except Exception:
                    with open(local) as xml:
                        playlist = xml.read()
            elif control.setting('local_remote') == '1':
                playlist = client.request(control.setting('misc_remote'))
            else:
                playlist = client.request(thgiliwt('==' + self.misc))

        self.data = client.parseDOM(playlist, 'item')

        for item in self.data:

            title = client.parseDOM(item, 'title')[0]
            icon = client.parseDOM(item, 'icon')[0]
            url = client.parseDOM(item, 'url')[0]
            url = url.replace('https://www.youtube.com/channel', '{0}/channel'.format(YT_ADDON))
            url = '/?'.join([url, 'addon_id={}'.format(control.addonInfo('id'))])

            item_data = {'title': title, 'icon': icon, 'url': url}

            self.list.append(item_data)

        return self.list

    def miscellany(self):

        self.data = self.misc_list()

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

        control.addItems(syshandle, self.list)
        control.directory(syshandle)
