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


class Sigma(ResolveUrl):

    name = 'sigmatv'
    domains = ['sigmatv.com']
    pattern = r'(?://|\.)(sigmatv\.com)/((?:webtv|shows|live)/?.*)'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        if media_id == 'live':
            stream = re.search(r'''application/x-mpegurl" src="(.+\.m3u8)"''', res)
            if stream:
                stream = ''.join(['https:', stream.group(1)])
            else:
                raise ResolverError('Live stream not found')
        else:
            stream = re.search(r'''type="video/mp4" src="(//.+\.mp4)"''', res)

            if stream:
                stream = stream.group(1)
            elif 'You are not allowed to view this content' in res:
                raise ResolverError('Source website does not allow this content to be played')
            else:
                raise ResolverError('Video not found')

        return stream + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        return self._default_get_url(host, media_id, template='http://{host}/{media_id}')
