# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import os
import sys
import xbmc
from xbmcaddon import Addon

if sys.version_info[0] == 3:
    from xbmcvfs import translatePath
else:
    from xbmc import translatePath

addon_id = 'plugin.video.AliveGR'
new_settings = 'special://home/addons/{}/resources/texts/matrix_settings.xml'.format(addon_id)
old_settings = 'special://home/addons/{}/resources/texts/leia_settings.xml'.format(addon_id)
settings_path = 'special://home/addons/{}/resources/settings.xml'.format(addon_id)
datapath = 'special://profile/addon_data/plugin.video.AliveGR/'
__addon__ = Addon(addon_id)
monitor = xbmc.Monitor()

# Some sellers are exploiting those who do voluntary work and have 3rd party links already enabled, while my intentions
# are that users themselves must enable them; will target only specific builds, lets do something about it:

it_exists = os.path.exists


while not monitor.abortRequested():

    if not it_exists(settings_path):

        if sys.version_info[0] == 3:

            new_f = open(translatePath(new_settings))
            settings_text = new_f.read()

            with open(translatePath(settings_path), 'w') as f:
                f.write(settings_text)

            new_f.close()

        else:

            old_f = open(translatePath(old_settings))
            settings_text = old_f.read()

            with open(translatePath(settings_path), 'w') as f:
                f.write(settings_text)

            old_f.close()

    if monitor.waitForAbort(360):
        break
