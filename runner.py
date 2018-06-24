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

import xbmcgui


text = """This version is released as such to serve as a form of a protest for the Team Kodi's decision over my ban from their forum and the rejection of submission for my LEGIT addons into the official repo.
All my addons are LEGIT including AliveGR, they do not contain anything malicious whatsoever, I have always respected Team Kodi, content creators and especially users themselves. One mistake I did roughly three months ago was definitely not enough for this ruthless ban over my alias.
I apologised about it: http://bit.ly/reddit_apology
[B]Actually I did nothing wrong![/B]
I was feeling depressed for a while and didn't want to code anything, but I recovered and thought about continuing and today's rejection of a PR has definitely made me very angry: https://github.com/xbmc/repo-plugins/pull/1912
If you think my ban was unfair please go to kodi forums and complain, request reconsideration or whatever.
Next version will be released after a week or so. Live channels will be brought down until then."""

if __name__ == '__main__':

    xbmcgui.Dialog().textviewer(heading='Thank you for using AliveGR', text=text)
