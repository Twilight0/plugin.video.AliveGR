# -*- coding: utf-8 -*-

import re

from streamlink.plugin.api.utils import itertags
from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.exceptions import PluginError


class Star(Plugin):

    _url_re = re.compile(r'https?://www\.starx?\.gr/(?:tv|show)/(?:live-stream/|(?:psychagogia|enimerosi|[\w-]+)/[\w-]+/(?:[\w-]+-\d+/|\d+))')
    _player_url = 'https://cdnapisec.kaltura.com/p/713821/sp/0/playManifest/entryId/{0}/format/applehttp/protocol/https/flavorParamId/0/manifest.m3u8'

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = self.session.http.get(self.url, headers=headers)

        if 'live-stream' in self.url:

            html = [i.text for i in list(itertags(res.text, 'script'))]

            html = [i for i in html if 'm3u8' in i][0]

            stream = re.search(r"(?P<url>http.+?\.m3u8)", html)

        elif 'starx' in self.url:

            try:
                vid = re.search(r"kalturaPlayer\('(?P<id>\w+)'", res.text).group('id')
                stream = self._player_url.format(vid)
            except Exception:
                stream = None

        else:

            stream = re.search(r"(?P<url>http.+?\.m3u8)", res.text)

        if not stream:
            raise PluginError('Did not find the playable url')
        elif 'starx' not in self.url:
            stream = stream.group('url')

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if parse_hls:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(stream=HTTPStream(self.session, stream, headers=headers))


__plugin__ = Star
