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

from random import choice
from tulip.compat import OrderedDict
from tulip.control import dataPath, join, setting

########################################################################################################################
############### Please do not copy these keys, instead create your own with this tutorial: #############################
######################################   https://ytaddon.page.link/keys    #############################################
########################################################################################################################

API_KEYS_1 = {
    'id': '368042868178-4fvokphtids9eh59h4m4j0m8huvj1qb2.apps.googleusercontent.com',
    'api_key': 'v1keo9GeEBXSJBTMYljRp1SVM5GVVJ0Q4J3UjdGRulnQ5NVY6lUQ',
    'secret': '-YtREVjllZtljRWYj_RXVgWP'
}

API_KEYS_2 = {
    'id': '427433549692-u6qr22obbb005l41onggbfeecrp0ssj1.apps.googleusercontent.com',
    'api_key': 'R5Ud3sGMNlDO3pndNRlRsJ2QFFXYxoFeDxmaOdjbC9ER5NVY6lUQ',
    'secret': 'tcLHhf_ptYutl-HzYvSpQ7rJ'
}

API_KEYS_3 = {
    'id': '809692766230-5cb1visviarrsou7rhd4d2s2rh2d68n2.apps.googleusercontent.com',
    'api_key': '0YFeFhzTJFWTrJWZlZkM2MFe1VTM3RUYGFETihEdthWQ5NVY6lUQ',
    'secret': '96w2Pc99Ih1HDuaek5LE8YvG'
}

API_KEYS_4 = {
    'id': '692804738907-sjq35lum9kcovk5o6kk3gkvn19neivu9.apps.googleusercontent.com',
    'api_key': 'JZ1Q4wkTrFWTI1mQvFUTPJXWzZzQzlEdON3atIDcwVXQ5NVY6lUQ',
    'secret': 'xFWM0vkol6TMXaFyAx78MKkX'
}

API_KEYS = choice([API_KEYS_1, API_KEYS_2, API_KEYS_3, API_KEYS_4])

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
PAYPAL = 'https://www.paypal.me/AliveGR'
PATREON = 'https://www.patreon.com/twilight0'

########################################################################################################################

LIVE_GROUPS = OrderedDict(
    [
        ('Panhellenic', 30201), ('Pancypriot', 30202), ('International', 30203), ('Regional', 30207),
        ('Toronto Channels', 30209), ('Music', 30125), ('Thematic', 30208), ('Cinema', 30205), ('AliveGR Cinema', 30342),
        ('Kids', 30032), ('Sports', 30094), ('Web TV', 30210), ('Misc', 30206)
    ]
)

########################################################################################################################

PINNED = join(dataPath, 'pinned.txt')

########################################################################################################################

SCRAMBLE = (
            'eJwVy8EOgiAAANBfcZzTZWBBt5xtpmsecqVdGiqQqUGAbdb69+b9vS8wrNbMgq0DYhQmj/U+jY6V4Jv8hS7S3so4AgsHUNXeOjbNbHf40N'
            'MUElLkkGdhl+gUx++xKGl1dbN92kp5hmg3r7aZA/LhkmA/wBhv3H5AXPUEUzU0DYfWLO8rG3QPoWW1Npp4VCnjCSlFz0bDdC2flj2tV8sB'
            '/P5BuTe0'
        )

CACHE_DEBUG = setting('do_not_use_cache') == 'true' and setting('debug') == 'true'
