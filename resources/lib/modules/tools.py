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

import pyxbmct, re
from tulip import control, client, cache
from .helpers import thgiliwt, cache_clear, i18n, reset_idx, leved
from .kodi import skin_name, force
from .constants import API_KEYS, FACEBOOK, TWITTER, WEBSITE
from os import path
from random import choice
from time import time


########################################################################################################################

iptv_folder = control.transPath('special://profile/addon_data/pvr.iptvsimple')
vtpi = 'wWb45ycn5Wa0RXZz9ld0BXavcXYy9Cdl5mLydWZ2lGbh9yL6MHc0RHa'


def setup_iptv():

    xbmc_path = control.join('special://xbmc', 'addons', 'pvr.iptvsimple')
    home_path = control.join('special://home', 'addons', 'pvr.iptvsimple')

    def install():

        if control.conditional_visibility('System.Platform.Linux') and not (path.exists(control.transPath(xbmc_path)) or path.exists(control.transPath(home_path))):

            control.okDialog(heading='AliveGR', line1=control.lang(30323))

            return False

        elif path.exists(control.transPath(xbmc_path)) or path.exists(control.transPath(home_path)):

            return True

        elif control.kodi_version() >= 18.0 and not control.condVisibility('System.HasAddon(pvr.iptvsimple)'):

            control.execute('InstallAddon(pvr.iptvsimple)')

            return True

        elif control.condVisibility('System.HasAddon(pvr.iptvsimple)'):

            return 'enabled'

        else:

            return False

    def setup_client(apply=False):

        url = thgiliwt('=' + vtpi)

        if apply:

            xml = client.request(url)

            settings = re.findall(r'id="(\w*?)" value="(\S*?)"', xml)

            for k, v in settings:

                control.addon('pvr.iptvsimple').setSetting(k, v)

        else:

            if not path.exists(iptv_folder):
                control.makeFile(iptv_folder)

            client.retriever(url, control.join(iptv_folder, "settings.xml"))

    if path.exists(control.join(iptv_folder, 'settings.xml')):

        integer = 30021

    else:

        integer = 30023

    if control.yesnoDialog(line1=control.lang(integer), line2='', line3=control.lang(30022)):

        success = install()

        if success:

            setup_client(apply=success == 'enabled')
            control.infoDialog(message=control.lang(30024), time=2000)
            enable_iptv()
            enable_proxy_module()

        else:

            control.okDialog('AliveGR', control.lang(30410))

    else:

        control.infoDialog(message=control.lang(30029), time=2000)


def enable_iptv():

    xbmc_path = control.join('special://xbmc', 'addons', 'pvr.iptvsimple')
    home_path = control.join('special://home', 'addons', 'pvr.iptvsimple')

    if control.condVisibility('Pvr.HasTVChannels') and (path.exists(control.transPath(xbmc_path)) or path.exists(control.transPath(home_path))) and control.addon_details('pvr.iptvsimple').get('enabled'):

        control.infoDialog(message=control.lang(30407), time=4000)

    elif not path.exists(control.join(iptv_folder, 'settings.xml')):

        control.infoDialog(message=control.lang(30409), time=4000)

    else:

        if control.yesnoDialog(line1=control.lang(30406), line2='', line3=''):

            control.enable_addon('pvr.iptvsimple')

            if control.infoLabel('System.AddonVersion(xbmc.python)') == '2.24.0':

                control.execute('StartPVRManager')


def enable_proxy_module():

    if control.condVisibility('System.HasAddon(service.streamlink.proxy)'):

        control.infoDialog(control.lang(30143))

    else:

        if control.infoLabel('System.AddonVersion(xbmc.python)') == '2.24.0':

            control.execute('RunPlugin(plugin://service.streamlink.proxy/)')

        else:

            control.execute('InstallAddon(service.streamlink.proxy)')


def setup_various_keymaps(keymap):

    keymap_settings_folder = control.transPath('special://profile/keymaps')

    if not path.exists(keymap_settings_folder):
        control.makeFile(keymap_settings_folder)

    if keymap == 'previous':

        location = control.join(keymap_settings_folder, 'alivegr_tvguide.xml')

        lang_int = 30025

        def seq():

            previous_keymap = """<keymap>
    <tvguide>
        <keyboard>
            <key id="61448">previousmenu</key>
        </keyboard>
    </tvguide>
    <tvchannels>
        <keyboard>
            <key id="61448">previousmenu</key>
        </keyboard>
    </tvchannels>
</keymap>
"""
            try:
                with open(location, mode='w', encoding='utf-8') as f:
                    f.write(previous_keymap)
            except Exception:
                with open(location, 'w') as f:
                    f.write(previous_keymap)

    elif keymap == 'mouse':

        location = control.transPath(control.join('special://profile', 'keymaps', 'alivegr_mouse.xml'))

        lang_int = 30238

        def seq():

            string_start = '<keymap><slideshow><mouse>'
            string_end = '</mouse></slideshow></keymap>'
            string_for_left = '<leftclick>NextPicture</leftclick>'
            string_for_right = '<rightclick>PreviousPicture</rightclick>'
            string_for_middle = '<middleclick>Rotate</middleclick>'
            string_for_up = '<wheelup>ZoomIn</wheelup>'
            string_for_down = '<wheeldown>ZoomOut</wheeldown>'

            classes = [
                string_for_left, string_for_right, string_for_middle,
                string_for_up, string_for_down
            ]

            map_left = control.lang(30241)
            map_right = control.lang(30242)
            map_middle = control.lang(30243)
            map_up = control.lang(30244)
            map_down = control.lang(30245)

            keys = [
                map_left, map_right, map_middle, map_up, map_down
            ]

            control.okDialog(control.name(), control.lang(30240))

            indices = control.dialog.multiselect(control.name(), keys)

            if not indices:

                control.infoDialog(control.lang(30246))

            else:

                finalized = []

                for i in indices:
                    finalized.append(classes[i])

                joined = ''.join(finalized)

                to_write = string_start + joined + string_end

                try:
                    with open(location, mode='w', encoding='utf-8') as f:
                        f.write(to_write)
                except Exception:
                    with open(location, 'w') as f:
                        f.write(to_write)

                control.execute('Action(reloadkeymaps)')

    yes = control.yesnoDialog(control.lang(lang_int))

    if yes:

        if path.exists(location):

            choices = [control.lang(30248), control.lang(30249)]

            choice = control.selectDialog(choices, heading=control.lang(30247))

            if choice == 0:

                seq()
                control.okDialog(control.name(), control.lang(30027) + ', ' + (control.lang(30028)))
                control.infoDialog(control.lang(30402))
                control.execute('Action(reloadkeymaps)')

            elif choice == 1:

                control.deleteFile(location)
                control.infoDialog(control.lang(30402))
                control.execute('Action(reloadkeymaps)')

            else:

                control.infoDialog(control.lang(30403))

        else:

            seq()
            control.okDialog(control.name(), control.lang(30027) + ', ' + (control.lang(30028)))
            control.infoDialog(control.lang(30402))

            control.execute('Action(reloadkeymaps)')

    else:

        control.infoDialog(control.lang(30403))


def yt_setup():

    def seq():

        control.addon('plugin.video.youtube').setSetting('youtube.api.id', API_KEYS['id'])
        control.addon('plugin.video.youtube').setSetting('youtube.api.key', thgiliwt(API_KEYS['api_key']))
        control.addon('plugin.video.youtube').setSetting('youtube.api.secret', API_KEYS['secret'])

        control.infoDialog(message=control.lang(30402), time=3000)

    def wizard():

        control.addon('plugin.video.youtube').setSetting('kodion.setup_wizard', 'false')
        control.addon('plugin.video.youtube').setSetting('youtube.language', 'el')
        control.addon('plugin.video.youtube').setSetting('youtube.region', 'GR')
        control.infoDialog(message=control.lang(30402), time=3000)

    def yt_mpd():

        control.addon('plugin.video.youtube').setSetting('kodion.video.quality.mpd', 'true')
        control.addon('plugin.video.youtube').setSetting('kodion.mpd.videos', 'true')
        control.addon('plugin.video.youtube').setSetting('kodion.mpd.live_streams', 'true')
        control.infoDialog(message=control.lang(30402), time=3000)

########################################################################################################################

    def process():

        if control.addon('plugin.video.youtube').getSetting('youtube.api.enable') == 'true':

            if control.yesnoDialog(line1=control.lang(30069), line2=control.lang(30022), line3=''):
                seq()
            else:
                control.infoDialog(message=control.lang(30029), time=3000)

        else:

            if control.yesnoDialog(line1=control.lang(30070), line2=control.lang(30022), line3=''):
                seq()
            else:
                control.infoDialog(message=control.lang(30029), time=3000)

########################################################################################################################

    process()

    if control.yesnoDialog(line1=control.lang(30132), line2='', line3=''):

        wizard()

    if control.condVisibility('System.HasAddon(inputstream.adaptive)') and control.yesnoDialog(line1=control.lang(30287), line2='', line3=''):

        yt_mpd()


########################################################################################################################


def file_to_text(file_):

    try:

        with open(file_, encoding='utf-8') as text:
            result = text.read()

    except Exception:

        with open(file_) as text:
            result = text.read()

    return result


def changelog():

    if control.setting('changelog_lang') == '0' and 'Greek' in control.infoLabel('System.Language'):
        change_txt = 'changelog.el.txt'
    elif (
            control.setting('changelog_lang') == '0' and 'Greek' not in control.infoLabel('System.Language')
    ) or control.setting('changelog_lang') == '1':
        change_txt = 'changelog.en.txt'
    else:
        change_txt = 'changelog.el.txt'

    change_txt = control.join(control.addonPath, 'resources', 'texts', change_txt)

    control.dialog.textviewer(control.addonInfo('name') + ', ' + control.lang(30110), file_to_text(change_txt))


def dmca():

    location = control.join(
        control.transPath(control.addonInfo('path')), 'resources', 'texts', 'dmca_{0}.txt'.format(i18n())
    )

    control.dialog.textviewer(control.addonInfo('name'), file_to_text(location))


def pp():

    location = control.join(
        control.transPath(control.addonInfo('path')), 'resources', 'texts', 'pp_{0}.txt'.format(i18n())
    )

    control.dialog.textviewer(control.addonInfo('name'), file_to_text(location))


def disclaimer():

    try:
        text = control.addonInfo('disclaimer').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
        text = control.addonInfo('disclaimer')

    control.dialog.textviewer(control.addonInfo('name') + ', ' + control.lang(30129), text)


def do_not_ask_again():

    control.setSetting('new_version_prompt', 'false')

    control.okDialog('AliveGR', control.lang(30361))


class Card(pyxbmct.AddonDialogWindow):

    pyxbmct.skin.estuary = False if 'onfluence' in skin_name().lower() or 'aeon' in skin_name().lower() else True

    def __init__(self):

        # noinspection PyArgumentList
        super(Card, self).__init__(control.lang(30267).format(control.version()))

        self.changelog_button = None
        self.disclaimer_button = None
        self.close_button = None
        self.external_label = None
        self.description = None
        self.facebook_button = None
        self.twitter_button = None
        self.website_button = None
        self.setGeometry(854, 480, 8, 3)
        self.set_controls()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.set_navigation()

    def set_controls(self):

        image = pyxbmct.Image(control.fanart(), aspectRatio=2)
        self.placeControl(image, 0, 0, 5, 3)
        # Note
        self.description = pyxbmct.Label(control.lang(30328), alignment=2)
        self.placeControl(self.description, 5, 0, 2, 3)
        # Click to open label
        # self.external_label = pyxbmct.Label(control.lang(30131), alignment=pyxbmct.ALIGN_CENTER_Y | pyxbmct.ALIGN_CENTER_X)
        # self.placeControl(self.external_label, 6, 0, 1, 1)
        # Twitter button
        self.twitter_button = pyxbmct.Button('Twitter')
        self.placeControl(self.twitter_button, 6, 0)
        self.connect(self.twitter_button, lambda: control.open_web_browser(TWITTER))
        # Website
        self.website_button = pyxbmct.Button(control.lang(30333))
        self.placeControl(self.website_button, 6, 1)
        self.connect(self.website_button, lambda: control.open_web_browser(WEBSITE))
        # Facebook button
        self.facebook_button = pyxbmct.Button('Facebook')
        self.placeControl(self.facebook_button, 6, 2)
        self.connect(self.facebook_button, lambda: control.open_web_browser(FACEBOOK))
        # Close button
        self.close_button = pyxbmct.Button(control.lang(30329))
        self.placeControl(self.close_button, 7, 1)
        self.connect(self.close_button, self.close)
        # Changelog button
        self.changelog_button = pyxbmct.Button(control.lang(30110))
        self.placeControl(self.changelog_button, 7, 0)
        self.connect(self.changelog_button, lambda: changelog())
        # Disclaimer button
        self.disclaimer_button = pyxbmct.Button(control.lang(30129))
        self.placeControl(self.disclaimer_button, 7, 2)
        self.connect(self.disclaimer_button, lambda: disclaimer())

    def set_navigation(self):

        self.twitter_button.controlDown(self.changelog_button)
        self.twitter_button.controlLeft(self.facebook_button)
        self.twitter_button.controlRight(self.website_button)
        self.twitter_button.controlUp(self.changelog_button)

        self.website_button.controlRight(self.facebook_button)
        self.website_button.controlLeft(self.twitter_button)
        self.website_button.controlDown(self.close_button)
        self.website_button.controlUp(self.close_button)

        self.facebook_button.controlDown(self.disclaimer_button)
        self.facebook_button.controlRight(self.twitter_button)
        self.facebook_button.controlUp(self.disclaimer_button)
        self.facebook_button.controlLeft(self.website_button)

        self.close_button.controlLeft(self.changelog_button)
        self.close_button.controlRight(self.disclaimer_button)
        self.close_button.controlUp(self.website_button)
        self.close_button.controlDown(self.website_button)

        self.changelog_button.controlRight(self.close_button)
        self.changelog_button.controlLeft(self.disclaimer_button)
        self.changelog_button.controlUp(self.twitter_button)
        self.changelog_button.controlDown(self.twitter_button)

        self.disclaimer_button.controlLeft(self.close_button)
        self.disclaimer_button.controlRight(self.changelog_button)
        self.disclaimer_button.controlUp(self.facebook_button)
        self.disclaimer_button.controlDown(self.facebook_button)

        self.setFocus(self.close_button)


class Prompt(pyxbmct.AddonDialogWindow):

    pyxbmct.skin.estuary = False if 'onfluence' in skin_name().lower() or 'aeon' in skin_name().lower() else True

    def __init__(self):

        # noinspection PyArgumentList
        super(Prompt, self).__init__(control.lang(30267).format(control.version()))

        self.yes_button = None
        self.no_button = None
        self.close_button = None
        self.do_not_ask_again_button = None
        self.description = None
        self.setGeometry(854, 480, 8, 3)
        self.set_controls()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.connect(pyxbmct.ACTION_MOUSE_LEFT_CLICK, self.close)
        self.set_navigation()

    def set_controls(self):

        image = pyxbmct.Image(control.fanart(), aspectRatio=2)
        self.placeControl(image, 0, 0, 5, 3)
        # Note
        self.description = pyxbmct.Label(control.lang(30356).format(remote_version()), alignment=2)
        self.placeControl(self.description, 5, 0, 2, 3)
        # Yes button
        self.yes_button = pyxbmct.Button(control.lang(30357))
        self.placeControl(self.yes_button, 6, 0)
        self.connect(self.yes_button, lambda: force())
        # No button
        self.no_button = pyxbmct.Button(control.lang(30358))
        self.placeControl(self.no_button, 6, 1)
        self.connect(self.no_button, self.close)
        # Do not ask again button
        self.do_not_ask_again_button = pyxbmct.Button(control.lang(30359))
        self.placeControl(self.do_not_ask_again_button, 6, 2)
        self.connect(self.do_not_ask_again_button, lambda: do_not_ask_again())
        # Close button
        self.close_button = pyxbmct.Button(control.lang(30329))
        self.placeControl(self.close_button, 7, 0, 1, 3)
        self.connect(self.close_button, self.close)

    def set_navigation(self):

        self.yes_button.controlRight(self.no_button)
        self.yes_button.controlLeft(self.do_not_ask_again_button)
        self.yes_button.controlDown(self.close_button)
        self.yes_button.controlUp(self.close_button)

        self.no_button.controlLeft(self.yes_button)
        self.no_button.controlRight(self.do_not_ask_again_button)
        self.no_button.controlDown(self.close_button)
        self.no_button.controlUp(self.close_button)

        self.do_not_ask_again_button.controlRight(self.yes_button)
        self.do_not_ask_again_button.controlLeft(self.no_button)
        self.do_not_ask_again_button.controlDown(self.close_button)
        self.do_not_ask_again_button.controlUp(self.close_button)

        self.close_button.controlUp(choice([self.yes_button, self.no_button, self.do_not_ask_again_button]))
        self.close_button.controlDown(choice([self.yes_button, self.no_button, self.do_not_ask_again_button]))
        self.close_button.controlLeft(self.do_not_ask_again_button)
        self.close_button.controlRight(self.yes_button)

        self.setFocus(self.close_button)


def new_version(new=False):

    version_file = control.join(control.dataPath, 'version.txt')

    if not path.exists(version_file) or new:

        if not path.exists(control.dataPath):

            control.makeFile(control.dataPath)

        try:
            with open(version_file, mode='w', encoding='utf-8') as f:
                f.write(control.version())
        except Exception:
            with open(version_file, 'w') as f:
                f.write(control.version())

        return True

    else:

        try:
            with open(version_file, encoding='utf-8') as f:
                version = f.read()
        except Exception:
            with open(version_file) as f:
                version = f.read()

        if version != control.version():
            return new_version(new=True)
        else:
            return False


def remote_version():

    xml = client.request('https://bitbucket.org/thgiliwt/repo.thgiliwt/raw/HEAD/_thgiliwt/addons.xml')

    version = client.parseDOM(xml, 'addon', attrs={'id': 'plugin.video.AliveGR'}, ret='version')[0]

    return version


def welcome():

    window = Card()
    window.doModal()

    del window


def prompt():

    window = Prompt()
    window.doModal()

    del window


def checkpoint():

    check = time() + 22000

    if new_version():

        # if control.yesnoDialog(control.lang(30267)):
        #     changelog()
        welcome()

        cache_clear()
        reset_idx(notify=False)

        if control.setting('debug') == 'true' or control.setting('toggler') == 'true':

            from tulip.log import log_notice

            log_notice('Debug settings have been reset, please do not touch these settings manually,'
                       ' they are *only* meant to help developer test various aspects.')

            control.setSetting('debug', 'false')
            control.setSetting('toggler', 'false')

        control.setSetting('last_check', str(check))

    elif control.setting('new_version_prompt') == 'true' and time() > float(control.setting('last_check')) and remote_version() != control.version():

        prompt()
        control.setSetting('last_check', str(check))


def dev():

    if control.setting('toggler') == 'false':

        dwp = control.dialog.input(
            'I hope you know what you\'re doing!', type=control.password_input, option=control.verify
        )
        text = client.request(thgiliwt('=' + leved))

        if text == dwp:

            control.setSetting('toggler', 'true')

            cache.clear(withyes=False)

        else:

            import sys
            control.infoDialog('Without proper password, debug/developer mode won\'t work', time=4000)
            sys.exit()

    elif control.setting('toggler') == 'true':

        control.setSetting('toggler', 'false')
