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


class Star(ResolveUrl):

    name = 'star'
    domains = ['star.gr', 'starx.gr']
    pattern = r'(?://|\.)(starx?\.gr)/((?:video|lifestyle|eidiseis|show|tv)/(?:live-stream/|[\w\-=/]+))'
    player_url = 'https://cdnapisec.kaltura.com/p/713821/sp/0/playManifest/entryId/{0}/format/applehttp/protocol/https/flavorParamId/0/manifest.m3u8'

    def get_media_url(self, host, media_id):

        headers = {'User-Agent': common.RAND_UA}
        web_url = self.get_url(host, media_id)
        res = self.net.http_GET(web_url, headers=headers).content

        if media_id == 'tv/live-stream/':
            stream = re.search(r'data-video="(http.+)"', res)
            if stream:
                stream = stream.group(1)
            else:
                raise ResolverError('Live stream not found')
        elif host == 'starx.gr':
            try:
                vid = re.search(r"kalturaPlayer\('(?P<id>\w+)'", res)
                if not vid:
                    stream = re.search(r"videoPlayer\.onYouTubeIframeAPIReady\('([\w-]{11})'\);", res)
                    if stream:
                        return 'plugin://plugin.video.youtube/play/?video_id={}'.format(stream.group(1))
                    else:
                        raise ResolverError('Video not found')
                else:
                    stream = self.player_url.format(vid.group('id'))
            except Exception as e:
                raise ResolverError('Video not found')
        else:
            stream = re.search(r"'(http.+kaltura.+\.m3u8)'", res)
            if stream:
                stream = stream.group(1)
            else:
                raise ResolverError('VOD stream not found')

        return stream + helpers.append_headers(headers)

    def get_url(self, host, media_id):

        return self._default_get_url(host, media_id, template='https://www.{host}/{media_id}')
