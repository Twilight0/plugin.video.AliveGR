# -*- coding: utf-8 -*-
# Not a true streamlink plugin, because its importing jsbeautifier which is not yet a dependency for upstream streamlink

import re

from jsbeautifier.unpackers.packer import unpack
from streamlink.plugin import Plugin
from streamlink.exceptions import PluginError
from streamlink.stream import HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags


class Cloudb(Plugin):

    _url_re = re.compile(r'https?://cloudb\.me/(?:embed-)?(?P<vid>\w+)\.html')

    _base_link = 'http://cloudb.me/embed-{0}.html'

    @classmethod
    def can_handle_url(cls, url):
        return cls._url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}

        self.url = self._base_link.format(self._url_re.match(self.url).group('vid'))

        res = self.session.http.get(self.url, headers=headers)

        try:

            obfuscated = [i.text for i in list(itertags(res.text, 'script')) if 'eval' in i.text][0]

            stream = unpack(obfuscated)

            stream = re.search(r'[\'"](.+?v\.mp4)[\'"]', stream).group(1)

            headers.update({"Referer": self.url})

            return dict(stream=HTTPStream(self.session, stream, headers=headers))

        except Exception:

            raise PluginError('Cloudb.me: Something went wrong')


__plugin__ = Cloudb
