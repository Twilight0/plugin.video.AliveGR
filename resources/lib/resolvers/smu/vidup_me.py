"""
    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
import json
import urllib
import urllib2
from urlresolver import common
from urlresolver.common import i18n
from urlresolver.plugins.lib import helpers
from urlresolver.resolver import UrlResolver, ResolverError


class VidUpMeResolver(UrlResolver):
    name = "vidup.me"
    domains = ["vidup.me"]
    pattern = '(?://|\.)(vidup\.me)/(?:embed-|download/)?([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()
        self.headers = {'User-Agent': common.SMU_USER_AGENT}

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {
            'Referer': web_url
        }
        headers.update(self.headers)
        html = self.net.http_GET(web_url, headers=headers).content
        sources = helpers.parse_sources_list(html)
        if sources:
            if len(sources) > 1:
                try: sources.sort(key=lambda x: int(re.sub("\D", '', x[0])), reverse=True)
                except: common.logger.log_debug('Scrape sources sort failed |int(re.sub(r"""\D""", '', x[0])|')

            result = self.__auth_ip(media_id)
            if 'vt' in result:
                vt = result['vt']
                del result['vt']
                return helpers.pick_source(sources) + '?' + urllib.urlencode({'vt': vt}) + helpers.append_headers(self.headers)
            else:
                raise ResolverError('Video Token Missing')

        else:
            raise ResolverError('File not found')

    def __auth_ip(self, media_id):
        header = i18n('vidup_auth_header')
        line1 = i18n('auth_required')
        line2 = i18n('visit_link')
        line3 = i18n('click_pair') % ('https://vidup.me/pair')
        with common.kodi.CountdownDialog(header, line1, line2, line3) as cd:
            return cd.start(self.__check_auth, [media_id])
        
    def __check_auth(self, media_id):
        common.logger.log('Checking Auth: %s' % (media_id))
        url = 'https://vidup.me/pair?file_code=%s&check' % (media_id)
        try: js_result = json.loads(self.net.http_GET(url, headers=self.headers).content)
        except ValueError:
            raise ResolverError('Unusable Authorization Response')
        except urllib2.HTTPError as e:
            if e.code == 401:
                js_result = json.loads(e.read())
            else:
                raise

        common.logger.log('Auth Result: %s' % (js_result))
        if js_result.get('status'):
            return js_result.get('response', {})
        else:
            if re.match('file\s*\w*\s*not\s*\w*\s*found', str(js_result.get('response', '')), re.IGNORECASE):
                raise ResolverError('File not found')
            return {}
        
    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id)
