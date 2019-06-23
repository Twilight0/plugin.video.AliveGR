# # -*- coding: utf-8 -*-
import re

from math import pow
from streamlink.plugin import Plugin
from streamlink.compat import quote, range
from streamlink.plugin.api.useragents import CHROME
from streamlink.exceptions import NoStreamsError
from streamlink.stream import HTTPStream
from streamlink.plugin.api.utils import itertags


class Openload(Plugin):

    url_re = re.compile(r'https?://(?P<domain>o(?:pen)?load\.(?:io|co|tv|stream|win|download|info|icu|fun|pw))/(?:embed|f)/(?P<streamid>[\w-]+)')
    web_url = 'https://{0}/stream/{1}?mime=true'

    HEADERS = {
        'User-Agent': CHROME,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Charset': 'UTF-8',
        'Accept-Encoding': 'gzip'
    }

    @classmethod
    def can_handle_url(cls, url):

        return cls.url_re.match(url)

    def _location(self, url):

        url = quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        req = self.session.http.get(url, headers=self.HEADERS, allow_redirects=False)

        return dict(req.headers).get('Location')

    def _compute(self, code, parseInt, _0x59ce16, _1x4bfb36, domain):

        _0x1bf6e5 = ''
        ke = []

        for i in list(range(0, len(code[0:9 * 8]), 8)):
            ke.append(int(code[i:i + 8], 16))

        _0x439a49 = 0
        _0x145894 = 0

        while _0x439a49 < len(code[9 * 8:]):

            _0x5eb93a = 64
            _0x896767 = 0
            _0x1a873b = 0
            _0x3c9d8e = 0

            while 1:

                if _0x439a49 + 1 >= len(code[9 * 8:]):
                    _0x5eb93a = 143

                _0x3c9d8e = int(code[9 * 8 + _0x439a49:9 * 8 + _0x439a49 + 2], 16)
                _0x439a49 += 2

                if _0x1a873b < 6 * 5:
                    _0x332549 = _0x3c9d8e & 63
                    _0x896767 += _0x332549 << _0x1a873b
                else:
                    _0x332549 = _0x3c9d8e & 63
                    _0x896767 += int(_0x332549 * pow(2, _0x1a873b))

                _0x1a873b += 6

                if not _0x3c9d8e >= _0x5eb93a:
                    break

            _0x30725e = _0x896767 ^ ke[_0x145894 % 9] ^ parseInt ^ _1x4bfb36
            _0x2de433 = _0x5eb93a * 2 + 127

            for i in list(range(4)):

                _0x3fa834 = chr(((_0x30725e & _0x2de433) >> (9 * 8 / 9) * i) - 1)

                if _0x3fa834 != '$':

                    _0x1bf6e5 += _0x3fa834

                _0x2de433 = (_0x2de433 << int(9 * 8 / 9))

            _0x145894 += 1

        url = self.web_url.format(domain, _0x1bf6e5)

        return url

    def _get_streams(self):

        data = self.session.http.get(self.url, headers={'User-Agent': CHROME}).text

        if 'File not found ;' in data:
            raise NoStreamsError

        code = [i.text for i in list(itertags(data, 'p')) if 'style' in i.attributes][0]
        _0x59ce16 = eval(re.search(r'_0x59ce16=(0x\w{8})', data).group(1))
        _1x4bfb36 = eval(re.search(r'_1x4bfb36=(parseInt[()\',\d-]+?);', data).group(1).replace('parseInt', 'int'))
        integer = eval(re.search(r'_0x30725e,(\(parseInt.*?)\),', data).group(1).replace('parseInt', 'int'))
        domain = re.search(self.url_re, self.url).group('domain')
        link = self._compute(code, integer, _0x59ce16, _1x4bfb36, domain)
        video = self._location(link)

        del self.HEADERS['Accept-Charset']
        del self.HEADERS['Accept']

        self.HEADERS.update({'Referer': self.url})

        return dict(vod=HTTPStream(self.session, video, headers=self.HEADERS))


__plugin__ = Openload
