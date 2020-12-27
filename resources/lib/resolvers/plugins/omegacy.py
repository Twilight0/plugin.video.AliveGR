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


class OmegaCY(ResolveUrl):

    name = 'omegacy'
    domains = ['omegatv.com.cy']
    pattern = r'(?://|\.)(omegatv\.com\.cy)/(.+)'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        if media_id == 'live/':
            stream = re.search(r'''['"]src['"]: ['"](.+m3u8.+)['"]''', res)
        else:
            iframe = re.search(r'''iframe.+"(.+LiveMediaPlayer.+)"''', res).group(1)
            html = self.net.http_GET(iframe, headers=headers).content
            stream = re.search(r"file: '(http://.+?\.mp4.+?)'", html)

        if stream:
            stream = stream.group(1)
        else:
            raise ResolverError('Video not found')

        return stream + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        return self._default_get_url(host, media_id, template='http://www.{host}/{media_id}')
