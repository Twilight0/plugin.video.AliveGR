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

from tulip import control
from resources.lib.modules.themes import iconname
from resources.lib.modules.constants import yt_addon, sdik

try:
    if control.condVisibility('System.HasAddon({0})'.format(sdik)):
        import sys
        sys.path.extend([control.join(control.addon(id=sdik).getAddonInfo('path'), 'resources', 'lib')])
        import extension
except Exception:
    pass


class Indexer:

    def __init__(self, argv):

        self.list = []; self.data = []
        self.argv = argv
        self.sysaddon = self.argv[0]
        self.syshandle = int(self.argv[1])

    def kids(self):

        self.data = [
            {
                'title': control.lang(30078),
                'url': 'plugin://plugin.video.AliveGR/?action=kids_live',
                'icon': iconname('kids_live')
            }
            ,
            {
                'title': control.lang(30074),
                'url': '{0}?action={1}'.format(self.sysaddon, 'cartoon_collection'),
                'icon': iconname('cartoon_collection')
            }
            ,
            {
                'title': control.lang(30075),
                'url': '{0}?action={1}'.format(self.sysaddon, 'educational'),
                'icon': iconname('educational')
            }
            ,
            {
                'title': control.lang(30076),
                'url': '{0}?action={1}'.format(self.sysaddon, 'kids_songs'),
                'icon': iconname('kids_songs')
            }
        ]

        try:
            if control.condVisibility('System.HasAddon({0})'.format(sdik)):
                extended = [
                    dict(
                        (k, control.lang(v) if (k == 'title') else v) for k, v in item.items()
                    ) for item in extension.kids_indexer
                ]
                extended = [
                    dict((k, iconname(v) if (k == 'icon') else v) for k, v in item.items()) for item in extended
                ]
                self.data = [self.data[0]] + extended + self.data[1:]
        except:
            pass

        for item in self.data:
            li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            self.list.append((item['url'], li, True))

        control.addItems(self.syshandle, self.list)
        control.directory(self.syshandle)

    def cartoon_collection(self):

        self.data = [
            {
                'title': u'Classical Films - Κλασσικά Κινηματογραφημένα',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PLF0A5359586D57FE8/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/X9RxumkELfE/mqdefault.jpg'
            }
            ,
            {
                'title': u'Mythology - Μυθολογία',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL3E1C926284F12F32/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/kpd-Z_VK6Jc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Aesop\'s Fables - Αισώπου Μύθοι',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL4FF9F773D3596E60/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/Gkr-pV_gY48/mqdefault.jpg'
            }
            ,
            {
                'title': u'Greek Fairy Tales - Ελληνικά Παραμύθια',
                'url': '{0}/channel/UC9VmWb5Wd5sc4E4k1CevEug/'.format(yt_addon),
                'icon': 'https://yt3.ggpht.com/-n8KoGQ6U_zc/AAAAAAAAAAI/AAAAAAAAAAA/SoUWvy5-Tb8/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Fairy Tales & Songs - Παραμύθια και Τραγούδια',
                'url': '{0}/channel/UCClAFTnbGditvz9_7_7eumw/playlists/'.format(yt_addon),
                'icon': 'https://yt3.ggpht.com/-mBPhzUcDIHM/AAAAAAAAAAI/AAAAAAAAAAA/pNQi44zsLq8/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Collection Miscellaneous - Συλλογή Διάφορα',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL4075DA390F6E82B1/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/MPtZ_VHNg34/mqdefault.jpg'
            }
        ]

        for item in self.data:
            if control.setting('lang_split') == '0':
                if 'Greek' in control.infoLabel('System.Language'):
                    li = control.item(label=item['title'].partition(' - ')[2])
                elif 'English' in control.infoLabel('System.Language'):
                    li = control.item(label=item['title'].partition(' - ')[0])
                else:
                    li = control.item(label=item['title'])
            elif control.setting('lang_split') == '1':
                li = control.item(label=item['title'].partition(' - ')[0])
            elif control.setting('lang_split') == '2':
                li = control.item(label=item['title'].partition(' - ')[2])
            else:
                li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            self.list.append((item['url'], li, True))

        control.addItems(self.syshandle, self.list)
        control.directory(self.syshandle)

    def educational(self):

        self.data = [
            {
                'title': u'Learn about animals - Μάθε για τα ζώα',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRboPyGr30sIRMnc20C77ui/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/_fDdVYJA9Vk/mqdefault.jpg'
            }
            ,
            {
                'title': u'Secondary school education - Εκπαίδευση Δημοτικού Σχολείου',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LQvxn7RyUySvQy6C6hTUTXf/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/isxjo7M2h74/mqdefault.jpg'
            }
            ,
            {
                'title': u'Sexual Education for children - Σεξουαλική Αγωγή για παιδιά',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRy-LRQEeRdT_kf5iFdofsu/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/l9gN1F6S3bc/mqdefault.jpg'
            }
            ,
            {
                'title': u'World\'s Seven Ancient Miracles - Τα Επτά Θαύματα του Αρχαίου Κόσμου',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeThKG7GK1k2DRgB5im-vPHc/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/5nEDQ_jYJIo/mqdefault.jpg'
            }
            ,
            {
                'title': u'The land of Knowledge - Η Χώρα των Γνώσεων',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeS-ZVlk0vgNdx5igsFvYN8s/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/K-Ba9l2uDDk/mqdefault.jpg'
            }
            ,
            {
                'title': u'Ancient Egypt - Αρχαία Αίγυπτος',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeTrRcdIHjtziNEkqPqalUOa/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/pV8EMy8gaXI/mqdefault.jpg'
            }
            ,
            {
                'title': u'Explorers & Seafarers - Εξερευνητές και Θαλασσοπόροι',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeQRBb7ayyynWgYEUbkQKPpJ/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/SPdnnVNZgwc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Mini Encyclopaedia - Μικρή Εγκυκλοπαίδεια',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeTLMi1bFqLC_cn5ZAtqSvlV/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/o31_SNQFYhc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Miscellaneous Documentaties - Διάφορα Ντοκυμαντέρ',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRY94Yga82ZYsPJ9Xbe3OiZ/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/Vf_o_Q5ZQRg/mqdefault.jpg'
            }
            ,
            {
                'title': u'Learn Ancient Greek - Μάθετε Αρχαία Ελληνικά',
                'url': '{0}/channel/UC5quWsvOBNUaR-Duv3K-JFA/playlist/PLxqCshQO3A1HnlHwxda3wX_kzY-C0gpZq/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/st01jb_Xb7g/mqdefault.jpg'
            }
            ,
            {
                'title': u'Drawings - Ζωγραφιές',
                'url': '{0}/channel/UC5quWsvOBNUaR-Duv3K-JFA/playlist/PLxqCshQO3A1FmjzGXbfIjTSXcysLfPfKM/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/GdiLSXePno8/mqdefault.jpg'
            }
        ]

        for item in self.data:
            if control.setting('lang_split') == '0':
                if 'Greek' in control.infoLabel('System.Language'):
                    li = control.item(label=item['title'].partition(' - ')[2])
                elif 'English' in control.infoLabel('System.Language'):
                    li = control.item(label=item['title'].partition(' - ')[0])
                else:
                    li = control.item(label=item['title'])
            elif control.setting('lang_split') == '1':
                li = control.item(label=item['title'].partition(' - ')[0])
            elif control.setting('lang_split') == '2':
                li = control.item(label=item['title'].partition(' - ')[2])
            else:
                li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            self.list.append((item['url'], li, True))

        control.addItems(self.syshandle, self.list)
        control.directory(self.syshandle)

    def kids_songs(self):

        self.data = [
            {
                'title': u'Zouzounia TV kids songs - Παιδικά Τραγούδια από τα Ζουζούνια',
                'url': 'plugin://plugin.video.zouzounia.tv/',
                'icon': 'https://yt3.ggpht.com/-zhH35bOsqec/AAAAAAAAAAI/AAAAAAAAAAA/LxUO6o-ZHPc/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Greek songs with lyrics No.1 - Ελληνικά παιδικά τραγούδια με στίχους No.1',
                'url': '{0}/channel/UCUmGu9Ncu5NeaEjwpLXW0PQ/'.format(yt_addon),
                'icon': 'https://yt3.ggpht.com/-MVbyrB7DJrY/AAAAAAAAAAI/AAAAAAAAAAA/WjLUCzyX3zI/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Greek songs with lyrics No.2 - Ελληνικά παιδικά τραγούδια με στίχους No.2',
                'url': '{0}/channel/UCyENiZwRYzfXzbwP-Mxk9oA/'.format(yt_addon),
                'icon': 'https://yt3.ggpht.com/-Jdrq5I2r5Tc/AAAAAAAAAAI/AAAAAAAAAAA/z7IPqFS7jqA/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Greek Karaoke - Ελληνικό Καραόκε',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRlD0w1GXbitRL6sbyMscVi/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/Iz5P8xJel-U/mqdefault.jpg'
            }
            ,
            {
                'title': u'Karaoke for English Learning - Μαθαίνω Αγγλικά με καραόκε',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeSL-M5Q0qG3Eszj0I1O98bT/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/L2atYpQ7Zbg/mqdefault.jpg'
            }
            ,
            {
                'title': u'Learning Music for Kids - Μαθαίνω Μουσική, για παιδιά',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRr5VH-HylSX89MHXQ_KyS0/'.format(yt_addon),
                'icon': 'https://i.ytimg.com/vi/w5tF5J_BNfI/mqdefault.jpg'
            }
        ]

        for item in self.data:
            if control.setting('lang_split') == '0':
                if 'Greek' in control.infoLabel('System.Language'):
                    li = control.item(label=item['title'].partition(' - ')[2])
                elif 'English' in control.infoLabel('System.Language'):
                    li = control.item(label=item['title'].partition(' - ')[0])
                else:
                    li = control.item(label=item['title'])
            elif control.setting('lang_split') == '1':
                li = control.item(label=item['title'].partition(' - ')[0])
            elif control.setting('lang_split') == '2':
                li = control.item(label=item['title'].partition(' - ')[2])
            else:
                li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            self.list.append((item['url'], li, True))

        control.addItems(self.syshandle, self.list)
        control.directory(self.syshandle)
