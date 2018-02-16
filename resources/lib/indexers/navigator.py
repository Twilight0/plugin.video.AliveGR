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


from tulip import control, directory, cache, client, bookmarks
from tulip.log import *
from tulip.init import syshandle, sysaddon
from ..modules.constants import art_id, yt_addon, sdik, radio_addons
from ..modules.themes import iconname
from ..modules.helpers import reset_idx as reset
from ..modules.helpers import thgiliwt


class Main:

    def __init__(self):

        self.list = []

    def root(self):

        self.list = [
            {
                'title': control.lang(30001),
                'action': 'live_tv',
                'icon': iconname('monitor'),
                'id': '30001'
            }
            ,
            {
                'title': control.lang(30036),
                'action': 'pvr_client',
                'icon': iconname('guide'),
                'id': '30036'
            }
            ,
            {
                'title': control.lang(30008),
                'action': 'networks',
                'icon': iconname('networks'),
                'id': '30008'
            }
            ,
            {
                'title': control.lang(30123),
                'action': 'news',
                'icon': iconname('news'),
                'id': '30123'
            }
            ,
            {
                'title': control.lang(30031),
                'action': 'movies',
                'icon': iconname('movies'),
                'id': '30031'
            }
            ,
            {
                'title': control.lang(30083),
                'action': 'short_films',
                'icon': iconname('short'),
                'id': '30083'
            }
            ,
            {
                'title': control.lang(30030),
                'action': 'series',
                'icon': iconname('series'),
                'id': '30030'
            }
            ,
            {
                'title': control.lang(30063),
                'action': 'shows',
                'icon': iconname('shows'),
                'id': '30063'
            }
            ,
            {
                'title': control.lang(30068),
                'action': 'theater',
                'icon': iconname('theater'),
                'id': '30068'
            }
            ,
            {
                'title': control.lang(30079),
                'action': 'documentaries',
                'icon': iconname('documentaries'),
                'id': '30079'
            }
            ,
            {
                'title': control.lang(30094),
                'action': 'sports',
                'icon': iconname('sports'),
                'id': '30094'
            }
            ,
            {
                'title': control.lang(30032),
                'action': 'kids',
                'icon': iconname('kids'),
                'id': '30032'
            }
            ,
            {
                'title': control.lang(30012),
                'action': 'miscellany',
                'icon': iconname('miscellany'),
                'id': '30012'
            }
            ,
            {
                'title': control.lang(30002),
                'action': 'radio',
                'icon': iconname('radios'),
                'id': '30002'
            }
            ,
            {
                'title': control.lang(30125),
                'action': 'music',
                'icon': iconname('music'),
                'id': '30125'
            }
            ,
            {
                'title': control.lang(30095).partition(' ')[0],
                'action': 'search',
                'icon': iconname('search'),
                'id': '30095'
            }
            ,
            {
                'title': control.lang(30055),
                'action': 'bookmarks',
                'icon': iconname('bookmarks'),
                'id': '30055'
            }
            ,
            {
                'title': control.lang(30137),
                'action': 'openSettings&query=0.0' if control.setting('old_settings') == 'true' else 'settings',
                'icon': iconname('settings'),
                'id': '30137'
            }
        ]

        if control.setting('show_live') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30001']
        if control.setting('show_pvr') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30036']
        if control.setting('show_networks') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30008']
        if control.setting('show_news') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30123']
        if control.setting('show_movies') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30031']
        if control.setting('show_short_films') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30083']
        if control.setting('show_series') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30030']
        if control.setting('show_shows') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30063']
        if control.setting('show_theater') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30068']
        if control.setting('show_docs') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30079']
        if control.setting('show_sports') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30094']
        if control.setting('show_kids') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30032']
        if control.setting('show_misc') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30012']
        if control.setting('show_radio') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30002']
        if control.setting('show_music') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30125']
        if control.setting('show_search') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30095']
        if control.setting('show_bookmarks') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30055']
        if control.setting('show_settings') == 'false':
            self.list = [d for d in self.list if d.get('id') != '30137']

        for item in self.list:
            refresh = {'title': 30054, 'query': {'action': 'refresh'}}
            cache_clear = {'title': 30056, 'query': {'action': 'cache_clear'}}
            reset_idx = {'title': 30134, 'query': {'action': 'reset_idx'}}
            settings = {'title': 30011, 'query': {'action': 'openSettings'}}
            tools = {'title': 30137, 'query': {'action': 'tools_menu'}}
            ii_cm = {'title': 30255, 'query': {'action': 'call_info'}}
            item.update({'cm': [ii_cm, refresh, cache_clear, reset_idx, settings, tools]})

        from ..modules.tools import checkpoint
        checkpoint()

        log_debug('Main menu loaded, have fun...')
        log_debug('Tulip libraries version ~ ' + control.addon('script.module.tulip').getAddonInfo('version'))

        if control.setting('reset-idx') == 'true':
            reset(notify=False)

        directory.add(self.list, content='addons')

    def audio(self):

        self.list = [
            {
                'title': control.lang(30002),
                'action': 'radio',
                'icon': iconname('radios')
            }
            ,
            {
                'title': control.lang(30125),
                'action': 'music',
                'icon': iconname('music')
            }
        ]

        for item in self.list:
            refresh = {'title': 30054, 'query': {'action': 'refresh'}}
            cache_clear = {'title': 30056, 'query': {'action': 'cache_clear'}}
            reset_idx = {'title': 30134, 'query': {'action': 'reset_idx'}}
            settings = {'title': 30011, 'query': {'action': 'openSettings'}}
            tools = {'title': 30137, 'query': {'action': 'tools_menu'}}
            item.update({'cm': [refresh, cache_clear, reset_idx, settings, tools]})

        log_debug('Plugin started as music addon, have fun...')
        log_debug('Tulip libraries version ~ ' + control.addon('script.module.tulip').getAddonInfo('version'))

        directory.add(self.list)


class Submenus:

    def __init__(self):

        self.list = []; self.data = []
        self.misc = 'AbthnL55WYsxWZjNXat9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'

    def bookmarks(self):

        import json
        from .gm import movies_link, theater_link, shortfilms_link

        self.data = bookmarks.get()

        if not self.data:

            log_debug('Bookmarks list is empty')
            na = [{'title': 30033, 'action':  None, 'icon': iconname('empty')}]
            directory.add(na)

        else:

            for i in self.data:

                if i['url'].startswith((movies_link, theater_link, shortfilms_link)):
                    if control.setting('action_type') == '1':
                        try:
                            del i['isFolder']
                        except:
                            pass
                        action = 'directory'
                    elif control.setting('action_type') == '2' and control.setting('auto_play') == 'false':
                        try:
                            del i['isFolder']
                        except:
                            pass
                        action = i['action']
                    else:
                        action = i['action']
                else:
                    action = i['action']

                i['action'] = action

                item = dict((k, v) for k, v in i.iteritems() if not k == 'next')
                item['delbookmark'] = i['url']
                i.update({'cm': [{'title': 30081, 'query': {'action': 'deleteBookmark', 'url': json.dumps(item)}}]})

            self.list = sorted(self.data, key=lambda k: k['title'].lower())

            directory.add(self.list)

    def networks(self):

        networks = [
            {
                'title': 'EPT',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='ert_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.ert.gr/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='ert_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'ANT1',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='ant1_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.antenna.gr/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='ant1_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'STAR',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='star_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.star.gr/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='star_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'ALPHA',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='alpha_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.alphatv.gr/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='alpha_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'SKAI',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='skai_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.skai.gr/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='skai_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'EURONEWS',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='euronews_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.euronews.com/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='euronews_fanart.jpg', media_subfolder=False)
            }
            # ,
            # {
            #     'title': 'VICE',
            #     'icon': control.addonmedia(addonid=art_id, theme='networks', icon='vice_icon.png', media_subfolder=False),
            #     'url': 'plugin://plugin.video.vice/',
            #     'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='vice_fanart.jpg', media_subfolder=False)
            # }
            ,
            {
                'title': 'NOVASPORTS',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='nova_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.novasports.gr/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='nova_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'GREEK VOICE',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='wzra48_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.greekvoice/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='wzra48_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'TORONTO CHANNELS',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='tc_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.Toronto-Channels/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='tc_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'MONTREAL GREEK TV',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='mg_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.montreal.greek-tv/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='mgtv_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'FAROS ON AIR',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='faros_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.faros.on-air/',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='faros_fanart.jpg', media_subfolder=False)
            }
        ]

        if control.infoLabel('System.AddonVersion(xbmc.python)') == '2.24.0':
            del networks[-2]

        for network in networks:

            list_item = control.item(label=network['title'])
            list_item.setArt({'icon': network['icon'], 'fanart': network['fanart']})
            url = network['url']
            self.list.append((url, list_item, True))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def documentaries(self):

        self.data = [
            {
                'title': control.lang(30041),
                'url': 'plugin://plugin.video.AliveGR/?action=listing&url=http://greek-movies.com/movies.php?g=6&y=&l=&p=',
                'icon': iconname('documentaries')
            }
            ,
            {
                'title': control.lang(30042),
                'url': 'plugin://plugin.video.AliveGR/?action=yt_documentaries',
                'icon': iconname('documentaries')
            }
            ]

        for item in self.data:
            list_item = control.item(label=item['title'])
            list_item.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            _url_ = item['url']
            isFolder = True
            self.list.append((_url_, list_item, isFolder))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

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

    def news(self):

        items = [
            {
                'title': control.lang(30230),
                'icon': 'http://downloadicons.net/sites/default/files/news-icon-53570.png',
                'url': '{0}?action=papers'.format(sysaddon),
                'fanart': control.addonInfo('fanart')
            }
            ,
            {
                'title': control.lang(30118),
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='ert_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.ert.gr/?action=episodes&url=http%3a%2f%2fwebtv.ert.gr%2fcategory%2fkatigories%2feidiseis%2f',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='ert_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30119),
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='ant1_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.antenna.gr/?action=news',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='ant1_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30120),
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='star_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.star.gr/?action=news',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='star_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30122),
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='alpha_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.alphatv.gr/?action=news',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='alpha_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30121),
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='skai_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.skai.gr/?action=news',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='skai_fanart.jpg', media_subfolder=False)
            }
            ,
            {
                'title': 'Euronews',
                'icon': control.addonmedia(addonid=art_id, theme='networks', icon='euronews_icon.png', media_subfolder=False),
                'url': 'plugin://plugin.video.euronews.com/?action=videos&url=%22methodName%22%3a%22content.getThemeDetails%22%2c%22params%22%3a%7b%22tId%22%3a%221%22%7d',
                'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='euronews_fanart.jpg', media_subfolder=False)
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

    def radio(self):

        for addon in radio_addons:
            li = control.item(label=addon['title'], iconImage=addon['icon'], thumbnailImage=addon['icon'])
            li.setInfo('music', {'title': addon['title']})
            li.setArt({'fanart': control.addonInfo('fanart')})
            url = addon['url']
            self.list.append((url, li, True))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def sports(self):

        self.list = [
            {
                'title': 30116,
                'action': 'sports_news',
                'icon': iconname('news')
            }
            ,
            {
                'title': 30117,
                'action': 'gm_sports',
                'icon': iconname('sports')
            }
            ]

        directory.add(self.list)

    def sports_news(self):

        self.data = [
                {
                    'title': 'EPT Sports',
                    'icon': control.addonmedia(addonid=art_id, theme='networks', icon='ert_icon.png', media_subfolder=False),
                    'url': 'plugin://plugin.video.ert.gr/?action=episodes&url=http%3a%2f%2fwebtv.ert.gr%2fcategory%2fkatigories%2fathlitika%2f',
                    'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='ert_fanart.jpg', media_subfolder=False)
                }
                ,
                {
                    'title': 'Skai Sports',
                    'icon': control.addonmedia(addonid=art_id, theme='networks', icon='skai_icon.png', media_subfolder=False),
                    'url': 'plugin://plugin.video.skai.gr/?action=sports',
                    'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='skai_fanart.jpg', media_subfolder=False)
                }
                ,
                {
                    'title': 'Euronews Sports',
                    'icon': control.addonmedia(addonid=art_id, theme='networks', icon='euronews_icon.png', media_subfolder=False),
                    'url': 'plugin://plugin.video.euronews.com/?action=videos&url=%22methodName%22%3a%22content.getThemeDetails%22%2c%22params%22%3a%7b%22tId%22%3a%228%22%7d',
                    'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='euronews_fanart.jpg', media_subfolder=False)
                }
                ,
                {
                    'title': 'NovaSports',
                    'icon': control.addonmedia(addonid=art_id, theme='networks', icon='nova_icon.png', media_subfolder=False),
                    'url': 'plugin://plugin.video.novasports.gr/',
                    'fanart': control.addonmedia(addonid=art_id, theme='networks', icon='nova_fanart.jpg', media_subfolder=False)
                }
        ]

        for item in self.data:
            list_item = control.item(label=item['title'])
            list_item.setArt({'icon': item['icon'], 'fanart': item['fanart']})
            _url_ = item['url']
            isFolder = True
            self.list.append((_url_, list_item, isFolder))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)


class Settings:

    def __init__(self):

        self.list = []; self.data = []

    def menu(self):

        self.list = [
            {
                'title': control.addonInfo('name') + ': ' + (control.lang(30255)),
                'action': 'info',
                'icon': control.addonInfo('icon')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + (control.lang(30003)),
                'action': 'openSettings',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + (control.lang(30005)),
                'action': 'openSettings',
                'query': '1.0',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + (control.lang(30004)),
                'action': 'openSettings',
                'query': '2.0',
                'icon': iconname('monitor')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + (control.lang(30138)),
                'action': 'openSettings',
                'query': '3.0',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.lang(30011) + ': ' + (control.lang(30017)),
                'action': 'openSettings',
                'query': '4.0',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + (control.lang(30115)),
                'action': 'openSettings',
                'query': '5.0',
                'icon': iconname('godmode')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + (control.lang(30056)),
                'action': 'cache_clear',
                'icon': iconname('empty')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + (control.lang(30135)),
                'action': 'purge_bookmarks',
                'icon': iconname('empty')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + (control.lang(30134)),
                'action': 'reset_idx',
                'icon': iconname('settings')
            }
            ,
            {
                'title': control.addonInfo('name') + ': ' + (control.lang(30110)),
                'action': 'changelog',
                'icon': control.addonInfo('icon')
            }
            ,
            {
                'title': 'ResolveURL' + ': ' + control.lang(30111).rpartition(' (')[0],
                'action': 'other_addon_settings',
                'query': 'script.module.resolveurl',
                'icon': control.addon(id='script.module.resolveurl').getAddonInfo('icon')
            }
        ]

        directory.add(self.list)

    def info(self):

        try:
            disclaimer = control.addonInfo('disclaimer').decode('utf-8')
        except AttributeError:
            disclaimer = control.addonInfo('disclaimer')

        self.list = [
            {
                'title': control.lang(30105),
                'action': 'dmca',
                'plot': disclaimer,
                'icon': control.addonmedia(
                    addonid=art_id, theme='icons', icon='dmca.png', media_subfolder=False
                )
            }
            ,
            {
                'title': control.lang(30260),
                'action': 'none',
                'plot': 'Git repo',
                'icon': control.addonmedia(
                    addonid=art_id, theme='icons', icon='bitbucket.png', media_subfolder=False
                )
            }
            ,
            {
                'title': control.lang(30259),
                'action': 'none',
                'plot': 'RSS feed: https://twitrss.me/twitter_user_to_rss/?user=TwilightZer0',
                'icon': control.addonmedia(addonid=art_id, theme='icons', icon='twitter.png', media_subfolder=False)
            }
            ,
            {
                'title': control.lang(30256).format(control.addonInfo('version')),
                'action': 'force',
                'plot': control.lang(30265),
                'icon': control.addonInfo('icon')
            }
            ,
            {
                'title': control.lang(30257).format(control.addon('script.module.tulip').getAddonInfo('version')),
                'action': 'force',
                'plot': control.lang(30265),
                'icon': control.addon('script.module.tulip').getAddonInfo('icon')
            }
            ,
            {
                'title': control.lang(30264).format(control.addon('script.module.resolveurl').getAddonInfo('version')),
                'action': 'force',
                'plot': control.lang(30265),
                'icon': control.addon('script.module.resolveurl').getAddonInfo('icon')
            }
            ,
            {
                'title': control.lang(30258).format(control.addon('xbmc.addon').getAddonInfo('version').rpartition('.')[0]),
                'action': 'system_info',
                'plot': control.lang(30263),
                'icon': control.addonmedia(addonid=art_id, theme='icons', icon='kodi.png', media_subfolder=False)
            }
        ]

        control.execute('Container.SetViewMode(50)')
        directory.add(self.list, content='movies')


class Kids:

    def __init__(self):

        self.list = []; self.data = []

    def kids(self):

        try:
            if control.condVisibility('System.HasAddon({0})'.format(sdik)):
                import sys
                sys.path.extend([control.join(control.addon(id=sdik).getAddonInfo('path'), 'resources', 'lib')])
                from extension import kids_indexer
        except:
            pass

        self.data = [
            {
                'title': control.lang(30078),
                'url': 'plugin://plugin.video.AliveGR/?action=kids_live',
                'icon': iconname('kids_live')
            }
            ,
            {
                'title': control.lang(30074),
                'url': '{0}?action={1}'.format(sysaddon, 'cartoon_collection'),
                'icon': iconname('cartoon_collection')
            }
            ,
            {
                'title': control.lang(30075),
                'url': '{0}?action={1}'.format(sysaddon, 'educational'),
                'icon': iconname('educational')
            }
            ,
            {
                'title': control.lang(30076),
                'url': '{0}?action={1}'.format(sysaddon, 'kids_songs'),
                'icon': iconname('kids_songs')
            }
        ]

        try:
            if control.condVisibility('System.HasAddon({0})'.format(sdik)):
                extended = [
                    dict(
                        (k, control.lang(v) if (k == 'title') else v) for k, v in item.items()
                    ) for item in kids_indexer
                ]
                extended = [
                    dict((k, iconname(v) if (k == 'icon') else v) for k, v in item.items()) for item in extended
                ]
                self.data = [self.data[0]] + extended + self.data[1:]
        except:
            pass

        for item in self.data:
            li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            self.list.append((item['url'], li, True))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def cartoon_collection(self):

        self.data = [
            {
                'title': u'Collection Miscellaneous 1 - Συλλογή Διάφορα 1',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL4075DA390F6E82B1/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/MPtZ_VHNg34/mqdefault.jpg'
            }
            ,
            {
                'title': u'Collection Miscellaneous 2 - Συλλογή Διάφορα 2',
                'url': '{0}/channel/UCzU4decItAYA0omjxNiIHbg/playlists/'.format(yt_addon),
                'icon': 'https://yt3.ggpht.com/-W3Asi5ry2Rs/AAAAAAAAAAI/AAAAAAAAAAA/QzJaKZpLEtw/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Classical Films - Κλασσικά Κινηματογραφημένα',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PLF0A5359586D57FE8/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/X9RxumkELfE/mqdefault.jpg'
            }
            ,
            {
                'title': u'Mythology - Μυθολογία',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL3E1C926284F12F32/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/kpd-Z_VK6Jc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Aesop\'s Fables - Αισώπου Μύθοι',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL4FF9F773D3596E60/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/Gkr-pV_gY48/mqdefault.jpg'
            }
            ,
            {
                'title': u'Greek Fairy Tales - Ελληνικά Παραμύθια',
                'url': '{0}/channel/UC9VmWb5Wd5sc4E4k1CevEug/'.format(yt_addon),
                'icon': 'https://yt3.ggpht.com/-n8KoGQ6U_zc/AAAAAAAAAAI/AAAAAAAAAAA/SoUWvy5-Tb8/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Fairy Tales & Songs - Παραμύθια και Τραγούδια',
                'url': '{0}/channel/UCClAFTnbGditvz9_7_7eumw/playlists/'.format(yt_addon),
                'icon': 'https://yt3.ggpht.com/-mBPhzUcDIHM/AAAAAAAAAAI/AAAAAAAAAAA/pNQi44zsLq8/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
        ]

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
            self.list.append((item['url'], li, True))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def educational(self):

        self.data = [
            {
                'title': u'Learn about animals - Μάθε για τα ζώα',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRboPyGr30sIRMnc20C77ui/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/_fDdVYJA9Vk/mqdefault.jpg'
            }
            ,
            {
                'title': u'Secondary school education - Εκπαίδευση Δημοτικού Σχολείου',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LQvxn7RyUySvQy6C6hTUTXf/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/isxjo7M2h74/mqdefault.jpg'
            }
            ,
            {
                'title': u'Sexual Education for children - Σεξουαλική Αγωγή για παιδιά',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRy-LRQEeRdT_kf5iFdofsu/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/l9gN1F6S3bc/mqdefault.jpg'
            }
            ,
            {
                'title': u'World\'s Seven Ancient Miracles - Τα Επτά Θαύματα του Αρχαίου Κόσμου',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeThKG7GK1k2DRgB5im-vPHc/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/5nEDQ_jYJIo/mqdefault.jpg'
            }
            ,
            {
                'title': u'The land of Knowledge - Η Χώρα των Γνώσεων',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeS-ZVlk0vgNdx5igsFvYN8s/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/K-Ba9l2uDDk/mqdefault.jpg'
            }
            ,
            {
                'title': u'Ancient Egypt - Αρχαία Αίγυπτος',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeTrRcdIHjtziNEkqPqalUOa/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/pV8EMy8gaXI/mqdefault.jpg'
            }
            ,
            {
                'title': u'Explorers & Seafarers - Εξερευνητές και Θαλασσοπόροι',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeQRBb7ayyynWgYEUbkQKPpJ/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/SPdnnVNZgwc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Mini Encyclopaedia - Μικρή Εγκυκλοπαίδεια',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeTLMi1bFqLC_cn5ZAtqSvlV/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/o31_SNQFYhc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Miscellaneous Documentaties - Διάφορα Ντοκυμαντέρ',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRY94Yga82ZYsPJ9Xbe3OiZ/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/Vf_o_Q5ZQRg/mqdefault.jpg'
            }
            ,
            {
                'title': u'Learn Ancient Greek - Μάθετε Αρχαία Ελληνικά',
                'url': '{0}/channel/UC5quWsvOBNUaR-Duv3K-JFA/playlist/PLxqCshQO3A1HnlHwxda3wX_kzY-C0gpZq/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/st01jb_Xb7g/mqdefault.jpg'
            }
            ,
            {
                'title': u'Drawings - Ζωγραφιές',
                'url': '{0}/channel/UC5quWsvOBNUaR-Duv3K-JFA/playlist/PLxqCshQO3A1FmjzGXbfIjTSXcysLfPfKM/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/GdiLSXePno8/mqdefault.jpg'
            }
        ]

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
            self.list.append((item['url'], li, True))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def kids_songs(self):

        self.data = [
            {
                'title': u'Zouzounia TV kids songs - Παιδικά Τραγούδια από τα Ζουζούνια',
                'url': 'plugin://plugin.video.zouzounia.tv/',
                'icon': 'https://yt3.ggpht.com/-zhH35bOsqec/AAAAAAAAAAI/AAAAAAAAAAA/LxUO6o-ZHPc/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Greek songs with lyrics No.1 - Ελληνικά παιδικά τραγούδια με στίχους No.1',
                'url': '{0}/channel/UCUmGu9Ncu5NeaEjwpLXW0PQ/'.format(yt_addon),
                'icon': 'https://yt3.ggpht.com/-MVbyrB7DJrY/AAAAAAAAAAI/AAAAAAAAAAA/WjLUCzyX3zI/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Greek songs with lyrics No.2 - Ελληνικά παιδικά τραγούδια με στίχους No.2',
                'url': '{0}/channel/UCyENiZwRYzfXzbwP-Mxk9oA/'.format(yt_addon),
                'icon': 'https://yt3.ggpht.com/-Jdrq5I2r5Tc/AAAAAAAAAAI/AAAAAAAAAAA/z7IPqFS7jqA/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Christmas songs - Χριστουγεννιάτικα Τραγούδια',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LQJIp9hY-4ESH6P1PVW34uB/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/WhQy0aZ22Tc/mqdefault.jpg'
            }
            ,
            {
                'title': u'The party\'s songs - Τα τραγούδια της παρέας',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRsQ-umYdnXPrTzclN0vsPh/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/V1pdBZaF3cc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Greek Karaoke - Ελληνικό Καραόκε',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRlD0w1GXbitRL6sbyMscVi/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/Iz5P8xJel-U/mqdefault.jpg'
            }
            ,
            {
                'title': u'Karaoke for English Learning - Μαθαίνω Αγγλικά με καραόκε',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeSL-M5Q0qG3Eszj0I1O98bT/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/L2atYpQ7Zbg/mqdefault.jpg'
            }
            ,
            {
                'title': u'Learning Music for Kids - Μαθαίνω Μουσική, για παιδιά',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRr5VH-HylSX89MHXQ_KyS0/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/w5tF5J_BNfI/mqdefault.jpg'
            }
        ]

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
            self.list.append((item['url'], li, True))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

