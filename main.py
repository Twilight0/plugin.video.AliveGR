# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''

from sys import argv
# noinspection PyUnresolvedReferences
from resources.lib.modules import utils, kodi, player
# noinspection PyUnresolvedReferences
from resources.lib.indexers import (
    navigator, settings, news, live, networks, gm, kids, sports, miscellany, radios, music, bookmarks, search
)
from tulip.compat import parse_qsl
from tulip.directory import run_builtin
from tulip import control, bookmarks as bm

params = dict(parse_qsl(argv[2][1:]))

content = params.get('content_type')
action = params.get('action')
url = params.get('url')
image = params.get('image')
title = params.get('title')
name = params.get('name')
query = params.get('query')

# Entry:

if content == 'video':

    navigator.Indexer().root()

elif content == 'audio':

    navigator.Indexer().audio()

elif content == 'image':

    news.Indexer().papers_index()

elif content == 'executable':

    settings.Indexer().menu()

elif action is None:

    navigator.Indexer().root()

elif action == 'root':

    run_builtin(content_type='video')

elif action == 'generic_index':

    navigator.Indexer().generic(query)

elif action == 'live_tv':

    live.Indexer().live_tv()

elif action == 'pvr_client':

    kodi.pvr_client(query)

elif action == 'networks':

    networks.Indexer().networks()

elif action == 'news':

    news.Indexer().news()

elif action == 'movies':

    gm.Indexer().movies()

elif action == 'short_films':

    gm.Indexer().short_films()

elif action == 'shows':

    gm.Indexer().shows()

elif action == 'series':

    gm.Indexer().series()

elif action == 'kids':

    kids.Indexer().kids()

elif action == 'kids_live':

    live.Indexer().modular('30032')

elif action == 'cartoon_series':

    gm.Indexer().cartoons_series()

elif action == 'cartoon_collection':

    kids.Indexer().cartoon_collection()

elif action == 'cartoon_various':

    kids.Indexer().cartoon_various(url)

elif action == 'educational':

    kids.Indexer().educational()

elif action == 'kids_songs':

    kids.Indexer().kids_songs()

elif action == 'listing':

    gm.Indexer().listing(url)

elif action == 'episodes':

    gm.Indexer().episodes(url)

elif action == 'sports':

    sports.Indexer().sports()

elif action == 'gm_sports':

    gm.Indexer().gm_sports()

elif action == 'sports_news':

    sports.Indexer().sports_news()

elif action == 'events':

    gm.Indexer().events(url)

elif action == 'theater':

    gm.Indexer().theater()

elif action == 'miscellany':

    miscellany.Indexer().miscellany()

elif action == 'audio':

    navigator.Indexer().audio()

elif action == 'music':

    music.Indexer().menu()

elif action == 'music_live':

    live.Indexer().modular('30125')

elif action == 'gm_music':

    music.Indexer().gm_music()

elif action == 'artist_index':

    music.Indexer().artist_index(url)

elif action == 'album_index':

    music.Indexer().album_index(url)

elif action == 'songs_index':

    music.Indexer().songs_index(url, name)

elif action == 'mgreekz_index':

    music.Indexer().mgreekz_index()

elif action == 'top50_list':

    music.Indexer().top50_list(url)

elif action == 'techno_choices':

    music.Indexer().techno_choices(url)

elif action == 'radio':

    radios.Indexer().radio()

elif action == 'papers':

    utils.papers()

elif action == 'papers_index':

    news.Indexer().papers_index()

elif action == 'addBookmark':

    bm.add(url)

elif action == 'deleteBookmark':

    bm.delete(url)

elif action == 'pin':

    utils.pin()

elif action == 'unpin':

    utils.unpin()

elif action == 'bookmarks':

    bookmarks.Indexer().bookmarks()

elif action == 'clear_bookmarks':
    bm.clear('bookmark', withyes=True, label_yes_no=30311, file_=control.bookmarksFile, notify=False)
    control.sleep(200)
    control.refresh()

elif action in ['search', 'add_to_history']:

    search.Indexer().search(action, query)

elif action == 'delete_from_history':

    utils.delete_from_history(query)

elif action == 'search_index':

    search.Indexer().search_index()

elif action == 'search_index':

    search.Indexer().search_index()

elif action == 'settings':

    settings.Indexer().menu()

elif action == 'tools_menu':

    utils.tools_menu()

elif action == 'openSettings':

    control.openSettings(query)

elif action == 'other_addon_settings':

    utils.other_addon_settings(query)

elif action in ['play', 'play_resolved', 'play_skipped']:

    player.player(url, params)

elif action == 'directory':

    player.directory_picker(url, argv=argv)

elif action == 'live_switcher':

    live.Indexer().switcher()

elif action == 'vod_switcher':

    gm.Indexer().vod_switcher(url)

elif action == 'papers_switcher':

    news.Indexer().switcher()

elif action == 'page_selector':

    utils.page_selector(query)

elif action == 'setup_iptv':

    utils.setup_iptv()

elif action == 'enable_iptv':

    utils.enable_iptv()

elif action == 'enable_proxy':

    utils.enable_proxy_module()

elif action == 'setup_various_keymaps':

    utils.setup_various_keymaps(query)

elif action == 'add_to_playlist':

    kodi.add_to_playlist()

elif action == 'clear_playlist':

    kodi.clear_playlist()

elif action == 'toggle_watched':

    kodi.toggle_watched()

elif action == 'toggle_debug':

    kodi.toggle_debug()

elif action == 'skin_debug':

    kodi.skin_debug()

elif action == 'reload_skin':

    kodi.reload_skin()

elif action == 'skin_choice':

    kodi.skin_choice()

elif action == 'cache_clear':

    utils.cache_clear()

elif action == 'purge_bookmarks':

    utils.purge_bookmarks()

elif action == 'delete_settings_xml':

    utils.delete_settings_xml()

elif action == 'refresh':

    control.refresh()

elif action == 'refresh_and_clear':

    utils.refresh_and_clear()

elif action == 'reset_idx':

    utils.reset_idx(force=query == 'force')

elif action == 'yt_setup':

    utils.yt_setup()

elif action == 'isa_enable':

    kodi.isa_enable()

elif action == 'isa_setup':

    utils.isa_setup()

elif action == 'rtmp_enable':

    kodi.rtmp_enable()

elif action == 'changelog':

    utils.changelog()

elif action == 'developer_mode':

    utils.dev()

elif action == 'info':

    settings.Indexer().info()

elif action == 'input_stream_addons':

    settings.Indexer().input_stream_addons()

elif action == 'call_info':

    utils.call_info()

elif action == 'open_link':

    control.open_web_browser(url)

elif action == 'force':

    kodi.force()

elif action == 'dmca':

    utils.dmca()

elif action == 'pp':

    utils.pp()

elif action == 'system_info':

    kodi.system_info()

elif action == 'lang_choice':

    kodi.lang_choice()

elif action == 'toggle_alt':

    utils.toggle_alt()

elif action == 'quit':

    control.quit_kodi()

elif action == 'global_settings':

    kodi.global_settings()

elif action == 'pvrsettings':

    kodi.pvrsettings()

elif action == 'activate_other_addon':

    utils.activate_other_addon(url, query=query)

elif action == 'welcome':

    utils.welcome()

elif action == 'kodi_log_upload':

    kodi.log_upload()

elif action == 'apply_new_settings':

    utils.apply_new_settings()


# Always run:
if __name__ == '__main__':

    utils.checkpoint()
