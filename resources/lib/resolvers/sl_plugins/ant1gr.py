import re

from streamlink.compat import urljoin
from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.exceptions import NoStreamsError

class Ant1Gr(Plugin):

    _url_re = re.compile(r'https?://www\.antenna\.gr/Live')
    _param_re = re.compile(r'\$.getJSON\(\'(?P<param>.+?)\?')
    _base_link = 'http://www.antenna.gr'

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = self.session.http.get(self.url, headers=headers)

        param = self._param_re.search(res.text).group('param')

        _json_url = urljoin(self._base_link, param)

        _json_object = self.session.http.get(_json_url, headers=headers).json()

        stream = _json_object.get('url')

        if stream.endswith('.mp4'):
            raise NoStreamsError('Stream is probably geo-locked to Greece')

        headers.update({"Referer": self.url})

        parse_hls = bool(strtobool(self.get_option('parse_hls')))

        if parse_hls:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(live=HTTPStream(self.session, stream, headers=headers))


__plugin__ = Ant1Gr
