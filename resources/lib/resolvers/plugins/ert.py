# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import json
import re
from six.moves import urllib_request, urllib_error
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError


class Ert(ResolveUrl):

    name = 'ert'
    domains = ['webtv.ert.gr', 'www.ertflix.gr', 'archive.ert.gr']
    pattern = r'//((?:www|archive|webtv)\.ert(?:flix)?\.gr)/(.+)'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content
        iframe = re.search(r'''iframe src=['"](https.+?)['"]''', res)

        if not iframe:
            raise ResolverError('Video not found')
        else:
            iframe = iframe.group(1)

        html = self.net.http_GET(iframe, headers=headers).content
        streams = re.findall(r'''(?:HLSLink|var stream(?:ww)?) = ['"](https.+)['"]''', html)

        if not streams:
            raise ResolverError('Error in searching urls from within the html')

        if '-live' in media_id:

            if self._geo_detect():
                stream = [i for i in streams if 'ww' not in i][0]
            else:
                stream = [i for i in streams if 'ww' in i][0]

            return stream + helpers.append_headers(headers)

        else:

            if len(streams) >= 2:

                url = [s for s in streams if 'dvrorigingr' in s or 'archive' in s][0]

                try:
                    video_ok = self._test_stream(url)
                except Exception:
                    video_ok = None

                if video_ok:

                    return url + helpers.append_headers(headers)

                else:

                    url = [s for s in streams if 'dvrorigin' in s][0]

                    return url + helpers.append_headers(headers)

            else:

                return streams[0] + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        return self._default_get_url(host, media_id, 'https://{host}/{media_id}')

    @common.cache.cache_method(cache_limit=24)
    def _geo_detect(self):

        _json = self.net.http_GET('https://geoip.siliconweb.com/geo.json').content

        _json = json.loads(_json)

        if 'GR' in _json['country']:
            return True

    def _test_stream(self, url):

        try:
            request = urllib_request.Request(url)
            request.get_method = lambda: 'HEAD'
            http_code = urllib_request.urlopen(request, timeout=15).getcode()
        except urllib_error.HTTPError as e:
            if isinstance(e, urllib_error.HTTPError):
                http_code = e.code
                if http_code == 405:
                    http_code = 200
            else:
                http_code = 600
        except urllib_error.URLError as e:
            http_code = 500
            if hasattr(e, 'reason'):
                if 'unknown url type' in str(e.reason).lower():
                    return True

        except Exception as e:
            http_code = 601
            msg = str(e)
            if msg == "''":
                http_code = 504

        return int(http_code) < 400 or int(http_code) == 504

