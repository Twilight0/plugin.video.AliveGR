# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from __future__ import absolute_import, unicode_literals

import re
import codecs
from tulip import control, client, cache, m3u8, directory
from tulip.compat import parse_qsl, is_py3, urlparse, py2_uni
from tulip.log import log_debug
from resources.lib.modules.themes import iconname
from resources.lib.modules.constants import WEBSITE, PINNED, HISTORY, cache_duration
from resources.lib.modules.kodi import force
from os import path
from time import time
from base64 import b64decode
from zlib import decompress, compress
from scrapetube.list_formation import list_playlist_videos, list_playlists


########################################################################################################################

iptv_folder = control.transPath('special://profile/addon_data/pvr.iptvsimple')
vtpi = 'wWb45ycn5Wa0RXZz9ld0BXavcXYy9Cdl5mLydWZ2lGbh9yL6MHc0RHa'
leved = 'Q2dw5CchN3c39mck9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'
reset_cache = cache.FunctionCache().reset_cache
cache_function = cache.FunctionCache().cache_function


def papers():

    control.execute('Dialog.Close(all)')

    control.execute('ActivateWindow(10002,"plugin://plugin.video.AliveGR/?content_type=image",return)')


def stream_picker(links):

    _choice = control.selectDialog(heading=control.lang(30006), list=[link[0] for link in links])

    if _choice <= len(links) and not _choice == -1:
        popped = [link[1] for link in links][_choice]
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

    links = list(zip(qualities, urls))

    return stream_picker(links)


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


def delete_history():

    if path.exists(HISTORY):
        if control.yesnoDialog(line1=control.lang(30484)):
            control.deleteFile(HISTORY)
            control.infoDialog(control.lang(30402))
        else:
            control.infoDialog(control.lang(30403))
    else:
        control.infoDialog(control.lang(30347))


def delete_settings_xml():

    if path.exists(control.dataPath):
        if control.yesnoDialog(line1=control.lang(30348)):
            control.deleteFile(control.join(control.dataPath, 'settings.xml'))
            control.infoDialog(control.lang(30402))
        else:
            control.infoDialog(control.lang(30403))
    else:
        control.infoDialog(control.lang(30487))


def tools_menu():

    control.execute('Dialog.Close(all)')

    control.execute('ActivateWindow(programs,"plugin://plugin.video.AliveGR/?content_type=executable",return)')


def call_info():

    control.close_all()

    control.execute('ActivateWindow(programs,"plugin://plugin.video.AliveGR/?content_type=executable&action=info",return)')


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


def pin_to_file(file_, txt):

    if not control.exists(file_):
        control.makeFiles(control.dataPath)

    if not txt:
        return

    if txt not in pinned_from_file(file_):

        with open(file_, 'a') as f:
            f.writelines(txt + '\n')


def pinned_from_file(file_):

    if control.exists(file_):

        with open(file_, 'r') as f:
            text = [i.rstrip('\n') for i in f.readlines()][::-1]

        return text

    else:

        return ['']


def unpin_from_file(file_, txt):

    with open(file_, 'r') as f:
        text = [i.rstrip('\n') for i in f.readlines()]

    text.remove(txt)

    with open(file_, 'w') as f:
        if not text:
            text = ''
        else:
            text = '\n'.join(text) + '\n'
        f.write(text)


def pin():

    control.busy()

    title = control.infoLabel('ListItem.Title')

    pin_to_file(PINNED, title)

    control.infoDialog(control.lang(30338), time=750)

    control.idle()


def unpin():

    control.busy()

    title = control.infoLabel('ListItem.Title')

    unpin_from_file(PINNED, title)

    control.sleep(100)
    control.refresh()

    control.infoDialog(control.lang(30338), time=750)

    control.idle()


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
    <visualisation>
        <keyboard>
            <key id="61670">osd</key>
        </keyboard>
    </visualisation>
</keymap>'''

        location = control.join(keymap_settings_folder, 'samsung.xml')

        lang_int = 30022

        def seq():

            with open(location, 'w') as f:
                f.write(string)

    elif keymap == 'stop_playback':

        string = '''<keymap>
    <fullscreenvideo>
        <keyboard>
            <key id="61448">stop</key>
        </keyboard>
        <keyboard>
            <key id="61448" mod="longpress">back</key>
        </keyboard>
    </fullscreenvideo>
    <visualisation>
        <keyboard>
            <key id="61448">stop</key>
        </keyboard>
        <keyboard>
            <key id="61448" mod="longpress">back</key>
        </keyboard>
    </visualisation>
</keymap>'''

        location = control.join(keymap_settings_folder, 'stop_playback.xml')

        lang_int = 30022

        def seq():

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


def isa_setup():

    settings_file = '''<settings version="2">
    <setting id="MINBANDWIDTH" default="true">0</setting>
    <setting id="MAXBANDWIDTH" default="true">0</setting>
    <setting id="MAXRESOLUTION" default="true">0</setting>
    <setting id="MAXRESOLUTIONSECURE" default="true">0</setting>
    <setting id="STREAMSELECTION">2</setting>
    <setting id="MEDIATYPE" default="true">0</setting>
    <setting id="HDCPOVERRIDE" default="true">false</setting>
    <setting id="IGNOREDISPLAY" default="true">false</setting>
    <setting id="DECRYPTERPATH" default="true">special://xbmcbinaddons</setting>
    <setting id="WIDEVINE_API" default="true">10</setting>
    <setting id="PRERELEASEFEATURES" default="true">false</setting>
</settings>
'''

    def wizard():

        lines = settings_file.splitlines()[1:-1]

        for line in lines:

            control.addon('inputstream.adaptive').setSetting(
                re.search(r'id="(\w+)"', line).group(1), re.search(r'>([\w/:]+)<', line).group(1)
            )

    if control.yesnoDialog(line1=control.lang(30022)):

        wizard()
        control.infoDialog(message=control.lang(30402), time=3000)


def yt_setup():

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


def trim_history():

    """
    Trims history to what is set in settings
    :return:
    """

    history_size = int(control.setting('history_size'))

    if is_py3:
        f = open(HISTORY, 'r', encoding='utf-8')
    else:
        f = codecs.open(HISTORY, 'r', encoding='utf-8')

    text = [i.rstrip('\n') for i in f.readlines()][::-1]

    f.close()

    if len(text) > history_size:

        if is_py3:
            f = open(HISTORY, 'w', encoding='utf-8')
        else:
            f = codecs.open(HISTORY, 'w', encoding='utf-8')

        dif = history_size - len(text)
        result = text[:dif][::-1]
        f.write('\n'.join(result) + '\n')
        f.close()


def add_to_history(txt):

    if not txt:
        return

    try:

        if is_py3:
            f = open(HISTORY, 'r', encoding='utf-8')
            if txt + '\n' in f.readlines():
                return
            else:
                pass
        else:
            f = codecs.open(HISTORY, 'r', encoding='utf-8')
            if py2_uni(txt) + '\n' in f.readlines():
                return
            else:
                pass
        f.close()

    except IOError:
        pass

    if is_py3:
        f = open(HISTORY, 'a', encoding='utf-8')
    else:
        f = codecs.open(HISTORY, 'a', encoding='utf-8')

    f.writelines(txt + '\n')
    f.close()
    trim_history()


def delete_from_history(txt):

    if is_py3:
        f = open(HISTORY, 'r', encoding='utf-8')
    else:
        f = codecs.open(HISTORY, 'r', encoding='utf-8')

    lines = f.readlines()
    f.close()

    if py2_uni(txt) + '\n' in lines:
        lines.remove(py2_uni(txt) + '\n')
    else:
        return

    if is_py3:
        f = open(HISTORY, 'w', encoding='utf-8')
    else:
        f = codecs.open(HISTORY, 'w', encoding='utf-8')

    f.write(''.join(lines))
    f.close()

    control.refresh()


def read_from_history():

    """
    Reads from history file which is stored in plain text, line by line
    :return: List
    """

    if control.exists(HISTORY):

        if is_py3:
            f = open(HISTORY, 'r', encoding='utf-8')
        else:
            f = codecs.open(HISTORY, 'r', encoding='utf-8')
        text = [i.rstrip('\n') for i in f.readlines()][::-1]

        f.close()

        return text

    else:

        return


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


def prompt():

    control.okDialog('AliveGR', control.lang(30356).format(remote_version()))

    choices = [control.lang(30357), control.lang(30358), control.lang(30359)]

    _choice = control.selectDialog(choices, heading=control.lang(30482))

    if _choice == 0:
        force()
    elif _choice == 1:
        control.close_all()
    elif _choice == 2:
        do_not_ask_again()


def welcome():

    choices = [control.lang(30329), control.lang(30340), control.lang(30129), control.lang(30333)]

    _choice = control.selectDialog(choices, heading=control.lang(30267).format(control.version()))

    if _choice in [0, -1]:
        control.close_all()
    elif _choice == 1:
        changelog()
    elif _choice == 2:
        disclaimer()
    elif _choice == 3:
        control.open_web_browser(WEBSITE)


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


@cache_function(cache_duration(60))
def yt_playlist(url):

    return list_playlist_videos(url)


@cache_function(cache_duration(480))
def yt_playlists(url):

    return list_playlists(url)
