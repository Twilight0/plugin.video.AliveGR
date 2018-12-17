import re

from streamlink.plugin import Plugin
from streamlink.stream import HLSStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags
from streamlink.compat import urlencode


class OmegaCy(Plugin):

    _url_re = re.compile(r'https?://www\.omegatv\.com\.cy/live/')

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        cookie = urlencode(dict(self.session.http.head(self.url, headers={'User-Agent': CHROME}).cookies.items()))
        headers.update({'Cookie': cookie})
        res = self.session.http.get(self.url, headers=headers)
        tags = list(itertags(res.text, 'script'))

        m3u8 = [i for i in tags if i.text.startswith(u'var playerInstance')][0].text

        stream = re.findall('"(.+?)"', m3u8)[1]

        headers.update({"Referer": self.url})
        del headers['Cookie']

        for s in HLSStream.parse_variant_playlist(self.session, stream, headers=headers).items():

            yield s


__plugin__ = OmegaCy
