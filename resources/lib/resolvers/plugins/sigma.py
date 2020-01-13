# -*- coding: utf-8 -*-
import re

from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags


_url_re = re.compile(r"""https?://www\.sigmatv\.com/(?:live|webtv|shows)(?:/view/\d+|/[\w-]+/episodes/\w+)?""")


class Sigma(Plugin):

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = self.session.http.get(self.url, headers=headers)

        if 'page/live' in self.url:
            stream = ''.join(['https:', [i for i in list(itertags(res.text, 'source'))][0].attributes['src']])
            live = True
        else:
            stream = [(i.attributes['type'], ''.join(['https:', i.attributes['src']])) for i in list(itertags(res.text, 'source'))[:-1]]
            live = False

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if live:
            if parse_hls:
                yield HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
            else:
                yield dict(live=HTTPStream(self.session, stream, headers=headers))
        else:
            for q, s in stream:
                yield q, HTTPStream(self.session, s, headers=headers)


__plugin__ = Sigma
