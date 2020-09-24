# -*- coding: utf-8 -*-
import re

from streamlink.plugin import Plugin
from streamlink.stream import HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.compat import urlparse

_url_re = re.compile(r'https?://kineskop\.tv/\?page=watch&ch=\d+')


class Kineskop(Plugin):

    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        origin = '{0}://{1}/'.format(urlparse(self.url).scheme, urlparse(self.url).netloc)

        headers.update({'Origin': origin, 'Referer': self.url})

        res = self.session.http.get(self.url, headers=headers)

        stream = re.search(r"getURLParam\('src','(.+?)'", res.text)

        if stream:

            return dict(stream=HTTPStream(self.session, stream.group(1), headers=headers))


__plugin__ = Kineskop
