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

SCRAMBLE_1 = (
    'eJwVy8sKgkAUANBfiVmXzAz5qJ0ipYVQmKGrGMfrc3xrqdG/h/tzvqgH3sGAjhvkxkVHw6GzqpNxJqZPHZ/fSidA2w1iTfYqYF6Zbi/MnXXxCK2FTB'
    '7Rg4+o3EtmeE/msPFuXu14Ku11ZdEaZE3Be0KpohF1J9oExxxDeijGNyujtMWjwCAXap7TPAWJNU0vJXWdCBh76HhdDVANEq9L9PsD2lw48A=='
)

SCRAMBLE_2 = (
    'eJwVy80OgiAAAOBXcZzLqfhD3SzXqqHOXJcuzoghCkL+ZNZ69+b9+76gp6SjA9gaYFdJiGcfuVUC32x/PuaQyUM8gZUBSs2Lhs4LC0+fMp/Di0+KiU'
    'c4yTMfy9szSq82jiW2U8lEEmbL4o8l2BvLRhBB17OctTXekWZqaDqvFjCg/qtFIoCe47mEcFGbpda9yZRigo497YhqB9oOJlES/P42mTb7'
)

SCRAMBLE_3 = (
    'eJwVy90KgjAYANBXkV2XlL+zOzUhTSIysTsZc4pm+/xZS43ePbw/54tGRgcm0EFByyfapyWRu865lzfeADTVw40TtFEQ6er8yeaVueFCktkPbZkeJy'
    '8LPKLF/fmUR2IyLmDNewP8axasqy7WYGGMdVszsWkZ26bqoSeyrfWCtMzRuGbQQRSUUlnKAg8q6bpRrQCqlr1HNlDggnGhUnih3x/3kTk3'
)

SCRAMBLE_4 = (
    'eJwVy8EKgjAYAOBXkZ1TclOX3cxDKFFIFnqSuX6npNtySlj07uH9+77IAB9hQnsLiViFpCEiU36B8yXPzpTpVxqjjYWY7qonLCuLkg+7LrGuTMwPKR'
    '3vl7ddRa6mZVjYfSrKpDwNx9u6uscawoDgbeBR6gW2hBH3Hpsp+JISCnPQd7hu63baDaThrsO0No5QSvQwGxi5khPIyeFqQL8/GFw28Q=='
)

SCRAMBLE_5 = (
    'eJwVy90KgjAYANBXkV2XlL+zOzUhTSIysTsZc4pm+/xZS43ePbw/54tGRgcm0EFByyfapyWRu865lzfeADTVw40TtFEQ6er8yeaVueFCktkPbZkeJy'
    '8LPKLF/fmUR2IyLmDNewP8axasqy7WYGGMdVszsWkZ26bqoSeyrfWCtMzRuGbQQRSUUlnKAg8q6bpRrQCqlr1HNlDggnGhUnih3x/3kTk3'
)

SCRAMBLE_6 = (
    'eJwVzNsOgiAAANBfaTynEw3D3rSc2arlujz44pDwRgITcrPWvzc/4JwvaJ9gswAYIYigsw486Fp+UzUV9hRz1NgLbETHOZUjxw1EZmSBTZTSdi1l/W'
    'JvzQYqhWHC2FT2YLkARLUFZ9PchumHXKeI8FCe4HaXT64+x2VHHnhM85vl+kOWJfvVrDSjAzMzOgyqV7qIS/9ujklkBI6dSxL74PcHEj435A=='
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
