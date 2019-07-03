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

from tulip import control, client
from resources.lib.modules.helpers import thgiliwt, addon_version, cache_clear, i18n, reset_idx, skin_name
from resources.lib.modules.constants import api_keys
from os import path
import pyxbmct, re
from random import choice


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

        elif addon_version('xbmc.python') >= 2260 and not control.condVisibility('System.HasAddon(pvr.iptvsimple)'):

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

                with open(location, 'w') as f:
                    f.write(to_write)

    elif keymap == 'remote_slideshow':

        location = control.transPath(control.join('special://profile', 'keymaps', 'alivegr_remote_slideshow.xml'))

        lang_int = 30238

        def seq():

            string_start = '<keymap><slideshow><keyboard>'
            ok_button = ''
            long_ok_button = ''
            next_pic = ''
            previous_pic = ''
            context = ''
            string_end = '</keyboard></slideshow></keymap>'

            yes_clicked = control.yesnoDialog(control.lang(30026))

            if yes_clicked:

                to_write = string_start + ok_button + long_ok_button + next_pic + previous_pic + context + string_end

            else:

                to_write = string_start + ok_button + long_ok_button + context + string_end

            with open(location, 'w') as f:
                f.write(to_write)

    yes = control.yesnoDialog(control.lang(lang_int))

    if yes:

        if path.exists(location):

            choices = [control.lang(30248), control.lang(30249)]

            choice = control.selectDialog(choices, heading=control.lang(30247))

            if choice == 0:

                seq()
                control.execute('Action(reloadkeymaps)')
                control.okDialog(control.name(), control.lang(30027) + ', ' + (control.lang(30028)))
                control.infoDialog(control.lang(30402))

            elif choice == 1:

                control.deleteFile(location)
                control.execute('Action(reloadkeymaps)')
                control.infoDialog(control.lang(30402))

            else:

                control.infoDialog(control.lang(30403))

        else:

            seq()
            control.okDialog(control.name(), control.lang(30027) + ', ' + (control.lang(30028)))
            control.infoDialog(control.lang(30402))

    else:

        control.infoDialog(control.lang(30403))


def yt_setup():

    def seq():

        control.addon('plugin.video.youtube').setSetting('youtube.api.enable', api_keys['enablement'])
        control.addon('plugin.video.youtube').setSetting('youtube.api.id', api_keys['id'])
        control.addon('plugin.video.youtube').setSetting('youtube.api.key', thgiliwt(api_keys['api_key']))
        control.addon('plugin.video.youtube').setSetting('youtube.api.secret', api_keys['secret'])

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

    else: pass

    if control.condVisibility('System.HasAddon(inputstream.adaptive)') and control.yesnoDialog(line1=control.lang(30287), line2='', line3=''):

        yt_mpd()

    else: pass

########################################################################################################################


def file_to_text(file_):

    with open(file_) as text:
        result = text.read()

    return result


def changelog():

    if control.setting('changelog_lang') == '0' and 'Greek' in control.infoLabel('System.Language'):
        change_txt = 'changelog.el.txt'
    elif (control.setting('changelog_lang') == '0' and  'Greek' not in control.infoLabel('System.Language')) or control.setting('changelog_lang') == '1':
        change_txt = 'changelog.txt'
    else:
        change_txt = 'changelog.el.txt'

    change_txt = control.join(control.addonPath, change_txt)

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


def isa_enable():

    if addon_version('xbmc.python') < 2250:

        control.infoDialog(control.lang(30322))
        return

    try:

        enabled = control.addon_details('inputstream.adaptive').get('enabled')

    except Exception:

        enabled = False

    try:

        if enabled:

            control.infoDialog(control.lang(30254))
            return

        else:

            xbmc_path = control.join('special://xbmc', 'addons', 'inputstream.adaptive')
            home_path = control.join('special://home', 'addons', 'inputstream.adaptive')

            if path.exists(control.transPath(xbmc_path)) or path.exists(control.transPath(home_path)):

                yes = control.yesnoDialog(control.lang(30252))

                if yes:

                    control.enable_addon('inputstream.adaptive')
                    control.infoDialog(control.lang(30402))

            else:

                try:

                    control.execute('InstallAddon(inputstream.adaptive)')

                except Exception:

                    control.okDialog(heading='AliveGR', line1=control.lang(30323))

    except Exception:

        control.infoDialog(control.lang(30278))


def rtmp_enable():

    if addon_version('xbmc.python') < 2250:

        control.infoDialog(control.lang(30322))
        return

    try:

        enabled = control.addon_details('inputstream.rtmp').get('enabled')

    except Exception:

        enabled = False

    try:

        if enabled:

            control.infoDialog(control.lang(30276))
            return

        else:

            xbmc_path = control.join('special://xbmc', 'addons', 'inputstream.rtmp')
            home_path = control.join('special://home', 'addons', 'inputstream.rtmp')

            if path.exists(control.transPath(xbmc_path)) or path.exists(control.transPath(home_path)):

                yes = control.yesnoDialog(control.lang(30277))

                if yes:

                    control.enable_addon('inputstream.rtmp')
                    control.infoDialog(control.lang(30402))

            else:

                try:

                    control.execute('InstallAddon(inputstream.rtmp)')

                except Exception:

                    control.okDialog(heading='AliveGR', line1=control.lang(30323))

    except Exception:

        control.infoDialog(control.lang(30279))


def disclaimer():

    try:
        text = control.addonInfo('disclaimer').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError, AttributeError):
        text = control.addonInfo('disclaimer')

    control.dialog.textviewer(control.addonInfo('name') + ', ' + control.lang(30129), text)


class Prompt(pyxbmct.AddonDialogWindow):

    pyxbmct.skin.estuary = False if 'onfluence' in skin_name().lower() or 'aeon' in skin_name().lower() else True

    def __init__(self):

        # noinspection PyArgumentList
        super(Prompt, self).__init__(control.lang(30267).format(control.version()))

        self.changelog_button = None
        self.disclaimer_button = None
        self.close_button = None
        self.external_label = None
        self.description = None
        self.patreon_button = None
        self.paypal_button = None
        self.facebook_button = None
        self.twitter_button = None
        self.website_button = None
        self.setGeometry(854, 480, 8, 5)
        self.set_controls()
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        self.set_navigation()

    def set_controls(self):

        image = pyxbmct.Image(control.fanart(), aspectRatio=2)
        self.placeControl(image, 0, 0, 5, 5)
        # Note
        self.description = pyxbmct.Label(control.lang(30328), alignment=2)
        self.placeControl(self.description, 5, 0, 2, 5)
        # Click to open label
        # self.external_label = pyxbmct.Label(control.lang(30131), alignment=pyxbmct.ALIGN_CENTER_Y | pyxbmct.ALIGN_CENTER_X)
        # self.placeControl(self.external_label, 6, 0, 1, 1)
        self.website_button = pyxbmct.Button(control.lang(30333))
        self.placeControl(self.website_button, 6, 0, 1, 1)
        self.connect(self.website_button, lambda: control.open_web_browser('https://www.alivegr.net'))
        # Paypal button
        self.paypal_button = pyxbmct.Button(control.lang(30141))
        self.placeControl(self.paypal_button, 6, 2, 1, 1)
        self.connect(self.paypal_button, lambda: control.open_web_browser('https://www.paypal.me/AliveGR'))
        # Patreon button
        self.patreon_button = pyxbmct.Button(control.lang(30142))
        self.placeControl(self.patreon_button, 6, 1, 1, 1)
        self.connect(self.patreon_button, lambda: control.open_web_browser('https://www.patreon.com/twilight0'))
        # Facebook button
        self.facebook_button = pyxbmct.Button('Facebook')
        self.placeControl(self.facebook_button, 6, 3, 1, 1)
        self.connect(self.facebook_button, lambda: control.open_web_browser('https://www.facebook.com/alivegr/'))
        # Twitter button
        self.twitter_button = pyxbmct.Button('Twitter')
        self.placeControl(self.twitter_button, 6, 4, 1, 1)
        self.connect(self.twitter_button, lambda: control.open_web_browser('https://twitter.com/TwilightZer0'))
        # Close button
        self.close_button = pyxbmct.Button(control.lang(30329))
        self.placeControl(self.close_button, 7, 2)
        self.connect(self.close_button, self.close)
        # Changelog button
        self.changelog_button = pyxbmct.Button(control.lang(30110))
        self.placeControl(self.changelog_button, 7, 0, 1, 2)
        self.connect(self.changelog_button, lambda: changelog())
        # Disclaimer button
        self.disclaimer_button = pyxbmct.Button(control.lang(30129))
        self.placeControl(self.disclaimer_button, 7, 3, 1, 2)
        self.connect(self.disclaimer_button, lambda: disclaimer())

    def set_navigation(self):

        self.website_button.controlRight(self.patreon_button)
        self.website_button.controlDown(self.changelog_button)

        self.patreon_button.controlLeft(self.website_button)
        self.patreon_button.controlRight(self.paypal_button)
        self.patreon_button.controlDown(self.changelog_button)

        self.paypal_button.controlRight(self.facebook_button)
        self.paypal_button.controlDown(self.close_button)
        self.paypal_button.controlLeft(self.patreon_button)

        self.facebook_button.controlRight(self.twitter_button)
        self.facebook_button.controlDown(self.disclaimer_button)
        self.facebook_button.controlLeft(self.paypal_button)

        self.twitter_button.controlDown(self.disclaimer_button)
        self.twitter_button.controlLeft(self.facebook_button)

        self.close_button.controlLeft(self.changelog_button)
        self.close_button.controlRight(self.disclaimer_button)
        self.close_button.controlUp(self.paypal_button)

        self.changelog_button.controlRight(self.close_button)
        self.changelog_button.controlUp(self.patreon_button)

        self.disclaimer_button.controlLeft(self.close_button)
        self.disclaimer_button.controlUp(choice([self.facebook_button, self.twitter_button]))

        self.setFocus(self.close_button)


def new_version(new=False):

    version_file = control.join(control.dataPath, 'version.txt')

    if not path.exists(version_file) or new:

        if not path.exists(control.dataPath):

            control.makeFile(control.dataPath)

        with open(version_file, 'w') as f:
            f.write(control.version())

        return True

    else:

        with open(version_file) as f:
            version = f.read()

        if version != control.version():
            return new_version(new=True)
        else:
            return False


def welcome():

    window = Prompt()
    window.doModal()

    del window


def checkpoint():

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


def dev():

    from resources.lib.modules.helpers import leved
    from tulip import cache

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
