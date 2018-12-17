import re

from streamlink.plugin import Plugin
from streamlink.stream import HLSStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags
from streamlink.exceptions import NoStreamsError


class Ant1Cy(Plugin):

    _url_re = re.compile(r'https?://www\.ant1\.com\.cy/web-tv-live/')
    _live_api_url = 'https://www.ant1.com.cy/ajax.aspx?m=Atcom.Sites.Ant1iwo.Modules.TokenGenerator&videoURL={0}'

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        get_page = self.session.http.get(self.url, headers=headers)

        try:
            m3u8 = re.findall("'(.+?)'", list(itertags(get_page.text, 'script'))[-2].text)[1]
        except IndexError:
            raise NoStreamsError

        stream = self.session.http.post(self._live_api_url.format(m3u8), headers=headers).text

        headers.update({"Referer": self.url})

        return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)


__plugin__ = Ant1Cy
