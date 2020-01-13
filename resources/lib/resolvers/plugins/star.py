# -*- coding: utf-8 -*-

import re

from streamlink.plugin.api.utils import itertags
from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.exceptions import PluginError


class Star(Plugin):

    _url_re = re.compile(r'https?://www\.star\.gr/tv/(?:live-stream|psychagogia|enimerosi)/(?:[\w-]+/v/\d+/.+?/)?')
    _api_url = 'https://www.star.gr/tv/ajax/Atcom.Sites.StarTV.Components.Show.PopupSliderItems?showid={show_id}&type=Episode&itemIndex=0&seasonid={season_id}&single=false'
    _player_url = 'https://cdnapisec.kaltura.com/p/713821/sp/0/playManifest/entryId/{0}/format/applehttp/protocol/https/flavorParamId/0/manifest.m3u8'

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        if 'live-stream' in self.url:
            live = True
        else:
            live = False

        res = self.session.http.get(self.url, headers=headers)

        if live:

            html = [i.text for i in list(itertags(res.text, 'script'))]

            html = [i for i in html if 'm3u8' in i][0]

        else:

            try:
                show_id, season_id = re.search(r'data-showid="(\d+)".+?data-seasonid="(\d+)"', res.text).groups()
            except Exception:
                raise PluginError('Did not match regex patterns to pass into the playable url')

            html = self.session.http.get(self._api_url.format(show_id=show_id, season_id=season_id), headers=headers).text

        stream = re.search(r"(?P<url>http.+?\.m3u8)", html)

        if stream:
            stream = stream.group(1)
        else:
            stream = self._player_url.format(re.search(r'kaltura-player(\w+)', html).group(1))

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
