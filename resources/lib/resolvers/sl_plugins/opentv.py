import re

from streamlink.compat import urljoin
from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.exceptions import NoStreamsError


class OpenTV(Plugin):

    _url_re = re.compile(r'https?://www\.tvopen\.gr/(?P<path>live|watch)(?:/\d+/[\w-]+)?')

    _param_re = re.compile(r"\$.getJSON\(\'(?P<param>.+?)[\?'](?:.+?cid: '(?P<id>\d+)')?")
    _base_link = 'https://www.tvopen.gr'

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        print self.url

        headers = {'User-Agent': CHROME}

        if self.url.endswith('/live'):
            live = True
        else:
            live = False

        res = self.session.http.get(self.url, headers=headers)

        match = self._param_re.search(res.text)

        param = match.group('param')

        if not live:
            param = '?'.join([param, 'cid={0}'.format(match.group('id'))])

        _json_url = urljoin(self._base_link, param)

        _json_object = self.session.http.get(_json_url, headers=headers).json()

        stream = _json_object.get('stream')

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if parse_hls:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(live=HTTPStream(self.session, stream, headers=headers))


__plugin__ = OpenTV
