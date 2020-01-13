# -*- coding: utf-8 -*-
import re

from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags


_url_re = re.compile(r"""http://www\.alphacyprus\.com\.cy/(?:page|shows)/(?:live|all|entertainment|ellinikes-seires|informative)(?:/[\w-]+/webtv/[\w-]+)?""")


class AlphaCy(Plugin):

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = self.session.http.get(self.url, headers=headers)

        if 'page/live' in url:
            stream = [i for i in list(itertags(res.text, 'script')) if "type: 'hls'" in i.text]
            stream = re.search(r'''url: ['"](http.+?)['"]''', stream[0]).group(1)
            live = True
        else:
            stream = [i for i in list(itertags(html, 'script')) if "mp4" in i.text]
            stream = re.search(r'''url: ['"](http.+?\.mp4)['"]''', stream[0].text).group(1)
            live = False

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if parse_hls and live:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(vod=HTTPStream(self.session, stream, headers=headers))


__plugin__ = AlphaCy
