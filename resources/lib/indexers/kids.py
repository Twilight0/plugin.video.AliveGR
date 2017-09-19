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


from tulip import control, cache, directory
from ..modules.themes import iconname
from ..modules import sysaddon, syshandle
import json

class Main:

    def __init__(self):

        self.list = []; self.data = []

    def kids(self):

        self.data = [
            {
                'title': control.lang(30078),
                'url': 'plugin://plugin.video.AliveGR/?action=kids_live',
                'icon': iconname('kids_live')
            }
            ,
            {
                'title': control.lang(30073),
                'url': 'plugin://plugin.video.AliveGR/?action=listing&url=http://greek-movies.com/movies.php?g=8&y=&l=&p=',
                'icon': iconname('cartoon_movies')
            }
            ,
            {
                'title': control.lang(30092),
                'url': 'plugin://plugin.video.AliveGR/?action=listing&url=http://greek-movies.com/shortfilm.php?g=8&y=&l=&p=',
                'icon': iconname('cartoon_short')
            }
            ,
            {
                'title': control.lang(30072),
                'url': '{0}?action={1}'.format(sysaddon, 'cartoon_series'),
                'icon': iconname('cartoon_series')
            }
            ,
            {
                'title': control.lang(30074),
                'url': '{0}?action={1}'.format(sysaddon, 'cartoon_collection'),
                'icon': iconname('cartoon_collection')
            }
            ,
            {
                'title': control.lang(30075),
                'url': '{0}?action={1}'.format(sysaddon, 'educational'),
                'icon': iconname('educational')
            }
            ,
            {
                'title': control.lang(30076),
                'url': '{0}?action={1}'.format(sysaddon, 'kids_songs'),
                'icon': iconname('kids_songs')
            }
        ]

        for item in self.data:
            li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            self.list.append((item['url'], li, True))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def cartoon_collection(self):

        self.data = [
            {
                'title': 'Collection Miscellaneous 1 - Συλλογή Διάφορα 1'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL4075DA390F6E82B1/',
                'icon': 'https://i.ytimg.com/vi/MPtZ_VHNg34/mqdefault.jpg'
            }
            ,
            {
                'title': 'Collection Miscellaneous 2 - Συλλογή Διάφορα 2'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCzU4decItAYA0omjxNiIHbg/playlists/',
                'icon': 'https://yt3.ggpht.com/-W3Asi5ry2Rs/AAAAAAAAAAI/AAAAAAAAAAA/QzJaKZpLEtw/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': 'Classical Films - Κλασσικά Κινηματογραφημένα'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PLF0A5359586D57FE8/',
                'icon': 'https://i.ytimg.com/vi/X9RxumkELfE/mqdefault.jpg'
            }
            ,
            {
                'title': 'Mythology - Μυθολογία'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL3E1C926284F12F32/',
                'icon': 'https://i.ytimg.com/vi/kpd-Z_VK6Jc/mqdefault.jpg'
            }
            ,
            {
                'title': 'Aesop\'s Fables - Αισώπου Μύθοι'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL4FF9F773D3596E60/',
                'icon': 'https://i.ytimg.com/vi/Gkr-pV_gY48/mqdefault.jpg'
            }
            ,
            {
                'title': 'Fairy Tales & Songs - Παραμύθια και Τραγούδια'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCClAFTnbGditvz9_7_7eumw/playlists/',
                'icon': 'https://yt3.ggpht.com/-mBPhzUcDIHM/AAAAAAAAAAI/AAAAAAAAAAA/pNQi44zsLq8/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
        ]

        for item in self.data:
            if control.setting('splitter') == 'true':
                if control.setting('lang_split') == '0':
                    li = control.item(label=item['title'].partition('-')[0].strip())
                elif control.setting('lang_split') == '1':
                    li = control.item(label=item['title'].partition('-')[2].strip())
            else:
                li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            self.list.append((item['url'], li, item['isFolder']))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def educational(self):

        self.data = [
            {
                'title': 'Learn about animals - Μάθε για τα ζώα'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRboPyGr30sIRMnc20C77ui/',
                'icon': 'https://i.ytimg.com/vi/_fDdVYJA9Vk/mqdefault.jpg'
            }
            ,
            {
                'title': 'Secondary school education - Εκπαίδευση Δημοτικού Σχολείου'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LQvxn7RyUySvQy6C6hTUTXf/',
                'icon': 'https://i.ytimg.com/vi/isxjo7M2h74/mqdefault.jpg'
            }
            ,
            {
                'title': 'Sexual Education for children - Σεξουαλική Αγωγή για παιδιά'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRy-LRQEeRdT_kf5iFdofsu/',
                'icon': 'https://i.ytimg.com/vi/l9gN1F6S3bc/mqdefault.jpg'
            }
            ,
            {
                'title': 'World\'s Seven Ancient Miracles - Τα Επτά Θαύματα του Αρχαίου Κόσμου'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeThKG7GK1k2DRgB5im-vPHc/',
                'icon': 'https://i.ytimg.com/vi/5nEDQ_jYJIo/mqdefault.jpg'
            }
            ,
            {
                'title': 'The land of Knowledge - Η Χώρα των Γνώσεων'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeS-ZVlk0vgNdx5igsFvYN8s/',
                'icon': 'https://i.ytimg.com/vi/K-Ba9l2uDDk/mqdefault.jpg'
            }
            ,
            {
                'title': 'Ancient Egypt - Αρχαία Αίγυπτος'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeTrRcdIHjtziNEkqPqalUOa/',
                'icon': 'https://i.ytimg.com/vi/pV8EMy8gaXI/mqdefault.jpg'
            }
            ,
            {
                'title': 'Explorers & Seafarers - Εξερευνητές και Θαλασσοπόροι'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeQRBb7ayyynWgYEUbkQKPpJ/',
                'icon': 'https://i.ytimg.com/vi/SPdnnVNZgwc/mqdefault.jpg'
            }
            ,
            {
                'title': 'Mini Encyclopaedia - Μικρή Εγκυκλοπαίδεια'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeTLMi1bFqLC_cn5ZAtqSvlV/',
                'icon': 'https://i.ytimg.com/vi/o31_SNQFYhc/mqdefault.jpg'
            }
            ,
            {
                'title': 'Miscellaneous Documentaties - Διάφορα Ντοκυμαντέρ'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRY94Yga82ZYsPJ9Xbe3OiZ/',
                'icon': 'https://i.ytimg.com/vi/Vf_o_Q5ZQRg/mqdefault.jpg'
            }
            ,
            {
                'title': 'Learn Ancient Greek - Μάθετε Αρχαία Ελληνικά'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UC5quWsvOBNUaR-Duv3K-JFA/playlist/PLxqCshQO3A1HnlHwxda3wX_kzY-C0gpZq/',
                'icon': 'https://i.ytimg.com/vi/st01jb_Xb7g/mqdefault.jpg'
            }
            ,
            {
                'title': 'Drawings - Ζωγραφιές'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UC5quWsvOBNUaR-Duv3K-JFA/playlist/PLxqCshQO3A1FmjzGXbfIjTSXcysLfPfKM/',
                'icon': 'https://i.ytimg.com/vi/GdiLSXePno8/mqdefault.jpg'
            }
        ]

        for item in self.data:
            if control.setting('splitter') == 'true':
                if control.setting('lang_split') == '0':
                    li = control.item(label=item['title'].partition('-')[0].strip())
                elif control.setting('lang_split') == '1':
                    li = control.item(label=item['title'].partition('-')[2].strip())
            else:
                li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            self.list.append((item['url'], li, item['isFolder']))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def kids_songs(self):

        self.data = [
            {
                'title': 'Zouzounia TV kids songs - Παιδικά Τραγούδια από τα Ζουζούνια'.decode('utf-8'),
                'url': 'plugin://plugin.video.zouzounia.tv/',
                'icon': 'https://yt3.ggpht.com/-zhH35bOsqec/AAAAAAAAAAI/AAAAAAAAAAA/LxUO6o-ZHPc/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': 'Greek songs with lyrics No.1 - Ελληνικά παιδικά τραγούδια με στίχους No.1'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCUmGu9Ncu5NeaEjwpLXW0PQ/',
                'icon': 'https://yt3.ggpht.com/-MVbyrB7DJrY/AAAAAAAAAAI/AAAAAAAAAAA/WjLUCzyX3zI/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': 'Greek songs with lyrics No.2 - Ελληνικά παιδικά τραγούδια με στίχους No.2'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCyENiZwRYzfXzbwP-Mxk9oA/',
                'icon': 'https://yt3.ggpht.com/-Jdrq5I2r5Tc/AAAAAAAAAAI/AAAAAAAAAAA/z7IPqFS7jqA/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': 'Christmas songs - Χριστουγεννιάτικα Τραγούδια'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LQJIp9hY-4ESH6P1PVW34uB/',
                'icon': 'https://i.ytimg.com/vi/WhQy0aZ22Tc/mqdefault.jpg'
            }
            ,
            {
                'title': 'The party\'s songs - Τα τραγούδια της παρέας'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRsQ-umYdnXPrTzclN0vsPh/',
                'icon': 'https://i.ytimg.com/vi/V1pdBZaF3cc/mqdefault.jpg'
            }
            ,
            {
                'title': 'Greek Karaoke - Ελληνικό Καραόκε'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRlD0w1GXbitRL6sbyMscVi/',
                'icon': 'https://i.ytimg.com/vi/Iz5P8xJel-U/mqdefault.jpg'
            }
            ,
            {
                'title': 'Karaoke for English Learning - Μαθαίνω Αγγλικά με καραόκε'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeSL-M5Q0qG3Eszj0I1O98bT/',
                'icon': 'https://i.ytimg.com/vi/L2atYpQ7Zbg/mqdefault.jpg'
            }
            ,
            {
                'title': 'Learning Music for Kids - Μαθαίνω Μουσική, για παιδιά'.decode('utf-8'),
                'url': 'plugin://plugin.video.youtube/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRr5VH-HylSX89MHXQ_KyS0/',
                'icon': 'https://i.ytimg.com/vi/w5tF5J_BNfI/mqdefault.jpg'
            }
        ]

        for item in self.data:
            if control.setting('splitter') == 'true':
                if control.setting('lang_split') == '0':
                    li = control.item(label=item['title'].partition('-')[0].strip())
                elif control.setting('lang_split') == '1':
                    li = control.item(label=item['title'].partition('-')[2].strip())
            else:
                li = control.item(label=item['title'])
            li.setArt({'icon': item['icon'], 'fanart': control.addonInfo('fanart')})
            self.list.append((item['url'], li, item['isFolder']))

        control.addItems(syshandle, self.list)
        control.directory(syshandle)