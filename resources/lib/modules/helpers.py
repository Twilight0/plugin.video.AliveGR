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

from zlib import decompress, compress
from base64 import b64decode
from tulip import control, cache, client
from tulip.log import *

leved = 'Q2dw5CchN3c39mck9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'


def pvr_client(query='false'):

    if control.condVisibility('Pvr.HasTVChannels'):

        if query is None or query == 'false':

            selection = control.selectDialog([control.lang(30001), control.lang(30014)])

            if selection == 0:
                control.execute('ActivateWindow(TVChannels)')
            elif selection == 1:
                control.execute('ActivateWindow(TVGuide)')
            else:
                control.execute('Dialog.Close(all)')

        elif query == 'true':

            control.execute('ActivateWindow(TVGuide)')

    else:

        control.infoDialog(message=control.lang(30065))


def papers():

    control.execute('ActivateWindow(10002,"plugin://plugin.video.AliveGR/?content_type=image",return)')


def stream_picker(qualities, urls):

    choice = control.selectDialog(heading=control.lang(30167).partition(' (')[0], list=qualities)

    if choice <= len(qualities) and not choice == -1:
        popped = urls[choice]
        return popped
    else:
        return 30403


def set_a_setting(setting, value):

    json_cmd = {
        "jsonrpc": "2.0", "method": "Settings.SetSettingValue", "params": {"setting": setting, "value": value}, "id": 1
    }

    control.json_rpc(json_cmd)


def get_a_setting(setting):

    json_cmd = {
        "jsonrpc": "2.0", "method": "Settings.GetSettingValue", "params": {"setting": setting}, "id": 1
    }

    return control.json_rpc(json_cmd)


def lang_choice():

    def set_other_options():

        set_a_setting('locale.longdateformat', 'regional')
        set_a_setting('locale.shortdateformat', 'regional')
        set_a_setting('locale.speedunit', 'regional')
        set_a_setting('locale.temperatureunit', 'regional')
        set_a_setting('locale.timeformat', 'regional')
        set_a_setting('locale.use24hourclock', 'regional')

    selections = [control.lang(30217), control.lang(30218)]

    dialog = control.selectDialog(selections)

    if dialog == 0:
        set_a_setting('locale.language', 'resource.language.en_gb')
        set_a_setting('locale.country', 'Central Europe')
        set_other_options()
    elif dialog == 1:
        set_a_setting('locale.language', 'resource.language.el_gr')
        set_a_setting('locale.country', 'Ελλάδα')
        set_other_options()
    else:
        control.execute('Dialog.Close(all)')

    layouts = get_a_setting('locale.keyboardlayouts').get('result').get('value')

    if 'English QWERTY' and 'Greek QWERTY' not in layouts:
        if control.yesnoDialog(control.lang(30286)):
            set_a_setting('locale.keyboardlayouts', ['English QWERTY', 'Greek QWERTY'])
        else: pass
    else: pass

    control.sleep(100)
    refresh()


def addon_version(addon_id):

    version = int(control.infoLabel('System.AddonVersion({0})'.format(addon_id)).replace('.', ''))

    return version


def other_addon_settings(query):

    try:
        control.openSettings(id='{0}'.format(query))
    except:
        pass


def reset_idx(notify=True):

    control.setSetting('live_group', 'ALL')
    control.setSetting('vod_group', '30213')
    control.setSetting('papers_group', '0')
    if notify:
        control.infoDialog(message=control.lang(30402), time=3000)
    log_debug('Indexers have been reset')


def add_to_playlist():

    control.execute('Action(Queue)')


def clear_playlist():

    control.execute('Playlist.Clear')


def toggle_watched():

    control.execute('Action(ToggleWatched)')


def toggle_debug():

    control.execute('ToggleDebug')


def cache_clear():

    log_debug('Cache has been cleared')
    cache.clear(withyes=False)


def cache_delete():

    cache.delete(withyes=False)


def purge_bookmarks():

    if control.exists(control.bookmarksFile):
        if control.yesnoDialog(line1=control.lang(30214)):
            control.deleteFile(control.bookmarksFile)
            control.infoDialog(control.lang(30402))
        else:
            control.infoDialog(control.lang(30403))
    else:
        control.infoDialog(control.lang(30139))


def tools_menu():

    control.execute('ActivateWindow(programs,"plugin://plugin.video.AliveGR/?content_type=executable",return)')


def greeting():

    control.infoDialog(control.lang(30263))


def delete_settings():

    if control.exists(control.dataPath):
        from shutil import rmtree
        rmtree(control.dataPath, ignore_errors=True)
        control.infoDialog(control.lang(30402).encode('utf-8'))
    else:
        control.infoDialog(control.lang(30140))


def refresh():

    control.refresh()


def refresh_and_clear():

    cache_clear()
    control.sleep(50)
    refresh()


def force():

    control.execute('UpdateAddonRepos')
    control.infoDialog(control.lang(30261))


def system_info():
    control.execute('ActivateWindow(systeminfo,return)')


def thgiliwt(s):

    string = s[::-1]

    return b64decode(string)


def pawsesac(s, ison=''):

    string = s.swapcase()

    string = string + ison
    return string


def dexteni(s):

    return decompress(s)


def xteni(s):

    return compress(s)


def loader(mod, folder):

    target = control.join(control.transPath(control.addonInfo('path')), 'resources', 'lib', folder, '{0}'.format(mod))

    # client.retriever('http://alivegr.net/raw/{0}'.format(mod), control.join(target))

    black_list_mod = client.request('https://pastebin.com/raw/DrddTrwg')

    with open(target, 'w') as f:
        f.write(black_list_mod)


def geo_loc():

    json_obj = client.request('http://freegeoip.net/json/')

    return json_obj


def dmca():

    i18n = 'el' if control.infoLabel('System.Language') == 'Greek' else 'en'

    location = control.join(
        control.transPath(control.addonInfo('path')), 'resources', 'texts', 'dmca_{0}.txt'.format(i18n)
    )

    with open(location) as f:
        text = f.read()

    control.dialog.textviewer(control.addonInfo('name'), text)
