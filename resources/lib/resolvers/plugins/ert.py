# -*- coding: utf-8 -*-
import re, json

from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags
from streamlink.plugin.api import validate


class Ert(Plugin):

    _url_re = re.compile(r'https?://(?:webtv|archive|www)\.ert(?:flix)?\.gr/(?:\d+/|\w+-live/|[\w-]+/[\w-]+/[\w-]+/)')

    arguments = PluginArguments(
        PluginArgument("parse_hls", default='true'), PluginArgument("force_gr_stream", default='false')
    )

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = self.session.http.get(self.url, headers=headers)

        iframe = list(itertags(res.text, 'iframe'))[0].attributes['src']

        res = self.session.http.get(iframe, headers=headers)
        streams = re.findall(r'var (?:HLSLink|stream)(?:ww)?\s+=\s+[\'"](.+?)[\'"]', res.text)

        try:
            force_gr = bool(strtobool(self.get_option('force_gr_stream')))
        except AttributeError:
            force_gr = True

        if (len(streams) == 2 and self._geo_detect()) or force_gr:
            stream = streams[0]
        else:
            stream = streams[-1]

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if parse_hls:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(vod=HTTPStream(self.session, stream, headers=headers))

    def _geo_detect(self):

        _json = self.session.http.get('https://geoip.siliconweb.com/geo.json').text

        _json = json.loads(_json)

        if 'GR' in _json['country']:
            return True


__plugin__ = Ert

