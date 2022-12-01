# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import, unicode_literals

import sys
from ..modules.themes import iconname
from ..modules.constants import ART_ID, PAYPAL, SUPPORT
from ..modules.utils import changelog
from tulip import control, directory


class Indexer:

    def __init__(self):

        self.list = []

    def menu(self):

        self.list = [
            {
                'title': '[B]' + control.addonInfo('name') + ': ' + control.lang(30255) + '[/B]',
                'action': 'info',
                'icon': control.addonInfo('icon')
            }
            ,
            {
                'title': '[B]' + control.addonInfo('name') + ': ' + control.lang(30017) + '[/B]',
                'action': 'actions',
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
                'title': control.addonInfo('name') + ': ' + control.lang(30115),
                'action': 'openSettings',
                'query': '4.0',
                'icon': iconname('godmode'),
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

        directory.add(self.list)

    def actions(self):

        self.list = [
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30350),
                'action': 'toggle_alt',
                'icon': iconname('monitor'),
                'isFolder': 'False',
                'isPlayable': 'False'
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
                'action': 'clear_bookmarks',
                'icon': iconname('empty'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30408),
                'action': 'clear_search_history',
                'icon': iconname('empty'),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + control.lang(30471),
                'action': 'clear_playback_history',
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
                'title': control.lang(30320) + ': ' + control.lang(30272),
                'action': 'input_stream_addons',
                'icon': iconname('monitor')
            }
            ,
            {
                'title': '[B]' + control.lang(30340) + '[/B]',
                'action': 'changelog',
                'icon': control.addonInfo('icon'),
                'plot': changelog(get_text=True),
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
                'title': control.lang(30472),
                'action': 'skin_debug',
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30469),
                'action': 'apply_settings_xml',
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
        ]

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
                'title': control.lang(30260).format(separator),
                'action': 'open_link',
                'url': SUPPORT,
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

                'title': control.lang(30264).format(separator, control.addon('script.module.resolveurl').getAddonInfo('version')),
                'action': 'other_addon_settings',
                'query': 'script.module.resolveurl',
                'plot': control.lang(30265),
                'icon': control.addon('script.module.resolveurl').getAddonInfo('icon'),
                'isFolder': 'False',
                'isPlayable': 'False'

            }
            ,
            {
                'title': control.lang(30258).format(separator, control.kodi_version()),
                'action': 'system_info',
                'plot': control.lang(30263),
                'icon': control.addonmedia(addonid=ART_ID, theme='icons', icon='kodi.png', media_subfolder=False),
                'isFolder': 'False',
                'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30303).format(separator, '.'.join([str(sys.version_info[0]), str(sys.version_info[1]), str(sys.version_info[2])])),
                'action': 'system_info',
                'plot': control.lang(30263),
                'image': 'https://www.python.org/static/opengraph-icon-200x200.png',
                'isFolder': 'False',
                'isPlayable': 'False'
            }
        ]

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
