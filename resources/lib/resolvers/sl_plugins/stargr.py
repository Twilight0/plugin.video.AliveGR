# -*- coding: utf-8 -*-

import re

from streamlink.plugin.api.utils import itertags
from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.exceptions import NoStreamsError


class StarGr(Plugin):

    _url_re = re.compile(r'https?://www\.star\.gr/tv/live-stream/')

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = self.session.http.get(self.url, headers=headers)

        script = [i.text for i in list(itertags(res.text, 'script'))][16]

        stream = re.search(r"'(?P<url>.+?\.m3u8)'", script).group('url')

        if self.session.http.head(stream).status_code == 404:
            raise NoStreamsError('Live stream is disabled due to 3rd party broacasts with no rights for web streams')

        headers.update({"Referer": self.url})

        parse_hls = bool(strtobool(self.get_option('parse_hls')))

        if parse_hls:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(live=HTTPStream(self.session, stream, headers=headers))


__plugin__ = StarGr
