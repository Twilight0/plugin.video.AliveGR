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


class Ant1cy(ResolveUrl):

    name = 'ant1gr'
    domains = ['ant1.com.cy']
    pattern = r'(?://|\.)(ant1\.com\.cy)/(?:webtv/show-page/(?:episodeinner|episodes)/\?show(?:ID)?=)?((?:\d+&episodeID=\d+|web-tv-live))'

    def __init__(self):

        self.api_url = 'https://www.ant1.com.cy/ajax.aspx?m=Atcom.Sites.Ant1iwo.Modules.TokenGenerator&videoURL={0}'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        if 'web-tv-live' in web_url:

            m3u8 = re.search(r'''["'](http.+?\.m3u8)['"]''', res)

            if m3u8:
                m3u8 = m3u8.group(1)
            else:
                raise ResolverError('Ant1 CY Broadcast is currently disabled')

        else:

            try:
                m3u8 = re.search(r"&quot;(http.+?master\.m3u8)&quot;", res).group(1)
            except Exception:
                raise ResolverError('Video not found')

        stream = self.net.http_GET(self.api_url.format(m3u8), headers=headers).content

        return stream + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        if 'web-tv-live' in media_id:

            return self._default_get_url(host, media_id, template='https://www.{host}/{media_id}/')

        else:

            show_id, episodeid = re.search(r'(\d+)&episodeID=(\d+)', media_id).groups()

            template = 'https://www.{0}/webtv/show-page/episodes/?show={1}&episodeID={2}'.format(host, show_id, episodeid)

            return self._default_get_url(host, media_id, template=template)
