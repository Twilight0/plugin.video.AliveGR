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

        # if 'live-stream' in self.url:
        #     live = True
        # else:
        #     live = False

        res = self.session.http.get(self.url, headers=headers)

        script = [i.text for i in list(itertags(res.text, 'script'))]

        script = [i for i in script if 'm3u8' in i][0]

        stream = re.search(r"(?P<url>http.+?\.m3u8)", script).group('url')

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if parse_hls:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(live=HTTPStream(self.session, stream, headers=headers))


__plugin__ = StarGr
