# -*- coding: utf-8 -*-
import re

from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags


class Ert(Plugin):

    _url_re = re.compile(r'https?://(?:webtv|archive)\.ert\.gr/(?:\d+/|[\w-]+/[\w-]+/[\w-]+/)')

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = self.session.http.get(self.url, headers=headers)

        iframe = list(itertags(res.text, 'iframe'))[0].attributes['src']

        res = self.session.http.get(iframe, headers=headers)
        stream = re.search(r'(?<!//)var (?:HLSLink|stream) = [\'"](.+?)[\'"]', res.text).group(1)

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if parse_hls:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(vod=HTTPStream(self.session, stream, headers=headers))


__plugin__ = Ert
