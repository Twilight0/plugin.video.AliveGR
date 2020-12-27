# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import re, json
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError

_subdomains = ['gr', 'www', 'fr', 'de', 'it', 'es', 'pt', 'ru', 'tr', 'hu', 'per', 'arabic']
_domains = ['.'.join([i, 'euronews.com']) for i in _subdomains]


class Euronews(ResolveUrl):

    name = 'euronews'
    domains = _domains + ['www.euronews.al']
    pattern = r'(\w{2,6}\.euronews\.com)/(?P<path>live|.*)'
    re_vod = re.compile(r'(?:<meta\s+property="og:video"\s+content="(?P<url>http.*?)"\s*/>|youtubevideoid\\":\\"(?P<id>[\w-]{11})\\")')
    live_api_url = "http://{0}/api/watchlive.json"
    headers = {'User-Agent': common.RAND_UA}

    def get_media_url(self, host, media_id):

        web_url = self.get_url(host, media_id)

        if media_id == 'live':
            stream = self._get_live_streams(host)
            if not stream:
                raise ResolverError('Live stream is probably geoblocked in your region')
            else:
                return stream + helpers.append_headers(self.headers)
        else:
            res = self.net.http_GET(web_url).content
            stream = self.re_vod.search(res)

            if stream.group('url'):
                stream = stream.group('url')
                return stream + helpers.append_headers(self.headers)
            elif stream.group('id'):
                stream = stream.group('id')
                return 'plugin://plugin.video.youtube/play/?video_id={}'.format(stream)
            else:
                raise ResolverError('This video is probably geoblocked in your region')

    def _get_live_streams(self, host):

        live_url = self.live_api_url.format(host)
        live_res = self.net.http_GET(live_url, headers=self.headers).content
        _json = json.loads(live_res)
        live_res = self.net.http_GET(''.join(['https:', _json.get('url')]), headers=self.headers).content
        _json = json.loads(live_res)
        if _json.get('status') == 'ko':
            return False
        elif _json.get('status') == 'ok':
            return _json.get('primary')
        else:
            raise ResolverError('Unknown error occured')

    def get_url(self, host, media_id):

        return self._default_get_url(host, media_id, template='https://{host}/{media_id}')
