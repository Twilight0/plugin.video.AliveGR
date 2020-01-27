# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

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

from tulip.compat import OrderedDict
from tulip.control import dataPath, join

########################################################################################################################
############### Please do not copy these keys, instead create your own with this tutorial: #############################
###############   http://forum.kodi.tv/showthread.php?tid=267160&pid=2299960#pid2299960    #############################
########################################################################################################################

API_KEYS = {
    'enablement': 'true',
    'id': '498788153161-pe356urhr0uu2m98od6f72k0vvcdsij0.apps.googleusercontent.com',
    'api_key': '0I1Ry82VGNWOypWMxUDR5JGMs5kQINDMmdET59UMrhTQ5NVY6lUQ',
    'secret': 'e6RBIFCVh1Fm-IX87PVJjgUu'
}

########################################################################################################################

ART_ID = 'resource.images.alivegr.artwork'
LOGOS_ID = 'resource.images.alivegr.logos'
YT_ADDON = 'plugin://plugin.video.youtube'
YT_URL = 'https://www.youtube.com/watch?v='
YT_PREFIX = YT_ADDON + '/play/?video_id='
PLAY_ACTION = '?action=play&url='

########################################################################################################################

WEBSITE = 'https://www.alivegr.net'
FACEBOOK = 'https://www.facebook.com/alivegr/'
TWITTER = 'https://twitter.com/TwilightZer0'

########################################################################################################################

LIVE_GROUPS = OrderedDict(
    [
        ('Panhellenic', 30201), ('Pancypriot', 30202), ('International', 30203), ('Cinema', 30205),
        ('AliveGR Cinema', 30342), ('Misc', 30206), ('Regional', 30207), ('Thematic', 30208),
        ('Toronto Channels', 30209), ('Web TV', 30210), ('Kids', 30032), ('Music', 30125), ('Sports', 30094)
    ]
)

########################################################################################################################

PINNED = join(dataPath, 'pinned.txt')

########################################################################################################################
