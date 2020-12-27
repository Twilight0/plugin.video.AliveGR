# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import re
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError


class AlphaCY(ResolveUrl):

    name = 'alphacy'
    domains = ['alphacyprus.com.cy']
    pattern = r'(?://|\.)(alphacyprus\.com\.cy)/((?:page|shows|live)(?:/(?:all|entertainment|ellinikes-seires|informative|news)(?:/[\w-]+/webtv/[\w-]+)?)?)'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        stream = re.search(r'''['"](http.+(?:mp4|m3u8.+))['"]''', res)

        if stream:
            stream = stream.group(1)
        else:
            raise ResolverError('Video not found')

        return stream + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        return self._default_get_url(host, media_id, template='https://www.{host}/{media_id}')
