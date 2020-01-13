# -*- coding: utf-8 -*-
import re, json

from distutils.util import strtobool
from streamlink.plugin import Plugin, PluginArguments, PluginArgument
from streamlink.stream import HLSStream, HTTPStream
from streamlink.plugin.api.useragents import CHROME
from streamlink.plugin.api.utils import itertags


_url_re = re.compile(r"""https?://www\.alphatv\.gr/(?:live|show|web-tv|news)/(?:[\w-]+/(?:[\w-]+)/)?\??(?:\d+/[\w-]+/|vtype=player&vid=(?P<vid>\d+)&showId=(?P<show_id>\d+)(?:&year=(?P<year>\d{4}))?)?""")
_api_url = 'https://www.alphatv.gr/ajax/Isobar.AlphaTv.Components.PopUpVideo.PopUpVideo.PlayMedia/?vid={vid}&showId={show_id}'

class AlphaGr(Plugin):

    arguments = PluginArguments(PluginArgument("parse_hls", default='true'))

    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    def _get_streams(self):

        headers = {'User-Agent': CHROME}
        live = False

        res = self.session.http.get(self.url, headers=headers)

        if '/live' in self.url:
            stream = [i for i in list(itertags(res.text, 'div')) if 'data-liveurl' in i.attributes]
            stream = stream[0].attributes['data-liveurl']
            live = True
        else:
            if 'vtype' in self.url:
                vid = _url_re.match(self.url).group('vid')
                show_id = _url_re.match(self.url).group('show_id')
                res = self.session.http.get(_api_url.format(vid=vid, show_id=show_id), headers=headers)
            vid = [i for i in list(itertags(res.text, 'div')) if 'data-plugin-player' in i.attributes][0].attributes['data-plugin-player']
            try:
                stream = json.loads(self._replace_html_codes(vid.decode('utf-8')))['Url']
            except Exception:
                stream = json.loads(self._replace_html_codes(vid))['Url']

        headers.update({"Referer": self.url})

        try:
            parse_hls = bool(strtobool(self.get_option('parse_hls')))
        except AttributeError:
            parse_hls = True

        if parse_hls and live:
            return HLSStream.parse_variant_playlist(self.session, stream, headers=headers)
        else:
            return dict(stream=HTTPStream(self.session, stream, headers=headers))

    def _replace_html_codes(self, txt):

        try:
            from HTMLParser import HTMLParser
            unescape = HTMLParser().unescape
        except Exception:
            from html import unescape

        txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
        txt = unescape(txt)
        txt = txt.replace("&quot;", "\"")
        txt = txt.replace("&amp;", "&")
        txt = txt.replace("&#38;", "&")
        txt = txt.replace("&nbsp;", "")

        return txt

__plugin__ = AlphaGr
