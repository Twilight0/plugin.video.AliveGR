# -*- coding: utf-8 -*-

import re, json

from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME


class SkaiGr(Plugin):

    _url_re = re.compile(r'http://www\.skaitv\.gr/episode/\w+/[\w-]+/[\d-]+')
    _player_url = 'http://videostream.skai.gr/'

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = self.session.http.get(self.url, headers=headers)

        json_ = re.search(r'var data = ({.+?});', res.text).group(1)

        json_ = json.loads(json_)

        stream = ''.join([self._player_url, json_['episode'][0]['media_item_file'], '.m3u8'])

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if parse_hls:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(vod=HTTPStream(self.session, stream, headers=headers))


__plugin__ = SkaiGr
