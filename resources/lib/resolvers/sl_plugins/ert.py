# -*- coding: utf-8 -*-

import re
from streamlink.plugin import Plugin
from streamlink.plugin.api import http, validate, useragents
from streamlink.plugin.api.utils import itertags

YOUTUBE_URL = "https://www.youtube.com/watch?v={0}"

_youtube_id = re.compile(r'/embed/([\w-]+)(?:.+?/embed/([\w-]+)|)', re.M | re.S)

_url_re = re.compile(r'http(s)?://webtv\.ert\.gr/ert.+?/')


class Ert(Plugin):

    @classmethod
    def can_handle_url(cls, url):

        return _url_re.match(url)

    def _iframe(self):

        r = http.get(self.url, params={'User-Agent': useragents.CHROME})

        iframe_url = list(itertags(r.content, 'iframe'))[0].attributes['src']

        return iframe_url

    def _youtube_url_schema(self, link):

        req = http.get('http://extreme-ip-lookup.com/json/', params={'User-Agent': useragents.CHROME})
        j_son = req.json()

        _youtube_url_schema = validate.Schema(
            validate.all(
                validate.transform(_youtube_id.search),
                validate.any(
                    None,
                    validate.all(
                        validate.get(
                            2 if j_son['countryCode'] == 'GR' and (
                                'ertworld-live' not in link or 'ert1-live' not in link
                            ) else 1
                        ),
                        validate.text
                    )
                )
            )
        )

        return _youtube_url_schema

    def _get_streams(self):

        channel_id = http.get(self._iframe(), schema=self._youtube_url_schema(self.url))

        if channel_id:
            return self.session.streams(YOUTUBE_URL.format(channel_id))


__plugin__ = Ert
