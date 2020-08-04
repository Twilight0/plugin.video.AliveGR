# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''
from __future__ import absolute_import, unicode_literals

import json
from zlib import decompress, compress
from .constants import PINNED, SCRAMBLE
from .kodi import rurl_enable
from os import path
from base64 import b64decode
from tulip import control, cache, client, m3u8
from tulip.compat import parse_qsl, urljoin
from tulip.log import log_debug
from youtube_registration import register_api_keys

leved = 'Q2dw5CchN3c39mck9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'


def papers():

    control.execute('Dialog.Close(all)')

    control.execute('ActivateWindow(10002,"plugin://plugin.video.AliveGR/?content_type=image",return)')


def stream_picker(qualities, urls):

    choice = control.selectDialog(heading=control.lang(30006), list=qualities)

    if choice <= len(qualities) and not choice == -1:
        popped = urls[choice]
        return popped


def m3u8_picker(url):

    try:

        if '|' not in url:
            raise TypeError

        link, sep, head = url.rpartition('|')

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

        uri = stream.uri

        if not uri.startswith('http'):
            uri = urljoin(stream.base_uri, uri)

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

    live_enability = control.lang(30330) if control.setting('show_alt_live') == 'true' else control.lang(30335)
    vod_enability = control.lang(30330) if control.setting('show_alt_vod') == 'true' else control.lang(30335)

    option = control.selectDialog(
        [control.lang(30317).format(live_enability), control.lang(30405).format(vod_enability)],
        heading=': '.join([control.addonInfo('name'), control.lang(30350)])
        )

    if option == 0:

        if control.setting('show_alt_live') == 'false':

            yes = control.yesnoDialog(control.lang(30114))

            if yes:

                control.setSetting('show_alt_live', 'true')
        else:

            yes = control.yesnoDialog(control.lang(30404))

            if yes:

                control.setSetting('show_alt_live', 'false')

    elif option == 1:

        if control.setting('show_alt_vod') == 'false':

            yes = control.yesnoDialog(control.lang(30114))

            if yes:

                control.setSetting('show_alt_vod', 'true')
                rurl_enable()

        else:

            yes = control.yesnoDialog(control.lang(30404))

            if yes:

                control.setSetting('show_alt_vod', 'false')


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


def activate_audio_addon(url, query=None):

    from tulip import directory

    directory.run_builtin(addon_id=url, action=query if query is not None else None, content_type='audio')


def cache_clear():

    log_debug('Cache has been cleared')
    cache.clear(withyes=False)


def cache_delete():

    cache.delete(withyes=False)


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

            keys = json.loads(decompress(b64decode(SCRAMBLE)))

            register_api_keys(control.addonInfo('id'), keys['api_key'], keys['id'], keys['secret'])

        f.close()
