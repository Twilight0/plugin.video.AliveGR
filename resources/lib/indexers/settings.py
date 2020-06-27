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

from ..modules.themes import iconname
from ..modules.constants import ART_ID, PAYPAL, PATREON
from tulip import control, directory


class Indexer:

    def __init__(self):

        self.list = []

    def menu(self):

        self.list = [
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30255),
                'action': 'info',
                'icon': control.addonInfo('icon')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30003),
                'action': 'openSettings',
                'icon': iconname('settings'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30005),
                'action': 'openSettings',
                'query': '1.0',
                'icon': iconname('settings'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30004),
                'action': 'openSettings',
                'query': '2.0',
                'icon': iconname('monitor'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30138),
                'action': 'openSettings',
                'query': '3.0',
                'icon': iconname('settings'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30011) + ': ' + control.lang(30017),
                'action': 'openSettings',
                'query': '4.0',
                'icon': iconname('settings'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30115),
                'action': 'openSettings',
                'query': '5.0',
                'icon': iconname('godmode'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30350),
                'action': 'toggle_alt',
                'icon': iconname('monitor'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30320) + ': ' + control.lang(30272),
                'action': 'input_stream_addons',
                'icon': iconname('monitor')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30056),
                'action': 'cache_clear',
                'icon': iconname('empty'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30135),
                'action': 'purge_bookmarks',
                'icon': iconname('empty'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30134),
                'action': 'reset_idx',
                'icon': iconname('settings'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30110),
                'action': 'changelog',
                'icon': control.addonInfo('icon'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30319),
                'action': 'global_settings',
                'icon': control.addonmedia(addonid=ART_ID, theme='icons', icon='kodi.png', media_subfolder=False),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
        ]

        if control.condVisibility('Window.IsVisible(programs)'):

            for i in self.list:
                i.update({'cm': [{'title': 30307, 'query': {'action': 'root'}}]})

        if control.condVisibility('System.HasAddon(script.module.resolveurl)'):

            rurl = {
                'title': control.lang(30111),
                'action': 'other_addon_settings',
                'query': 'script.module.resolveurl',
                'icon': control.addon(id='script.module.resolveurl').getAddonInfo('icon'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }

            self.list.insert(-2, rurl)

        directory.add(self.list)

    def info(self):

        separator = '[CR]' if control.setting('wrap_labels') == '0' else ' '

        try:
            disclaimer = control.addonInfo('disclaimer').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
            disclaimer = control.addonInfo('disclaimer')

        self.list = [
            {
                'title': control.lang(30331),
                'action': 'welcome',
                'icon': control.addonInfo('icon'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30105),
                'action': 'dmca',
                'plot': disclaimer,
                'icon': control.addonmedia(
                    addonid=ART_ID, theme='icons', icon='dmca.png', media_subfolder=False
                ),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30290),
                'action': 'pp',
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30295),
                'action': 'toggle_debug',
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30341),
                'action': 'kodi_log_upload',
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30296),
                'action': 'force',
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30260).format(separator),
                'action': 'open_link',
                'url': 'https://bitbucket.org/thgiliwt/plugin.video.alivegr/issues',
                'plot': 'Git repo',
                'icon': control.addonmedia(
                    addonid=ART_ID, theme='icons', icon='bitbucket.png', media_subfolder=False
                ),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30141) + ': [COLOR cyan]' + PAYPAL + '[/COLOR]',
                'action': 'open_link',
                'url': PAYPAL,
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30142) + ': [COLOR cyan]' + PATREON + '[/COLOR]',
                'action': 'open_link',
                'url': PATREON,
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30256).format(separator, control.addonInfo('version')),
                'action': 'force',
                'plot': control.lang(30265),
                'icon': control.addonInfo('icon'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30257).format(separator, control.addon('script.module.tulip').getAddonInfo('version')),
                'action': 'force',
                'plot': control.lang(30265),
                'icon': control.addon('script.module.tulip').getAddonInfo('icon'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30294).format(separator, control.addon('script.module.streamlink.base').getAddonInfo('version')),
                'action': 'force',
                'image': control.addon('script.module.streamlink.base').getAddonInfo('icon'),
                'plot': control.lang(30265),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30258).format(separator, control.addon('xbmc.addon').getAddonInfo('version').rpartition('.')[0]),
                'action': 'system_info',
                'plot': control.lang(30263),
                'icon': control.addonmedia(addonid=ART_ID, theme='icons', icon='kodi.png', media_subfolder=False),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
        ]

        try:

            rurl_enabled = control.addon_details('script.module.resolveurl').get('enabled')

        except Exception:

            rurl_enabled = False

        if rurl_enabled:

            resolveurl = {

                'title': control.lang(30264).format(separator, control.addon('script.module.resolveurl').getAddonInfo('version')),
                'action': 'other_addon_settings',
                'query': 'script.module.resolveurl',
                'plot': control.lang(30265),
                'icon': control.addon('script.module.resolveurl').getAddonInfo('icon'),
                'isFolder': 'False',
                'isPlayable': 'False'

            }

            self.list.insert(-2, resolveurl)

        directory.add(self.list, content='movies')

    def input_stream_addons(self):

        self.list = [
            {
                'title': control.lang(30253),
                'action': 'isa_enable',
                'isFolder': 'False',
                'isPlayable': 'False',
                'cm': [{'title': 30253, 'query': {'action': 'other_addon_settings', 'query': 'inputstream.adaptive'}}]
            }
            ,
            {
                'title': control.lang(30273),
                'action': 'other_addon_settings',
                'query': 'inputstream.adaptive',
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30275),
                'action': 'rtmp_enable',
                'isFolder': 'False',
                'isPlayable': 'False'
            }
        ]

        directory.add(self.list)
