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


class AlphaGR(ResolveUrl):

    name = 'alphagr'
    domains = ['alphatv.gr']
    pattern = r'(?://|\.)(alphatv\.gr)/(?:show/[\w-]+/(?:[\w-]+)?/\?vtype=player&vid=)?(news/.+|\d+&showId=\d+&year=\d{4}|live)'
    api_url = 'https://www.alphatv.gr/ajax/Isobar.AlphaTv.Components.PopUpVideo.PopUpVideo.PlayMedia/?vid={vid}&showId={show_id}&year={year}'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        if media_id == 'live':

            stream = re.search(r'data-liveurl="(https.+m3u8)"', res)

            if stream:
                stream = stream.group(1)
            else:
                raise ResolverError('Live stream not found')

        else:

            stream = re.search(r'(https.+mp4.+?)&quot', res)

            if stream:
                stream = stream.group(1)
            else:
                raise ResolverError('Video not found')

        return stream + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        if media_id == 'live':

            return self._default_get_url(host, media_id, template='https://www.{host}/{media_id}/')

        elif 'news' in media_id:

            return self._default_get_url(host, media_id, template='https://www.{host}/{media_id}')

        else:

            vid, show_id, year = re.search(r'(\d+)&showId=(\d+)&year=(\d{4})', media_id).groups()

            template = self.api_url.format(vid=vid, show_id=show_id, year=year)

            return self._default_get_url(host, media_id, template=template)
