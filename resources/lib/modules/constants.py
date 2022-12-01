# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from tulip.compat import OrderedDict
from tulip.control import dataPath, join, setting
from tulip.cache import FunctionCache

cache_function = FunctionCache().cache_function
cache_method = FunctionCache().cache_method

########################################################################################################################

ART_ID = 'resource.images.alivegr.artwork'
LOGOS_ID = 'resource.images.alivegr.logos'
PLUGINS_ID = 'script.module.resolveurl.pluginsgr'
PLUGINS_PATH = 'special://home/addons/{0}/resources/plugins/'.format(PLUGINS_ID)
YT_ADDON_ID = 'plugin.video.youtube'
YT_ADDON = 'plugin://{0}'.format(YT_ADDON_ID)
YT_URL = 'https://www.youtube.com/watch?v='
YT_PREFIX = YT_ADDON + '/play/?video_id='
PLAY_ACTION = '?action=play&url='

########################################################################################################################

WEBSITE = 'https://www.alivegr.net'
FACEBOOK = 'https://www.facebook.com/alivegr/'
TWITTER = 'https://twitter.com/TwilightZer0'
PAYPAL = 'https://www.paypal.me/AliveGR'
PATREON = 'https://www.patreon.com/twilight0'
SUPPORT = 'https://github.com/Twilight0/plugin.video.AliveGR/issues'

########################################################################################################################

LIVE_GROUPS = OrderedDict(
    [
        ('Panhellenic', 30201), ('Pancypriot', 30202), ('International', 30203), ('Regional', 30207),
        ('Toronto Channels', 30209), ('Music', 30125), ('Thematic', 30208), ('Cinema', 30205),
        ('AliveGR Cinema', 30342), ('Kids', 30032), ('Sports', 30094), ('Web TV', 30210), ('Misc', 30206)
    ]
)

QUERY_MAP = OrderedDict(
            [
                ('Live TV Channel', 30113), ('Movie', 30130), ('TV Serie', 30305), ('TV Show', 30133),
                ('Theater', 30068), ('Cartoon', 30097), ('Person', 30101)
            ]
        )

########################################################################################################################

PINNED = join(dataPath, 'pinned.txt')
SEARCH_HISTORY = join(dataPath, 'search_history.csv')
PLAYBACK_HISTORY = join(dataPath, 'playback_history.list')

########################################################################################################################

CACHE_DEBUG = setting('do_not_use_cache') == 'true' and setting('debug') == 'true'
SEPARATOR = ' - ' if setting('wrap_labels') == '1' else '[CR]'


def HOSTS(url):

    _hosts = [
        'dailymotion' in url, 'ant1.com.cy' in url, 'netwix.gr' in url, 'tvopen.gr' in url, 'megatv.com' in url,
        'alphatv.gr' in url, 'alphacyprus.com.cy' in url, 'sigmatv.com' in url,
        'antenna.gr' in url, 'star.gr/tv/' in url, 'cybc.com.cy' in url, 'omegatv.com.cy' in url,
        'skaitv.gr' in url, 'webtv.ert.gr' in url, 'ertflix.gr' in url, 'dai.ly/' in url
    ]

    return any(_hosts)


def cache_duration(duration):
    if CACHE_DEBUG:
        return 0
    else:
        return duration
