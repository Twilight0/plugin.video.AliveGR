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


from tulip import control


def theme():

    theme = control.setting('theme')
    toggle = control.setting('dark_theme')

    if theme == '0':
        return 'alivegr', '+alivegr.png'
    elif theme == '1':
        return 'twilight', '+twilight.png'
    elif theme == '2' and toggle == 'true':
        return 'dr.azziw_dark', '+dr.azziw_dark.png'
    else:
        return 'dr.azziw_inverted', '+dr.azziw_inverted.png'


def iconname(name):
    return control.addonmedia(addonid='script.AliveGR.artwork', theme=theme()[0], icon=name + theme()[1])
