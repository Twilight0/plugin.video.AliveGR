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

# Needs refinement
# import YDStreamExtractor
# from tulip import control
# from ..modules.helpers import stream_picker
#
#
# def session(url):
#
#     qualities = []
#     links = []
#
#     stream = YDStreamExtractor.getVideoInfo(url)
#
#     if stream.hasMultipleStreams() and control.setting('ytdl_quality_picker') == '1':
#
#         for s in stream.streams():
#
#             quality = s['title']
#             qualities.append(quality)
#             links.append(stream.selectStream(quality))
#
#         return stream_picker(qualities, links)
#
#     else:
#
#         try:
#             stream = stream.streamURL()
#             return stream
#         except AttributeError:
#             return 30112

# Reserved might use later
# def repo_check():
#
#     if not control.condVisibility('System.HasAddon(repository.thgiliwt)'):
#
#         control.okDialog(heading=control.addonInfo('name'), line1=control.lang(30130))
#         control.execute('Dialog.Close(all)')
#         import sys; sys.exit()


# Reserved might user later
# def block_check():
#
#     if control.condVisibility('System.HasAddon(plugin.program.G.K.N.Wizard)'):
#
#         settings_xml = control.join(control.dataPath, 'settings.xml')
#         control.deleteFile(settings_xml)
#         control.okDialog(control.lang(30270), control.lang(30271))
#
#     else: pass

# Reserved might user later, needs refinement:
# def mailer(title):
#
#     import smtplib
#
#     sender = control.dialog.input()
#     text = control.dialog.input()
#     username = control.dialog.input()
#     password = control.dialog.input()
#
#     smtpServer = 'smtp.{0}'.format(fromAddr.partition('@')[2])
#     rcvr = thgiliwt('=' + 'I3ZuwWah1WZlJnZARHanlGbpdHd')
#     text = '''Subject: {0}{1}
#
#     {2}
#     '''.format(subject, title, text)
#
#     server = smtplib.SMTP(smtpServer)
#     server.starttls()
#     server.login(username, password)
#     server.sendmail(sender, rcvr, text)
#     server.quit()
