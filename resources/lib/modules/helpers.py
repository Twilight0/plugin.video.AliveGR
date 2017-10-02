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


from tulip import control, cache

leved = 'Q2dw5CchN3c39mck9ydhJ3L0VmbuI3ZlZXasF2LvoDc0RHa'


def pvr_client(tvguide='false'):

    if control.condVisibility('Pvr.HasTVChannels'):

        if tvguide is None or tvguide == 'false':

            selection = control.selectDialog([control.lang(30001), control.lang(30014)])

            if selection == 0:
                control.execute('ActivateWindow(TVChannels)')
            elif selection == 1:
                control.execute('ActivateWindow(TVGuide)')
            else:
                control.execute('Dialog.Close(all)')

        elif tvguide == 'true':

            control.execute('ActivateWindow(TVGuide)')

    else:

        control.infoDialog(message=control.lang(30065))


def stream_picker(qualities, urls):

    choice = control.selectDialog(heading=control.lang(30167).partition(' (')[0], list=qualities)

    if choice <= len(qualities) and not choice == -1:
        popped = urls.pop(choice)
        return popped
    else:
        return 30403


def smu_settings(sleep=True):

    if sleep:
        control.execute('Dialog.Close(all)')
        control.sleep(50)
        control.Settings('script.module.urlresolver')
    else:
        control.Settings('script.module.urlresolver')


def reset_idx():

    control.setSetting('live_group', 'ALL')
    control.setSetting('vod_group', '30213')
    control.infoDialog(message=control.lang(30402), time=3000)


def add_to_playlist():

    control.execute('Action(Queue)')


def clear_playlist():

    control.execute('Playlist.Clear')


def toggle_watched():

    control.execute('Action(ToggleWatched)')


def cache_clear():

    cache.clear(withyes=False)


def cache_delete():

    cache.delete(withyes=False)


def purge_bookmarks():

    if control.exists(control.bookmarksFile):
        if control.yesnoDialog(line1=control.lang(30214)):
            control.deleteFile(control.bookmarksFile)
            control.infoDialog(control.lang(30402))
        else:
            control.infoDialog(control.lang(30403))
    else:
        control.infoDialog(control.lang(30139))


def delete_settings():

    if control.exists(control.dataPath):
        from shutil import rmtree
        rmtree(control.dataPath, ignore_errors=True)
        control.infoDialog(control.lang(30402).encode('utf-8'))
    else:
        control.infoDialog(control.lang(30140))


def refresh():

    control.refresh()


def refresh_and_clear():

    cache_clear()
    control.sleep(50)
    refresh()


def thgiliwt(s):

    from base64 import b64decode

    string = s[::-1]

    return b64decode(string)
