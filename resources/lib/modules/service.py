# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import sys, os
from xbmcvfs import mkdir
from xbmcaddon import Addon

if sys.version_info[0] == 3:
    from xbmcvfs import translatePath
else:
    from xbmc import translatePath

addon_id = 'plugin.video.AliveGR'
original_settings = 'special://home/addons/{}/resources/settings.xml'.format(addon_id)
new_settings = 'special://home/addons/{}/resources/texts/matrix_settings.xml'.format(addon_id)
datapath = 'special://profile/addon/plugin.video.AliveGR/'
__addon__ = Addon(addon_id)


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
