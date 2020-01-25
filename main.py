# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

        License summary below, for more details please read license.txt file

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 2 of the License, or
        (at your option) any later version.
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import absolute_import, unicode_literals


########################################################################################################################

import sys
# noinspection PyUnresolvedReferences
from resources.lib.modules.tools import checkpoint
from tulip.compat import parse_qsl

########################################################################################################################

argv = sys.argv
params = dict(parse_qsl(argv[2].replace('?', '')))

########################################################################################################################

content = params.get('content_type')
action = params.get('action')
url = params.get('url')
image = params.get('image')
title = params.get('title')
name = params.get('name')
query = params.get('query')
plot = params.get('plot')
genre = params.get('genre')

########################################################################################################################

if content == 'video':
    from resources.lib.indexers import navigator
    navigator.Indexer().root()

elif content == 'audio':
    from resources.lib.indexers import navigator
    navigator.Indexer().audio()

elif content == 'image':
    from resources.lib.indexers import news
    news.Indexer().papers_index()

elif content == 'executable':
    from resources.lib.indexers import settings
    settings.Indexer().menu()

########################################################################################################################

elif action is None:
    from resources.lib.indexers import navigator
    navigator.Indexer().root()

########################################################################################################################

elif action == 'root':
    from tulip import control
    control.execute('ActivateWindow(videos,"plugin://plugin.video.AliveGR/?content=video")')

elif action == 'live_tv':
    from resources.lib.indexers import live
    live.Indexer().live_tv()

elif action == 'pvr_client':
    from resources.lib.modules import kodi
    kodi.pvr_client(query)

elif action == 'networks':
    from resources.lib.indexers import networks
    networks.Indexer().networks()

elif action == 'news':
    from resources.lib.indexers import news
    news.Indexer().news()

elif action == 'movies':
    from resources.lib.indexers import gm
    gm.Indexer().movies()

elif action == 'short_films':
    from resources.lib.indexers import gm
    gm.Indexer().short_films()

elif action == 'shows':
    from resources.lib.indexers import gm
    gm.Indexer().shows()

elif action == 'series':
    from resources.lib.indexers import gm
    gm.Indexer().series()

elif action == 'kids':
    from resources.lib.indexers import kids
    kids.Indexer().kids()

elif action == 'kids_live':
    from resources.lib.indexers import live
    live.Indexer().modular('30032')

elif action == 'cartoon_series':
    from resources.lib.indexers import gm
    gm.Indexer().cartoons_series()

elif action == 'cartoon_collection':
    from resources.lib.indexers import kids
    kids.Indexer().cartoon_collection()

elif action == 'cartoon_various':
    from resources.lib.indexers import kids
    kids.Indexer().cartoon_various(url)

elif action == 'educational':
    from resources.lib.indexers import kids
    kids.Indexer().educational()

elif action == 'kids_songs':
    from resources.lib.indexers import kids
    kids.Indexer().kids_songs()

elif action == 'listing':
    from resources.lib.indexers import gm
    gm.Indexer().listing(url)

elif action == 'episodes':
    from resources.lib.indexers import gm
    gm.Indexer().episodes(url)

elif action == 'sports':
    from resources.lib.indexers import sports
    sports.Indexer().sports()

elif action == 'gm_sports':
    from resources.lib.indexers import gm
    gm.Indexer().gm_sports()

elif action == 'sports_news':
    from resources.lib.indexers import sports
    sports.Indexer().sports_news()

elif action == 'events':
    from resources.lib.indexers import gm
    gm.Indexer().events(url)

elif action == 'theater':
    from resources.lib.indexers import gm
    gm.Indexer().theater()

# elif action == 'documentaries':
#     from resources.lib.indexers import documentaries
#     documentaries.Indexer().documentaries()
#
# elif action == 'yt_documentaries':
#     from resources.lib.indexers import documentaries
#     documentaries.Indexer().yt_documentaries()

elif action == 'miscellany':
    from resources.lib.indexers import miscellany
    miscellany.Indexer().miscellany()

elif action == 'audio':
    from resources.lib.indexers import navigator
    navigator.Indexer().audio()

elif action == 'music':
    from resources.lib.indexers import music
    music.Indexer().menu()

elif action == 'music_live':
    from resources.lib.indexers import live
    live.Indexer().modular('30125')

elif action == 'gm_music':
    from resources.lib.indexers import music
    music.Indexer().gm_music()

elif action == 'artist_index':
    from resources.lib.indexers import music
    music.Indexer().artist_index(url)

elif action == 'album_index':
    from resources.lib.indexers import music
    music.Indexer().album_index(url)

elif action == 'songs_index':
    from resources.lib.indexers import music
    music.Indexer().songs_index(url, name)

elif action == 'mgreekz_index':
    from resources.lib.indexers import music
    music.Indexer().mgreekz_index()

elif action == 'mgreekz_list':
    from resources.lib.indexers import music
    music.Indexer().mgreekz_list(url)

elif action == 'mgreekz_top10':
    from resources.lib.indexers import music
    music.Indexer().mgreekz_top10()

elif action == 'top20_list':
    from resources.lib.indexers import music
    music.Indexer().top20_list(url)

elif action == 'top50_list':
    from resources.lib.indexers import music
    music.Indexer().top50_list(url)

elif action == 'techno_choices':
    from resources.lib.indexers import music
    music.Indexer().techno_choices(url)

elif action == 'radio':
    from resources.lib.indexers import radios
    radios.Indexer().radio()

elif action == 'papers':
    from resources.lib.modules import helpers
    helpers.papers()

elif action == 'papers_index':
    from resources.lib.indexers import news
    news.Indexer().papers_index()

elif action == 'addBookmark':
    from tulip import bookmarks
    bookmarks.add(url)

elif action == 'deleteBookmark':
    from tulip import bookmarks
    bookmarks.delete(url)

elif action == 'pin':
    from resources.lib.modules import helpers
    helpers.pin()

elif action == 'unpin':
    from resources.lib.modules import helpers
    helpers.unpin()

elif action == 'bookmarks':
    from resources.lib.indexers import bookmarks
    bookmarks.Indexer().bookmarks()

elif action == 'search':
    from resources.lib.indexers import search
    search.Indexer().search()

elif action == 'settings':
    from resources.lib.indexers import settings
    settings.Indexer().menu()

elif action == 'tools_menu':
    from resources.lib.modules import helpers
    helpers.tools_menu()

elif action == 'openSettings':
    from tulip import control
    control.openSettings(query)

elif action == 'other_addon_settings':
    from resources.lib.modules import helpers
    helpers.other_addon_settings(query)

elif action in ['play', 'play_resolved']:
    # noinspection PyUnresolvedReferences
    from resources.lib.modules.player import player
    player(url, params, do_not_resolve=action == 'play_resolved')

elif action == 'directory':
    # noinspection PyUnresolvedReferences
    from resources.lib.modules.player import directory_picker
    directory_picker(url, argv=argv)

elif action == 'live_switcher':
    from resources.lib.indexers import live
    live.Indexer().switcher()

elif action == 'vod_switcher':
    from resources.lib.indexers import gm
    gm.Indexer().vod_switcher(url)

elif action == 'papers_switcher':
    from resources.lib.indexers import news
    news.Indexer().switcher()

elif action == 'setup_iptv':
    from resources.lib.modules import tools
    tools.setup_iptv()

elif action == 'enable_iptv':
    from resources.lib.modules import tools
    tools.enable_iptv()

elif action == 'enable_proxy':
    from resources.lib.modules import tools
    tools.enable_proxy_module()

elif action == 'setup_various_keymaps':
    from resources.lib.modules import tools
    tools.setup_various_keymaps(query)

elif action == 'add_to_playlist':
    from resources.lib.modules import kodi
    kodi.add_to_playlist()

elif action == 'clear_playlist':
    from resources.lib.modules import kodi
    kodi.clear_playlist()

elif action == 'toggle_watched':
    from resources.lib.modules import kodi
    kodi.toggle_watched()

elif action == 'toggle_debug':
    from resources.lib.modules import kodi
    kodi.toggle_debug()

elif action == 'skin_debug':
    from resources.lib.modules import kodi
    kodi.skin_debug()

elif action == 'reload_skin':
    from resources.lib.modules import kodi
    kodi.reload_skin()

elif action == 'skin_choice':
    from resources.lib.modules import kodi
    kodi.skin_choice()

elif action == 'cache_clear':
    from resources.lib.modules import helpers
    helpers.cache_clear()

elif action == 'cache_delete':
    from resources.lib.modules import helpers
    helpers.cache.delete()

elif action == 'purge_bookmarks':
    from resources.lib.modules import helpers
    helpers.purge_bookmarks()

elif action == 'refresh':
    from resources.lib.modules import helpers
    helpers.refresh()

elif action == 'refresh_and_clear':
    from resources.lib.modules import helpers
    helpers.refresh_and_clear()

elif action == 'reset_idx':
    from resources.lib.modules import helpers
    helpers.reset_idx(force=query == 'force')

elif action == 'yt_setup':
    from resources.lib.modules import tools
    tools.yt_setup()

elif action == 'isa_enable':
    from resources.lib.modules import tools
    tools.isa_enable()

elif action == 'rtmp_enable':
    from resources.lib.modules import tools
    tools.rtmp_enable()

elif action == 'changelog':
    from resources.lib.modules import tools
    tools.changelog()

elif action == 'developer_mode':
    from resources.lib.modules import tools
    tools.dev()

elif action == 'info':
    from resources.lib.indexers import settings
    settings.Indexer().info()

elif action == 'input_stream_addons':
    from resources.lib.indexers import settings
    settings.Indexer().input_stream_addons()

elif action == 'call_info':
    from resources.lib.modules import helpers
    helpers.call_info()

elif action == 'open_link':
    from tulip import control
    control.open_web_browser(url)

elif action == 'force':
    from resources.lib.modules import kodi
    kodi.force()

elif action == 'dmca':
    from resources.lib.modules import tools
    tools.dmca()

elif action == 'pp':
    from resources.lib.modules import tools
    tools.pp()

elif action == 'system_info':
    from resources.lib.modules import kodi
    kodi.system_info()

elif action == 'lang_choice':
    from resources.lib.modules import kodi
    kodi.lang_choice()

elif action == 'toggle_alt':
    from resources.lib.modules import helpers
    helpers.toggle_alt()

elif action == 'quit':
    from tulip.control import quit_kodi
    quit_kodi()

elif action == 'global_settings':
    from resources.lib.modules import kodi
    kodi.global_settings()

elif action == 'pvrsettings':
    from resources.lib.modules import kodi
    kodi.pvrsettings()

elif action == 'activate_audio_addon':
    from resources.lib.modules import helpers
    helpers.activate_audio_addon(url, query=query)

elif action == 'welcome':
    from resources.lib.modules import tools
    tools.welcome()

elif action == 'kodi_log_upload':
    from resources.lib.modules import helpers
    helpers.kodi_log_upload()

# Reserved might use later:
# elif action == 'report':
#     from resources.lib.modules import tools
#     tools.mailer(text=title)


if __name__ == '__main__':

    checkpoint()
