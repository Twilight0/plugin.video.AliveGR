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
from helpers import thgiliwt, addon_version, cache_clear
from constants import api_keys


########################################################################################################################

iptv_folder = control.transPath('special://profile/addon_data/pvr.iptvsimple')
iscoff = '{"jsonrpc":"2.0", "method": "Addons.SetAddonEnabled", "params": {"addonid": "pvr.iptvsimple", "enabled": false}, "id": 1}'
iscon = '{"jsonrpc":"2.0", "method": "Addons.SetAddonEnabled", "params": {"addonid": "pvr.iptvsimple", "enabled": true}, "id": 1}'
liveoff = '{"jsonrpc":"2.0", "method": "Settings.SetSettingValue", "params": {"setting": "pvrmanager.enabled", "value": false}, "id": 1}'
liveon = '{"jsonrpc":"2.0", "method": "Settings.SetSettingValue", "params": {"setting": "pvrmanager.enabled", "value": true}, "id": 1}'

########################################################################################################################


def setup_iptv():

    if control.exists(control.join(iptv_folder, 'settings.xml')):
        if control.yesnoDialog(line1=control.lang(30021), line2='', line3=control.lang(30022)):
            control.deleteFile(control.join(iptv_folder, 'settings.xml'))
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
        if control.yesnoDialog(line1=control.lang(30410), line2='', line3=''):
            control.jsonrpc(iscoff)
            try:
                control.deleteFile(control.join(iptv_folder, 'iptv.m3u.cache'))
                control.deleteFile(control.join(iptv_folder, 'xmltv.xml.cache'))
            except:
                pass
            control.jsonrpc(iscon)
            if control.infoLabel('System.AddonVersion(xbmc.python)') == '2.24.0':
                control.jsonrpc(liveoff)
                control.jsonrpc(liveon)
        else: pass

    elif not control.exists(control.join(iptv_folder, 'settings.xml')):
        control.infoDialog(message=control.lang(30409), time=4000)

    else:

        if control.yesnoDialog(line1=control.lang(30406), line2='', line3=''):
            control.jsonrpc(iscon)
            if control.infoLabel('System.AddonVersion(xbmc.python)') == '2.24.0':
                control.jsonrpc(liveon)
        else: pass


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


def setup_mouse_keymap():

    location = control.transPath(control.join('special://profile', 'keymaps', 'newspapers.xml'))

    def seq():

        string_start = '<keymap><slideshow><mouse>'
        string_end = '</mouse></slideshow></keymap>'
        string_for_left = '<leftclick>NextPicture</leftclick>'
        string_for_right = '<rightclick>PreviousPicture</rightclick>'
        string_for_middle = '<middleclick>Rotate</middleclick>'
        string_for_up = '<wheelup>ZoomIn</wheelup>'
        string_for_down = '<wheeldown>ZoomOut</wheeldown>'

        classes = [string_for_left, string_for_right, string_for_middle, string_for_up, string_for_down]

        map_left = control.lang(30241)
        map_right = control.lang(30242)
        map_middle = control.lang(30243)
        map_up = control.lang(30244)
        map_down = control.lang(30245)

        keys = [map_left, map_right, map_middle, map_up, map_down]

        control.okDialog(control.addonInfo('name'), control.lang(30240))

        indices = control.dialog.multiselect(control.addonInfo('name'), keys)

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

            control.infoDialog(control.lang(30402))

    yes = control.yesnoDialog(control.lang(30238))

    if yes:

        if control.exists(location):

            choices = [control.lang(30248), control.lang(30249)]

            choice = control.selectDialog(choices, heading=control.lang(30247))

            if choice == 0:

                seq()

            elif choice == 1:

                control.deleteFile(location)
                control.execute('Action(reloadkeymaps)')

            else:

                control.infoDialog(control.lang(30403))

        else:

            seq()

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

########################################################################################################################


def changelog():

    if control.setting('changelog_lang') == '0' and control.infoLabel('System.Language') == 'Greek':
        change_txt = 'changelog.el.txt'
    elif control.setting('changelog_lang') == '0' and control.infoLabel('System.Language') != 'Greek' or control.setting('changelog_lang') == '1':
        change_txt = 'changelog.txt'
    else:
        change_txt = 'changelog.el.txt'

    ch_txt = control.join(control.addonPath, change_txt)
    with open(ch_txt) as text:
        result = text.read()

    control.dialog.textviewer(control.addonInfo('name') + ', ' + control.lang(30110), result)

    text.close()


def isa_enable():

    try:
        enabled = control.addon_details('inputstream.adaptive').get('enabled')

        if addon_version('xbmc.python') >= 225 and not enabled:
            yes = control.yesnoDialog(control.lang(30252))
            if yes:
                control.enable_addon('inputstream.adaptive')
                control.infoDialog(control.lang(30402))
            else:
                pass
        elif enabled:
            control.infoDialog(control.lang(30254))
    except:
        pass


def rtmp_enable():

    try:
        enabled = control.addon_details('inputstream.rtmp').get('enabled')

        if addon_version('xbmc.python') >= 225 and not enabled:
            yes = control.yesnoDialog(control.lang(30277))
            if yes:
                control.enable_addon('inputstream.adaptive')
                control.infoDialog(control.lang(30402))
            else:
                pass
        elif enabled:
            control.infoDialog(control.lang(30276))
    except:
        pass


def disclaimer():

    text = control.addonInfo('disclaimer')

    if control.setting('first_time') == 'true':

        control.dialog.textviewer(
            control.addonInfo(
                'name'
            ) + ', ' + control.lang(30129), ' ' * 3 + text.decode('utf-8') + '\n' * 2 + control.lang(30131)
        )

        if control.yesnoDialog(control.lang(30266)):

            control.setSetting('first_time', 'false')
            control.aborted()

        else:
            pass

    else:
        pass


def repo_check():

    if not control.condVisibility('System.HasAddon(repository.thgiliwt)'):

        control.okDialog(heading=control.addonInfo('name'), line1=control.lang(30130))
        control.execute('Dialog.Close(all)')
        import sys; sys.exit()

    else: pass


def block_check():

    if control.condVisibility('System.HasAddon(plugin.program.G.K.N.Wizard)'):

        settings_xml = control.join(control.dataPath, 'settings.xml')
        control.deleteFile(settings_xml)
        control.okDialog(control.lang(30270), control.lang(30271))

    else: pass


def checkpoint():

    disclaimer()

    if control.exists(control.join(control.addonPath, 'DELETE_ME')):
        if control.yesnoDialog(control.lang(30267)):
            changelog()
        else:
            pass
        cache_clear()
        block_check()
        control.deleteFile(control.join(control.addonPath, 'DELETE_ME'))

    else: pass


#Reserved might user later, needs refinement:
# def mailer(title):
#
#     import smtplib
#
#     sender = control.dialog.input()
#     text = control.dialog.input()
#     username = control.dialog.input()
#     password = control.dialog.input()
#
#     smtpServer = 'smtp.{0}'.format(fromAddr.partition('@')[2])
#     rcvr = thgiliwt('=' + 'I3ZuwWah1WZlJnZARHanlGbpdHd')
#     text = '''Subject: {0}{1}
#
#     {2}
#     '''.format(subject, title, text)
#
#     server = smtplib.SMTP(smtpServer)
#     server.starttls()
#     server.login(username, password)
#     server.sendmail(sender, rcvr, text)
#     server.quit()


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
