# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from tulip import control, client
from tulip.compat import range
from os import path


def pvr_client(query='false'):

    control.execute('Dialog.Close(all)')

    if control.condVisibility('Pvr.HasTVChannels'):

        if query is None or query == 'false':

            selection = control.selectDialog([control.lang(30001), control.lang(30014)])

            if selection == 0:
                control.execute('ActivateWindow(TVChannels)')
            elif selection == 1:
                control.execute('ActivateWindow(TVGuide)')

        elif query == 'true':

            control.execute('ActivateWindow(TVGuide)')

    else:

        control.infoDialog(message=control.lang(30065))


def skin_name():

    addon_xml = control.join(control.transPath('special://skin/'), 'addon.xml')

    try:

        with open(addon_xml, encoding='utf-8') as f:

            xml = f.read()

    except Exception:

        with open(addon_xml) as f:

            xml = f.read()

    try:
        name = client.parseDOM(xml, u'addon', ret='name')[0]
    except IndexError:
        name = 'not found'

    return name


def lang_choice():

    selections = [control.lang(30217), control.lang(30218), control.lang(30312), control.lang(30327)]

    dialog = control.selectDialog(selections)

    if dialog == 0:
        control.execute('Addon.Default.Set(kodi.resource.language)')
    elif dialog == 1:
        languages = [control.lang(30286), control.lang(30299)]
        layouts = ['English QWERTY', 'Greek QWERTY']
        indices = control.dialog.multiselect(control.name(), languages)
        control.set_gui_setting('locale.keyboardlayouts', [layouts[i] for i in indices])
    elif dialog == 2:
        control.set_gui_setting('locale.charset', 'CP1253')
        control.set_gui_setting('subtitles.charset', 'CP1253')
    elif dialog == 3:
        control.execute('Dialog.Close(all)')
        control.execute('ActivateWindow(interfacesettings)')
    else:
        control.execute('Dialog.Close(all)')


def add_to_playlist():

    control.execute('Action(Queue)')


def clear_playlist():

    control.execute('Playlist.Clear')


def toggle_watched():

    control.execute('Action(ToggleWatched)')


def toggle_debug():

    control.execute('ToggleDebug')


def skin_debug():

    control.execute('Skin.ToggleDebug')


def skin_choice():

    control.execute('Addon.Default.Set(xbmc.gui.skin)')


def global_settings():

    control.execute('Dialog.Close(all)')

    control.execute('ActivateWindow(settings,return)')


def pvrsettings():

    control.execute('Dialog.Close(all)')

    control.execute('ActivateWindow(pvrsettings)')


def reload_skin():

    control.execute('ReloadSkin()')


def system_info():

    control.execute('Dialog.Close(all)')

    control.execute('ActivateWindow(systeminfo,return)')


def isa_enable():

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


def log_upload():

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


def rtmp_enable():

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


def force():

    control.execute('UpdateAddonRepos')
    control.infoDialog(control.lang(30261))


def prevent_failure():

    for i in range(0, 500):

        if control.condVisibility('Window.IsActive(busydialog)'):
            control.sleep(100)
        else:
            control.execute('Dialog.Close(all,true)')
            break
