# -*- coding: utf-8 -*-
import re

from distutils.util import strtobool
from streamlink.compat import quote
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags
from streamlink.exceptions import NoStreamsError


class Rik(Plugin):

    _url_re = re.compile(r'https?://cybc\.com\.cy/(?:live-tv|video-on-demand)/(?:\u03c1\u03b9\u03ba|\xcf\x81\xce\xb9\xce\xba|%CF%81%CE%B9%CE%BA)-\w+/(?:.+?episodes.+?/)?', re.U)

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        self.url = self.url.replace(u'ρικ', quote(u'ρικ'.encode('utf-8')))

        get_page = self.session.http.get(self.url, headers=headers)

        tags = list(itertags(get_page.text, 'script'))

        if 'live-tv' in self.url:

            tag = [i for i in tags if 'm3u8' in i.text][0].text

            try:
                stream = re.search(r'''["'](http.+?\.m3u8)['"]''', tag).group(1)
            except IndexError:
                raise NoStreamsError('RIK Broadcast is currently disabled')

        else:

            tag = [i for i in tags if '.mp4' in i.text and 'sources' in i.text][0].text

            stream = re.search(r'''file: ['"](.+?\.mp4)['"]''', tag).group(1)

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if parse_hls and 'live-tv' in self.url:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(stream=HTTPStream(self.session, stream, headers=headers))


__plugin__ = Rik
