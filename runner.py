# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Thgiliwt

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

from resources.lib import action, content, title, url, query, plot, genre, name

########################################################################################################################

if content == 'video':
    from resources.lib.indexers import navigator
    navigator.Main().root()

elif content == 'audio':
    from resources.lib.indexers import navigator
    navigator.Main().audio()

elif content == 'image':
    from resources.lib.indexers import news
    news.Main().papers_index()

elif content == 'executable':
    from resources.lib.indexers import settings
    settings.Main().menu()

########################################################################################################################

elif action is None:
    from resources.lib.indexers import navigator
    navigator.Main().root()

elif action == 'live_tv':
    from resources.lib.indexers import live
    live.Main().live_tv()

elif action == 'pvr_client':
    from resources.lib.modules import helpers
    helpers.pvr_client(query)

elif action == 'networks':
    from resources.lib.indexers import networks
    networks.Main().networks()

elif action == 'news':
    from resources.lib.indexers import news
    news.Main().news()

elif action == 'movies':
    from resources.lib.indexers import gm
    gm.Main().movies()

elif action == 'short_films':
    from resources.lib.indexers import gm
    gm.Main().short_films()

elif action == 'shows':
    from resources.lib.indexers import gm
    gm.Main().shows()

elif action == 'series':
    from resources.lib.indexers import gm
    gm.Main().series()

elif action == 'kids':
    from resources.lib.indexers import kids
    kids.Main().kids()

elif action == 'kids_live':
    from resources.lib.indexers import live
    live.Main().modular('30032')

elif action == 'cartoon_series':
    from resources.lib.indexers import gm
    gm.Main().cartoons_series()

elif action == 'cartoon_collection':
    from resources.lib.indexers import kids
    kids.Main().cartoon_collection()

elif action == 'educational':
    from resources.lib.indexers import kids
    kids.Main().educational()

elif action == 'kids_songs':
    from resources.lib.indexers import kids
    kids.Main().kids_songs()

elif action == 'listing':
    from resources.lib.indexers import gm
    gm.Main().listing(url)

elif action == 'episodes':
    from resources.lib.indexers import gm
    gm.Main().episodes(url)

elif action == 'sports':
    from resources.lib.indexers import sports
    sports.Main().sports()

elif action == 'gm_sports':
    from resources.lib.indexers import gm
    gm.Main().gm_sports()

elif action == 'sports_news':
    from resources.lib.indexers import sports
    sports.Main().sports_news()

elif action == 'events':
    from resources.lib.indexers import gm
    gm.Main().events(url)

elif action == 'theater':
    from resources.lib.indexers import gm
    gm.Main().theater()

elif action == 'documentaries':
    from resources.lib.indexers import documentaries
    documentaries.Main().documentaries()

elif action == 'yt_documentaries':
    from resources.lib.indexers import documentaries
    documentaries.Main().yt_documentaries()

elif action == 'miscellany':
    from resources.lib.indexers import miscellany
    miscellany.Main().miscellany()

elif action == 'audio':
    from resources.lib.indexers import navigator
    navigator.Main().audio()

elif action == 'music':
    from resources.lib.indexers import music
    music.Main().menu()

elif action == 'music_live':
    from resources.lib.indexers import live
    live.Main().modular('30125')

elif action == 'gm_music':
    from resources.lib.indexers import music
    music.Main().gm_music()

elif action == 'artist_index':
    from resources.lib.indexers import music
    music.Main().artist_index(url)

elif action == 'album_index':
    from resources.lib.indexers import music
    music.Main().album_index(url)

elif action == 'songs_index':
    from resources.lib.indexers import music
    music.Main().songs_index(url, name)

elif action == 'mgreekz_index':
    from resources.lib.indexers import music
    music.Main().mgreekz_index()

elif action == 'mgreekz_top10':
    from resources.lib.indexers import music
    music.Main().mgreekz_top10()

elif action == 'top20_list':
    from resources.lib.indexers import music
    music.Main().top20_list(url)

elif action == 'radio':
    from resources.lib.indexers import radios
    radios.Main().radio()

elif action == 'papers':
    from resources.lib.modules import helpers
    helpers.papers()

elif action == 'papers_index':
    from resources.lib.indexers import news
    news.Main().papers_index()

elif action == 'addBookmark':
    from tulip import bookmarks
    bookmarks.add(url)

elif action == 'deleteBookmark':
    from tulip import bookmarks
    bookmarks.delete(url)

elif action == 'bookmarks':
    from resources.lib.indexers import bookmarks
    bookmarks.Main().bookmarks()

elif action == 'search':
    from resources.lib.indexers import search
    search.Main().search()

elif action == 'settings':
    from resources.lib.indexers import settings
    settings.Main().menu()

elif action == 'tools_menu':
    from resources.lib.modules import helpers
    helpers.tools_menu()

elif action == 'openSettings':
    from tulip import control
    control.openSettings(query)

elif action == 'smu_settings':
    from resources.lib.modules import helpers
    helpers.smu_settings()

elif action == 'youtube':
    from resources.lib.indexers import you_tube
    you_tube.yt_videos(url)

elif action == 'play':
    from resources.lib.modules.player import player
    player(url, name)

elif action == 'directory':
    from resources.lib.modules.player import directory_picker
    directory_picker(url, title, plot, genre)

elif action == 'live_switcher':
    from resources.lib.indexers import live
    live.Main().switcher()

elif action == 'vod_switcher':
    from resources.lib.indexers import gm
    gm.Main().vod_switcher(url)

elif action == 'papers_switcher':
    from resources.lib.indexers import news
    news.Main().switcher()

elif action == 'setup_iptv':
    from resources.lib.modules import tools
    tools.setup_iptv()

elif action == 'enable_iptv':
    from resources.lib.modules import tools
    tools.enable_iptv()

elif action == 'enable_proxy':
    from resources.lib.modules import tools
    tools.enable_proxy_module()

elif action == 'setup_previous_menu_key':
    from resources.lib.modules import tools
    tools.setup_previous_menu_key()

elif action == 'setup_mouse_keymap':
    from resources.lib.modules import tools
    tools.setup_mouse_keymap()

elif action == 'add_to_playlist':
    from resources.lib.modules import helpers
    helpers.add_to_playlist()

elif action == 'clear_playlist':
    from resources.lib.modules import helpers
    helpers.clear_playlist()

elif action == 'toggle_watched':
    from resources.lib.modules import helpers
    helpers.toggle_watched()

elif action == 'toggle_debug':
    from resources.lib.modules import helpers
    helpers.toggle_debug()

elif action == 'cache_clear':
    from resources.lib.modules import helpers
    helpers.cache_clear()

elif action == 'cache_delete':
    from resources.lib.modules import helpers
    helpers.cache.delete()

elif action == 'purge_bookmarks':
    from resources.lib.modules import helpers
    helpers.purge_bookmarks()

elif action == 'delete_settings':
    from resources.lib.modules import helpers
    helpers.delete_settings()

elif action == 'refresh':
    from resources.lib.modules import helpers
    helpers.refresh()

elif action == 'refresh_and_clear':
    from resources.lib.modules import helpers
    helpers.refresh_and_clear()

elif action == 'reset_idx':
    from resources.lib.modules import helpers
    helpers.reset_idx()

elif action == 'yt_setup':
    from resources.lib.modules import tools
    tools.yt_setup()

elif action == 'isa_enable':
    from resources.lib.modules import tools
    tools.isa_enable()

elif action == 'changelog':
    from resources.lib.modules import tools
    tools.changelog()

elif action == 'developer_mode':
    from resources.lib.modules import tools
    tools.dev()

elif action == 'info':
    from resources.lib.indexers import settings
    settings.Main().info()

elif action == 'force':
    from resources.lib.modules import helpers
    helpers.force()

elif action == 'dmca':
    from resources.lib.modules import helpers
    helpers.dmca()

elif action == 'system_info':
    from resources.lib.modules import helpers
    helpers.system_info()

# Reserved might use later:
# elif action == 'report':
#     from resources.lib.modules import tools
#     tools.mailer(text=title)

else:
    from resources.lib.modules import helpers
    helpers.greeting()
