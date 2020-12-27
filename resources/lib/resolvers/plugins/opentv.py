# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import re, json
from six.moves.urllib_parse import urljoin
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl, ResolverError


class OpenTV(ResolveUrl):

    name = 'tvopen'
    domains = ['tvopen.gr']
    pattern = r'(?://|\.)(tvopen\.gr)/(?:embed|watch)?/?(\d+|live)'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        base_link = 'https://www.tvopen.gr'
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        param_re = re.compile(r"\$.getJSON\(\'(?P<param>.+?)[?'](?:.+?cid: '(?P<id>\d+)')?")

        try:
            match = param_re.search(res)

            param = match.group('param')

            if media_id != 'live':
                param = '?'.join([param, 'cid={0}'.format(match.group('id'))])
        except Exception:
            raise ResolverError('Video not found')

        json_url = urljoin(base_link, param)

        _json = self.net.http_GET(json_url, headers=headers).content

        stream = json.loads(_json).get('stream')

        if not stream:

            raise ResolverError('Video not found')

        return stream.strip() + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        if media_id == 'live':

            return self._default_get_url(host, media_id, template='https://www.{host}/{media_id}/')

        else:

            template = 'https://www.{0}/embed/{1}'.format(host, media_id)

            return self._default_get_url(host, media_id, template=template)
