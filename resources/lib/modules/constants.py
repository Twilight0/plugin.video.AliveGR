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

SCRAMBLE_0 = (
    'eJwVzNsKgjAYAOBXiV2XbCMPdadIaSEUZuhVzPl7nGctNXr38AG+74uyCB03SNYUvCeUKhpRd6JNcMwxpIdifLMySls8CgxyoeY5zVOQWNP0UlLXiY'
    'Cxh47X1QDVIPG6RNsNYk32KmBeW91emDvr4hFaC5k8ogcfUbmXzPCezGHj3bza8VTaq+qBdzCsyI2LjoZDZ1Un40xMnzo+v5VOgH5/P3M48A=='
)

SCRAMBLE_1 = (
    'eJwVzNsOgiAAANBfcTyXU/FCvVmuVUOduV56cUYMURDyklnr35sfcM4X8AfYGsDeWDaCCLqe5ayt8Y40U0PTebWAAfVfLRIB9BzPJYSL2iy17k2mFB'
    'N07GlHVDvQdjCJkmBlgFLzoqHz0oanT5nP4cUnxcQjnOSZj+XtGaVXG8cS26lkIgmzRfWUdHRY0K6SEM8+cqsEvtn+fMwhk4d4Ar8/krE2+w=='
)

SCRAMBLE_2 = (
    'eJwVzN0KgjAYANBXkV2XlL+zOzUhTSIysTsZc4pm+/xZS43ePXyAc76oLtBBQRbGWLc1E5uWsW2qHnoi21ovSMscjWsGHURBKZWlLPCgkq4b1Qqgat'
    'l7ZAMFLhgXKoUX2iiIdHX+ZPPauuFCktkPbZkeJy8LPKLF/fmUR2IyLmDNewP8axasamR0YGJFyyfapyWRu865lzfeADTVw40T9PsDY3A5Nw=='
)

SCRAMBLE_3 = (
    'eJwVzN0KgjAYANBXiV2nzL9p3VlKhBFoYLEbGfphw59N3YoVvXv4AOd8EW/QfoMCjB0cEA8TL7BGorXfR+6LdZMaoq4J9eK22GXMiRwycZtJuditEG'
    '0PeoG5FqOCUdm1GNB2g5jkVQdmbePzh93MQT7hQjVkpjqxiZeOTnNe5BDS3ihKrXRVC9QzqBUlu9Yzxfg43vOrGsBPSh779J2h3x/Yvzg/'
)

SCRAMBLE_4 = (
    'eJwVzNsKgjAAANBfkT2n6FSmvYmFiBaEgdWL2DacudzavGTRv4cfcM4XtARsDQBt23ND5AbIR+bEOHJ8F1JFJGyIoynhbJp80XWB0i2xaim11QjRcD'
    'pqqrDoB9oPFhZPsDFALduqo8vaRumnLpZYJUWJdnJuH+Se5yFbrsf3+VXtyShiJHiwKk2xosOKmjQ5lCdmcpxF3s1mwyWbR+hh8PsDOlU4+A=='
)

SCRAMBLE_5 = (
    'eJwVzEkOgjAUANCrkK6FUJDJnVFAI4jEYNQNwfaHqaWMCzDe3XCA976opGgnIdO0sIUdSzMcLKuFzgvV1qjd4Wabc8acybZKCp1eTRWvlaxtByUXIm'
    'cwDdAT0YzQjAoRHG0klLVlWsO8tvvzkt3nw0ecBpfQyLkG78VPYta9YrdmkJGoDWsermoA0sO4osBL8M2InwJERbtUzh8XPy69I/r9AeCkOHc='
)

########################################################################################################################

ART_ID = 'resource.images.alivegr.artwork'
LOGOS_ID = 'resource.images.alivegr.logos'
PLUGINS_ID = 'script.module.resolveurl.pluginsgr'
PLUGINS_PATH = 'special://home/addons/{0}/resources/plugins/'.format(PLUGINS_ID)
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
SUPPORT = 'https://github.com/Twilight0/plugin.video.AliveGR/issues'

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
