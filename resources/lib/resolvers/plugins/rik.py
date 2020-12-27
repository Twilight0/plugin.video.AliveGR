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


class Rik(ResolveUrl):

    name = 'rik'
    domains = ['cybc.com.cy']
    pattern = r'(?://|\.)(cybc\.com\.cy)/((?:live-tv|video-on-demand).+)'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        if 'live-tv' in media_id:
            stream = re.search(r'''file: ['"](http://.+?\.m3u8)['"]''', res)
        else:
            stream = re.search(r'''file: ['"](http://.+?\.mp4)['"]''', res)

        if stream:
            stream = stream.group(1)
        else:
            raise ResolverError('Video not found')

        return stream + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        return self._default_get_url(host, media_id, template='http://{host}/{media_id}')
