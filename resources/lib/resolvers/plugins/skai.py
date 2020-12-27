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


class Skai(ResolveUrl):

    name = 'skai'
    domains = ['skai.gr', 'skaitv.gr']
    pattern = r'(?://|\.)(skai(?:tv)?\.gr)/((?:live|episode|videos).*)'
    player_url = 'http://videostream.skai.gr/'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        if media_id == 'live':

            stream = re.search(r'livestream":"(https.+?)"', res)

            if stream:
                stream = stream.group(1).replace('\\', '')
            else:
                raise ResolverError('Stream not found')

        elif 'videos' not in media_id:

            data = re.search(r'var data = ({.+?});', res)
            if not data:
                raise ResolverError('Stream not found')
            else:
                json_ = json.loads(data.group(1))
                stream = ''.join([self.player_url, json_['episode'][0]['media_item_file'], '.m3u8'])

        else:

            stream = re.search(r'"og:video" content=" ?(https://videostream\.skai\.gr/.+\.mp4\.m3u8)"', res)

            if stream:
                stream = stream.group(1)
            else:
                raise ResolverError('Stream not found')

        return stream + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        return self._default_get_url(host, media_id, template='https://www.{host}/{media_id}')
