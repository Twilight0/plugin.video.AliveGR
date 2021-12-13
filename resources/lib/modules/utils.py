# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import, unicode_literals

import pyxbmct, re, json
from tulip import control, client, cache, m3u8, directory, youtube
from tulip.compat import parse_qsl, is_py3, urlparse, py2_uni
from tulip.log import log_debug
from .kodi import skin_name, force as force_
from .themes import iconname
from .constants import (
    FACEBOOK, TWITTER, WEBSITE, PINNED, SCRAMBLE_1, SCRAMBLE_2, SCRAMBLE_3, SCRAMBLE_4, SCRAMBLE_5, SCRAMBLE_6,
    cache_duration
)
from os import path
from random import choice
from time import time
from base64 import b64decode
from zlib import decompress, compress
from youtube_registration import register_api_keys


########################################################################################################################

iptv_folder = control.transPath('special://profile/addon_data/pvr.iptvsimple')
vtpi = 'wWb45ycn5Wa0RXZz9ld0BXavcXYy9Cdl5mLydWZ2lGbh9yL6MHc0RHa'
leved = 'Q2dw5CchN3c39mck9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'
reset_cache = cache.FunctionCache().reset_cache
cache_function = cache.FunctionCache().cache_function


def papers():

    control.execute('Dialog.Close(all)')

    control.execute('ActivateWindow(10002,"plugin://plugin.video.AliveGR/?content_type=image",return)')


def stream_picker(qualities, urls):

    _choice = control.selectDialog(heading=control.lang(30006), list=qualities)

    if _choice <= len(qualities) and not _choice == -1:
        popped = urls[_choice]
        return popped


def m3u8_picker(url):

    try:

        if '|' not in url:
            raise TypeError

        link, _, head = url.rpartition('|')

        headers = dict(parse_qsl(head))
        streams = m3u8.load(link, headers=headers).playlists

    except TypeError:

        streams = m3u8.load(url).playlists

    if not streams:
        return url

    qualities = []
    urls = []

    for stream in streams:

        quality = repr(stream.stream_info.resolution).strip('()').replace(', ', 'x')

        if quality == 'None':
            quality = 'Auto'

        uri = stream.absolute_uri

        qualities.append(quality)

        try:

            if '|' not in url:
                raise TypeError

            urls.append(uri + ''.join(url.rpartition('|')[1:]))

        except TypeError:
            urls.append(uri)

    if len(qualities) == 1:

        control.infoDialog(control.lang(30220).format(qualities[0]))

        return url

    return stream_picker(qualities, urls)


def kodi_log_upload():

    exists = control.condVisibility('System.HasAddon(script.kodi.loguploader)')
    addon_path = control.transPath(control.join('special://', 'home', 'addons', 'script.kodi.loguploader'))

    if not exists:

        if path.exists(addon_path):
            control.enable_addon('script.kodi.loguploader')
        else:
            control.execute('InstallAddon(script.kodi.loguploader)')

        while not path.exists(addon_path):
            control.sleep(1000)
        else:
            control.execute('RunScript(script.kodi.loguploader)')

    else:

        control.execute('RunScript(script.kodi.loguploader)')


def toggle_alt():

    if control.setting('show_alt_live') == 'true':
        live_enability = '[COLOR green]' + control.lang(30330) + '[/COLOR]'
    else:
        live_enability = '[COLOR red]' + control.lang(30335) + '[/COLOR]'

    if control.setting('show_alt_vod') == 'true':
        vod_enability = '[COLOR green]' + control.lang(30330) + '[/COLOR]'
    else:
        vod_enability = '[COLOR red]' + control.lang(30335) + '[/COLOR]'

    option = control.selectDialog(
        [
            control.lang(30317).format(live_enability), control.lang(30405).format(vod_enability)
        ],
        heading=': '.join([control.addonInfo('name'), control.lang(30350)])
        )

    if option == 0:

        if control.setting('show_alt_live') == 'false':

            yes = control.yesnoDialog(control.lang(30114))

            if yes:

                control.setSetting('show_alt_live', 'true')
                control.infoDialog(message=control.lang(30402), time=1000)
        else:

            yes = control.yesnoDialog(control.lang(30404))

            if yes:

                control.setSetting('show_alt_live', 'false')
                control.infoDialog(message=control.lang(30402), time=1000)

    elif option == 1:

        if control.setting('show_alt_vod') == 'false':

            yes = control.yesnoDialog(control.lang(30114))

            if yes:

                control.setSetting('show_alt_vod', 'true')
                control.infoDialog(message=control.lang(30402), time=1000)

        else:

            yes = control.yesnoDialog(control.lang(30404))

            if yes:

                control.setSetting('show_alt_vod', 'false')
                control.infoDialog(message=control.lang(30402), time=1000)


def i18n():

    lang = 'el_GR' if 'Greek' in control.infoLabel('System.Language') else 'en_GB'

    return lang


def thumb_maker(video_id, hq=False):

    return 'http://img.youtube.com/vi/{0}/{1}.jpg'.format(video_id, 'mqdefault' if not hq else 'maxresdefault')


def other_addon_settings(query):

    try:

        if query == 'script.module.resolveurl':

            from resolveurl import display_settings
            display_settings()

        else:

            control.openSettings(id='{0}'.format(query))
    except:

        pass


def reset_idx(notify=True, force=False):

    if control.setting('reset_idx') == 'true' or force:

        if control.setting('reset_live') == 'true' or force:

            control.setSetting('live_group', '0')

        control.setSetting('vod_group', '30213')
        control.setSetting('papers_group', '0')

        if notify:
            control.infoDialog(message=control.lang(30402), time=3000)

        log_debug('Indexers have been reset')


def activate_other_addon(url, query=None):

    if not url.startswith('plugin://'):
        url = ''.join(['plugin://', url, '/'])

    parsed = urlparse(url)

    if not control.condVisibility('System.HasAddon({0})'.format(parsed.netloc)):
        control.execute('InstallAddon({0})'.format(parsed.netloc))

    params = dict(parse_qsl(parsed.query))
    action = params.get('action')
    url = params.get('url')

    directory.run_builtin(addon_id=parsed.netloc, action=action, url=url, content_type=query)


def cache_clear(notify=True):

    log_debug('Cache has been cleared')
    reset_cache(notify=notify)


def purge_bookmarks():

    if path.exists(control.bookmarksFile):
        if control.yesnoDialog(line1=control.lang(30214)):
            control.deleteFile(control.bookmarksFile)
            control.infoDialog(control.lang(30402))
        else:
            control.infoDialog(control.lang(30403))
    else:
        control.infoDialog(control.lang(30139))


def delete_settings_xml():

    if path.exists(control.dataPath):
        if control.yesnoDialog(line1=control.lang(30348)):
            control.deleteFile(control.join(control.dataPath, 'settings.xml'))
            control.infoDialog(control.lang(30402))
        else:
            control.infoDialog(control.lang(30403))
    else:
        control.infoDialog(control.lang(30347))


def tools_menu():

    control.execute('Dialog.Close(all)')

    control.execute('ActivateWindow(programs,"plugin://plugin.video.AliveGR/?content_type=executable",return)')


def call_info():

    control.close_all()

    control.execute('ActivateWindow(programs,"plugin://plugin.video.AliveGR/?action=info",return)')


def greeting():

    control.infoDialog(control.lang(30263))


def refresh():

    control.refresh()


def refresh_and_clear():

    cache_clear()
    control.sleep(100)
    refresh()


def thgiliwt(s):

    string = s[::-1]

    return b64decode(string)


def pawsesac(s, ison=''):

    string = s.swapcase()

    string = string + ison
    return string


def bourtsa(s):

    return decompress(s)


def xteni(s):

    return compress(s)


def geo_loc():

    json_obj = client.request('https://extreme-ip-lookup.com/json/', output='json')

    if not json_obj or 'error' in json_obj:
        json_obj = client.request('https://ip-api.com/json/', output='json')

    if not json_obj or 'error' in json_obj:
        json_obj = client.request('https://geoip.siliconweb.com/geo.json', output='json')

    country = json_obj.get('country', 'Worldwide')

    return country


def add_to_file(file_, txt):

    if not control.exists(file_):
        control.makeFiles(control.dataPath)

    if not txt:
        return

    if txt not in read_from_file(file_):

        with open(file_, 'a') as f:
            f.writelines(txt + '\n')


def read_from_file(file_):

    if control.exists(file_):

        with open(file_, 'r') as f:
            text = [i.rstrip('\n') for i in f.readlines()][::-1]

        return text

    else:

        return ['']


def delete_from_file(file_, txt):

    with open(file_, 'r') as f:
        text = [i.rstrip('\n') for i in f.readlines()]

    text.remove(txt)

    with open(file_, 'w') as f:
        if not text:
            text = ''
        else:
            text = '\n'.join(text) + '\n'
        f.write(text)


def api_keys():

    keys_list = [SCRAMBLE_1, SCRAMBLE_2, SCRAMBLE_3, SCRAMBLE_4, SCRAMBLE_5, SCRAMBLE_6]

    if control.setting('keys_are_set') == 'false':

        balancer = choice(keys_list)

        control.setSetting('keys_are_set', 'true')
        control.setSetting('keys_choice', str(keys_list.index(balancer) + 1))

        return json.loads(decompress(b64decode(balancer)))

    else:

        return json.loads(decompress(b64decode(keys_list[int(control.setting('keys_choice')) - 1])))


def pin():

    control.busy()

    title = control.infoLabel('ListItem.Title')

    add_to_file(PINNED, title)

    control.infoDialog(control.lang(30338), time=750)

    control.idle()


def unpin():

    control.busy()

    title = control.infoLabel('ListItem.Title')

    delete_from_file(PINNED, title)

    control.sleep(100)
    control.refresh()

    control.infoDialog(control.lang(30338), time=750)

    control.idle()


def keys_registration():

    filepath = control.transPath(
        control.join(control.addon('plugin.video.youtube').getAddonInfo('profile'), 'api_keys.json')
    )

    setting = control.addon('plugin.video.youtube').getSetting('youtube.allow.dev.keys') == 'true'

    if path.exists(filepath):

        f = open(filepath)

        jsonstore = json.load(f)

        no_keys = control.addonInfo('id') not in jsonstore.get('keys', 'developer').get('developer')

        if setting and no_keys:

            register_api_keys(control.addonInfo('id'), api_keys()['api_key'], api_keys()['id'], api_keys()['secret'])

        f.close()


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

    if control.yesnoDialog(line1=control.lang(integer) + '[CR]' + control.lang(30022)):

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

        if control.yesnoDialog(line1=control.lang(30406)):

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

        lang_int = 30022

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

    elif keymap == 'samsung':

        string = '''<keymap>
    <global>
        <keyboard>
            <key id="61670">contextmenu</key>
        </keyboard>
    </global>
    <fullscreenvideo>
        <keyboard>
            <key id="61670">osd</key>
        </keyboard>
    </fullscreenvideo>
</keymap>'''

        location = control.join(keymap_settings_folder, 'samsung.xml')

        lang_int = 30022

        def seq():

            try:
                with open(location, mode='w', encoding='utf-8') as f:
                    f.write(string)
            except Exception:
                with open(location, 'w') as f:
                    f.write(string)

    yes = control.yesnoDialog(control.lang(lang_int))

    if yes:

        if path.exists(location):

            choices = [control.lang(30248), control.lang(30249)]

            _choice = control.selectDialog(choices, heading=control.lang(30247))

            if _choice == 0:

                seq()
                control.okDialog(control.name(), control.lang(30027) + ', ' + (control.lang(30028)))
                control.infoDialog(control.lang(30402))
                control.execute('Action(reloadkeymaps)')

            elif _choice == 1:

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

        control.addon('plugin.video.youtube').setSetting('youtube.api.id', api_keys()['id'])
        control.addon('plugin.video.youtube').setSetting('youtube.api.key', api_keys()['api_key'])
        control.addon('plugin.video.youtube').setSetting('youtube.api.secret', api_keys()['secret'])

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

            if control.yesnoDialog(line1=control.lang(30069) + '[CR]' + control.lang(30022)):
                seq()
            else:
                control.infoDialog(message=control.lang(30029), time=3000)

        else:

            if control.yesnoDialog(line1=control.lang(30070) + '[CR]' + control.lang(30022)):
                seq()
            else:
                control.infoDialog(message=control.lang(30029), time=3000)

########################################################################################################################

    process()

    if control.yesnoDialog(line1=control.lang(30132)):

        wizard()

    if control.condVisibility('System.HasAddon(inputstream.adaptive)') and control.yesnoDialog(line1=control.lang(30287)):

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


def changelog(get_text=False):

    if control.setting('changelog_lang') == '0' and 'Greek' in control.infoLabel('System.Language'):
        change_txt = 'changelog.el.txt'
    elif (
            control.setting('changelog_lang') == '0' and 'Greek' not in control.infoLabel('System.Language')
    ) or control.setting('changelog_lang') == '1':
        change_txt = 'changelog.en.txt'
    else:
        change_txt = 'changelog.el.txt'

    change_txt = control.join(control.addonPath, 'resources', 'texts', change_txt)

    if get_text:
        return py2_uni(file_to_text(change_txt)).partition(u'\n\n')[0]
    else:
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
        self.connect(self.yes_button, lambda: force_())
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


@cache_function(cache_duration(360))
def remote_version():

    xml = client.request('https://raw.githubusercontent.com/Twilight0/repo.twilight0/master/_zips/addons.xml')

    version = client.parseDOM(xml, 'addon', attrs={'id': control.addonInfo('id')}, ret='version')[0]

    version = int(version.replace('.', ''))

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

    check = time() + 10800
    try:
        new_version_prompt = control.setting('new_version_prompt') == 'true' and remote_version() > int(control.version().replace('.', ''))
    except ValueError:  # will fail if version install is alpha or beta
        new_version_prompt = False

    if new_version():

        # if control.yesnoDialog(control.lang(30267)):
        #     changelog()
        welcome()

        cache_clear(notify=False)
        reset_idx(notify=False)

        if control.setting('debug') == 'true' or control.setting('toggler') == 'true':

            from tulip.log import log_debug

            log_debug('Debug settings have been reset, please do not touch these settings manually,'
                       ' they are *only* meant to help developer test various aspects.')

            control.setSetting('debug', 'false')
            control.setSetting('toggler', 'false')

        control.setSetting('last_check', str(check))

    elif new_version_prompt and time() > float(control.setting('last_check')):

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


def page_selector(query):

    pages = [control.lang(30415).format(i) for i in list(range(1, int(query) + 1))]

    _choice = control.selectDialog(pages, heading=control.lang(30416))

    if _choice != -1:

        control.setSetting('page', str(_choice))
        control.sleep(200)
        control.refresh()

        if control.setting('pagination_reset') == 'true':
            # wait a second in order to ensure container is first loaded then reset the page
            control.sleep(1000)
            control.setSetting('page', '0')


def page_menu(pages, reset=False):

    if not reset:
        index = str(int(control.setting('page')) + 1)
    else:
        index = '1'

    menu = {
        'title': control.lang(30414).format(index),
        'action': 'page_selector',
        'query': str(pages),
        'icon': iconname('switcher'),
        'isFolder': 'False',
        'isPlayable': 'False'
    }

    return menu


def apply_new_settings():

    if is_py3:

        original_settings = 'special://home/addons/{}/resources/settings.xml'.format(control.addonInfo('id'))
        new_settings = 'special://home/addons/{}/resources/texts/matrix_settings.xml'.format(control.addonInfo('id'))

        with open(control.transPath(new_settings)) as new_f:
            new_settings_text = new_f.read()

            with open(control.transPath(original_settings), 'w') as f:
                f.write(new_settings_text)

        control.infoDialog(message=control.lang(30402), time=1000)

    else:

        control.infoDialog(message=control.lang(30300), time=3000)


@cache_function(cache_duration(30))
def yt_videos(url):

    return youtube.youtube(key=api_keys()['api_key'], replace_url=False).videos(url)


@cache_function(cache_duration(60))
def yt_playlist(url):

    return youtube.youtube(key=api_keys()['api_key'], replace_url=False).playlist(url)


@cache_function(cache_duration(480))
def yt_playlists(url):

    return youtube.youtube(key=api_keys()['api_key'], replace_url=False).playlists(url)
