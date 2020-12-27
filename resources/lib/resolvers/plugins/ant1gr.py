# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

import json
import re
from six.moves.urllib_parse import urljoin
from resolveurl import common
from resolveurl.plugins.lib import helpers
from resolveurl.resolver import ResolveUrl


class Ant1gr(ResolveUrl):

    name = 'ant1gr'
    domains = ['antenna.gr', 'netwix.gr']
    pattern = r'(?://|\.)((?:antenna|netwix)\.gr)/(?:watch|embed)?/?(\d+|Live)'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}

        base_link = 'http://www.{0}'.format(host)
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content
        param_re = re.compile(r"\$.getJSON\(\'(?P<param>.+?)[?'](?:.+?cid: '(?P<id>\d+)')?")
        match = param_re.search(res)
        param = match.group('param')
        param = '?'.join([param, 'cid={0}'.format(match.group('id'))])

        _url = urljoin(base_link, param)
        if 'antenna.gr' in _url:
            _url = _url.replace('http', 'https')
        _json = json.loads(self.net.http_GET(_url, headers=headers).content)
        stream = _json.get('url')

        return stream + helpers.append_headers(headers)

    def get_url(self, host, media_id):
        if media_id == 'Live':
            return self._default_get_url(host, media_id, 'http://www.{host}/{media_id}')
        else:
            return self._default_get_url(host, media_id, 'http://www.{host}/embed/{media_id}')
