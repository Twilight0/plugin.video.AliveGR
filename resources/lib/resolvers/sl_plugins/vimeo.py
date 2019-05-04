import re

from streamlink.plugin import Plugin
from streamlink.stream import HLSStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags


class Vimeo(Plugin):

    _url_re = re.compile(r'https?://player\.vimeo\.com/video/\d+')

    @classmethod
    def can_handle_url(cls, url):

        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        res = self.session.http.get(self.url, headers=headers)
        tags = list(itertags(res.text, 'script'))

        m3u8 = [i for i in tags if u'VimeoPlayer' in i.text][0].text

        streams = re.findall(r'"url":"(.+?)"', m3u8)

        if streams:

            m3u8_stream = streams[1]

            for s in HLSStream.parse_variant_playlist(self.session, m3u8_stream).items():

                yield s


__plugin__ = Vimeo
