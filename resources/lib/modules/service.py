# -*- coding: utf-8 -*-

# AliveGR Addon
# Author Twilight0
# SPDX-License-Identifier: GPL-3.0-only
# See LICENSES/GPL-3.0-only for more information.

import os
import sys
import hashlib
import xbmc
from xbmcaddon import Addon

if sys.version_info[0] == 3:
    from xbmcvfs import translatePath
else:
    from xbmc import translatePath

addon_id = 'plugin.video.AliveGR'
new_settings = 'special://home/addons/{}/resources/texts/matrix_settings.xml'.format(addon_id)
old_settings = 'special://home/addons/{}/resources/texts/leia_settings.xml'.format(addon_id)
settings_path = 'special://home/addons/{}/resources/settings.xml'.format(addon_id)
datapath = 'special://profile/addon_data/plugin.video.AliveGR/'
__addon__ = Addon(addon_id)
monitor = xbmc.Monitor
it_exists = os.path.exists


class WatchChanges(xbmc.Monitor):

    def __init__( self):

        xbmc.Monitor.__init__(self)

    def action(self):

        if xbmc.getInfoLabel('Container.PluginName') == addon_id:
            xbmc.executebuiltin('Container.Refresh')

    def onSettingsChanged(self):

        self.action()


class Daemon:

    def __init__(self):

        self._service_setup()

        while not self.Monitor.abortRequested():

            with open(translatePath(settings_path)) as settings_f:

                text = settings_f.read()

                try:
                    md5sum = hashlib.md5(text).hexdigest()
                except TypeError:
                    md5sum = hashlib.md5(bytes(text, encoding='utf-8')).hexdigest()

                if md5sum == 'ede0024610bda958e525b095b061c6bf':

                    if sys.version_info[0] == 3:

                        new_f = open(translatePath(new_settings))
                        settings_text = new_f.read()

                        with open(translatePath(settings_path), 'w') as f:
                            f.write(settings_text)

                        new_f.close()

                    else:

                        old_f = open(translatePath(old_settings))
                        settings_text = old_f.read()

                        with open(translatePath(settings_path), 'w') as f:
                            f.write(settings_text)

                        old_f.close()

            if self.Monitor.waitForAbort(360):
                break

    def _service_setup(self):

        self.Monitor = WatchChanges()
        self._get_settings()

    def _get_settings(self):

        self.show_clear_bookmarks = __addon__.getSetting('show_clear_bookmarks')
        self.paginate_items = __addon__.getSetting('paginate_items')
        self.wrap_labels = __addon__.getSetting('wrap_labels')
        self.lang_split = __addon__.getSetting('lang_split')
        self.theme = __addon__.getSetting('theme')
        self.show_live = __addon__.getSetting('show_live')
        self.show_m3u = __addon__.getSetting('show_m3u')
        self.show_pvr = __addon__.getSetting('show_pvr')
        self.show_networks = __addon__.getSetting('show_networks')
        self.show_news = __addon__.getSetting('show_news')
        self.show_movies = __addon__.getSetting('show_movies')
        self.show_short_films = __addon__.getSetting('show_short_films')
        self.show_series = __addon__.getSetting('show_series')
        self.show_shows = __addon__.getSetting('show_shows')
        self.show_theater = __addon__.getSetting('show_theater')
        self.show_docs = __addon__.getSetting('show_docs')
        self.show_sports = __addon__.getSetting('show_sports')
        self.show_kids = __addon__.getSetting('show_kids')
        self.show_misc = __addon__.getSetting('show_history')
        self.show_radio = __addon__.getSetting('show_radio')
        self.show_music = __addon__.getSetting('show_music')
        self.show_search = __addon__.getSetting('show_search')
        self.show_bookmarks = __addon__.getSetting('show_bookmarks')
        self.show_settings = __addon__.getSetting('show_settings')
        self.show_quit = __addon__.getSetting('show_quit')
        self.live_tv_mode = __addon__.getSetting('live_tv_mode')
        self.show_live_switcher = __addon__.getSetting('show_live_switcher')
        self.show_vod_switcher = __addon__.getSetting('show_vod_switcher')
        self.show_pic_switcher = __addon__.getSetting('show_pic_switcher')


if __name__ == '__main__':

    Daemon()
