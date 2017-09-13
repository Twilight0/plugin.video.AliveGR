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


from tulip import control, client
from helpers import thgiliwt

########################################################################################################################
############### Please do not copy these keys, instead create your own with this tutorial: #############################
############### http://forum.kodi.tv/showthread.php?tid=267160&pid=2299960#pid2299960      #############################
########################################################################################################################

api_keys = {
            'enablement': 'true',
            'id': '498788153161-pe356urhr0uu2m98od6f72k0vvcdsij0.apps.googleusercontent.com',
            'api_key': '0I1Ry82VGNWOypWMxUDR5JGMs5kQINDMmdET59UMrhTQ5NVY6lUQ',
            'secret': 'e6RBIFCVh1Fm-IX87PVJjgUu'
           }

iptv_folder = control.transPath('special://profile/addon_data/pvr.iptvsimple')


def setup_iptv():

    if control.exists(control.join(iptv_folder, 'settings.xml')):
        if control.yesnoDialog(line1=control.lang(30021), line2='', line3=control.lang(30022)):
            client.retriever('http://alivegr.net/raw/iptv_settings.xml', control.join(iptv_folder, "settings.xml"))
            control.infoDialog(message=control.lang(30024), time=2000)
            enable_iptv()
            enable_proxy_module()
        else:
            control.infoDialog(message=control.lang(30029), time=2000)

    elif not control.exists(control.join(iptv_folder, 'settings.xml')):
        if control.yesnoDialog(line1=control.lang(30023), line2='', line3=control.lang(30022)):
            if not control.exists(iptv_folder):
                control.makeFile(iptv_folder)
            client.retriever('http://alivegr.net/raw/iptv_settings.xml', control.join(iptv_folder, 'settings.xml'))
            control.infoDialog(message=control.lang(30024), time=2000)
            enable_iptv()
            enable_proxy_module()
        else:
            control.infoDialog(message=control.lang(30029), time=2000)


def enable_iptv():

    if control.condVisibility('Pvr.HasTVChannels'):
        control.infoDialog(message=control.lang(30407), time=4000)

    elif not control.exists(control.join(iptv_folder, 'settings.xml')):
        control.infoDialog(message=control.lang(30409), time=4000)

    else:

        if control.yesnoDialog(line1=control.lang(30406), line2='', line3=''):
            iscon = '{"jsonrpc":"2.0", "method": "Addons.SetAddonEnabled", "params": {"addonid": "pvr.iptvsimple", "enabled": true}, "id": 1}'
            control.jsonrpc(iscon)
            if control.infoLabel('System.AddonVersion(xbmc.python)') == '2.24.0':
                liveon = '{"jsonrpc":"2.0", "method": "Settings.SetSettingValue", "params": {"setting": "pvrmanager.enabled", "value": true}, "id": 1}'
                control.jsonrpc(liveon)
        else:
            pass


def enable_proxy_module():

    if not control.condVisibility('System.HasAddon(service.streamlink.proxy)'):
        if control.yesnoDialog(line1=control.lang(30141), line2='', line3=''):
            if control.infoLabel('System.AddonVersion(xbmc.python)') == '2.24.0':
                control.execute('RunPlugin(plugin://service.streamlink.proxy/)')
            else:
                control.execute('InstallAddon(service.streamlink.proxy)')
        else:
            control.infoDialog(control.lang(30142))
    else:
        control.infoDialog(control.lang(30143))
    control.addon('service.streamlink.proxy').setSetting('listen_port', '50165')


def setup_previous_menu_key():

    keymap_settings_folder = control.transPath('special://profile/keymaps')

    if control.yesnoDialog(line1=control.lang(30025) + ' ' + control.lang(30026), line2=control.lang(30022), line3= ''):
        if not control.exists(keymap_settings_folder):
            control.makeFile(keymap_settings_folder)
        client.retriever('http://alivegr.net/raw//tvguide.xml', control.join(keymap_settings_folder, 'tvguide.xml'))
        control.execute('Action(reloadkeymaps)')
        control.infoDialog(message=control.lang(30024), time=2000)
        control.okDialog(control.addonInfo('name'), control.lang(30027) + ', ' + control.lang(30028))
    else:
        control.infoDialog(message=control.lang(30029), time=2000)


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
        control.addon('plugin.video.youtube').setSetting('youtube.language', 'GR')
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

    else:

        pass

########################################################################################################################


def changelog():

    ch_txt = control.join(control.addonPath, 'changelog.txt')
    with open(ch_txt) as text:
        result = text.read()

    control.dialog.textviewer(control.addonInfo('name') + ', ' + control.lang(30110), result)

    text.close()


def checkpoint():

    disclaimer = control.addonInfo('disclaimer')

    if control.setting('first_time') == 'true':

        control.dialog.textviewer(
            control.addonInfo(
                'name'
            ) + ', ' + control.lang(30129),  ' ' * 3 + disclaimer.decode('utf-8') + '\n' * 2 + control.lang(30131)
        )

        control.setSetting('first_time', 'false')

    else:

        pass

    if not control.condVisibility('System.HasAddon(repository.thgiliwt)'):

        control.okDialog(heading=control.addonInfo('name'), line1=control.lang(30130))
        import sys
        sys.exit(1)

    else:

        pass

    if control.exists(control.join(control.addonPath, 'DELETE_ME')):

        from helpers import cache_clear, reset_idx
        cache_clear(); reset_idx()

    else:

        pass



def dev():

    from helpers import leved
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
