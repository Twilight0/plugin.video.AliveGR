# -*- coding: utf-8 -*-

'''
    AliveGR Addon
    Author Twilight0

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/GPL-3.0-only for more information.
'''
from __future__ import absolute_import, unicode_literals

import re
from tulip import control, client, directory
from tulip.init import syshandle, sysaddon
from ..modules.themes import iconname
from ..modules.constants import YT_ADDON, cache_method, cache_duration
from .gm import GM_BASE

GK_BASE = 'https://gamatotv.info'


class Indexer:

    def __init__(self):

        self.list = []
        self.data = []

    def kids(self):

        self.list = [
            {
                'title': control.lang(30078),
                'action': 'kids_live',
                'icon': iconname('kids_live')
            }
            ,
            {
                'title': control.lang(30073),
                'action': 'listing',
                'url': ''.join([GM_BASE, 'movies.php?g=8&y=&l=&p=']),
                'icon': iconname('cartoon_movies')
            }
            ,
            {
                'title': control.lang(30092),
                'action': 'listing',
                'url': ''.join([GM_BASE, 'shortfilm.php?g=8&y=&l=&p=']),
                'icon': iconname('cartoon_short')
            }
            ,
            {
                'title': control.lang(30072),
                'action': 'cartoon_series',
                'icon': iconname('cartoon_series')
            }
            ,
            {
                'title': control.lang(30074),
                'action': 'cartoon_collection',
                'icon': iconname('cartoon_collection')
            }
            ,
            {
                'title': control.lang(30075),
                'action': 'educational',
                'icon': iconname('educational')
            }
            ,
            {
                'title': control.lang(30262),
                'action': 'activate_other_addon',
                'url': 'plugin://plugin.video.ert.gr/?action=categories&url=https%3A%2F%2Fwww.ertflix.gr%2Fshow%2Fchildren',
                'icon': iconname('cartoon_collection'),
                'isFolder': 'False', 'isPlayable': 'False'
            }
            ,
            {
                'title': control.lang(30076),
                'action': 'kids_songs',
                'icon': iconname('kids_songs')
            }
        ]

        directory.add(self.list)

    def cartoon_collection(self):

        self.data = [
            {
                'title': u'Classical Films - Κλασσικά Κινηματογραφημένα',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PLF0A5359586D57FE8/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/X9RxumkELfE/mqdefault.jpg'
            }
            ,
            {
                'title': u'Mythology - Μυθολογία',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL3E1C926284F12F32/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/kpd-Z_VK6Jc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Aesop\'s Fables - Αισώπου Μύθοι',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL4FF9F773D3596E60/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/Gkr-pV_gY48/mqdefault.jpg'
            }
            ,
            {
                'title': u'Greek Fairy Tales - Ελληνικά Παραμύθια',
                'url': '{0}/channel/UC9VmWb5Wd5sc4E4k1CevEug/'.format(YT_ADDON),
                'icon': 'https://yt3.ggpht.com/-n8KoGQ6U_zc/AAAAAAAAAAI/AAAAAAAAAAA/SoUWvy5-Tb8/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Fairy Tales & Songs - Παραμύθια και Τραγούδια',
                'url': '{0}/channel/UCClAFTnbGditvz9_7_7eumw/playlists/'.format(YT_ADDON),
                'icon': 'https://yt3.ggpht.com/-mBPhzUcDIHM/AAAAAAAAAAI/AAAAAAAAAAA/pNQi44zsLq8/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Collection Miscellaneous - Συλλογή Διάφορα',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL4075DA390F6E82B1/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/MPtZ_VHNg34/mqdefault.jpg'
            }
        ]

        for i in self.data:
            i['url'] = '?'.join([i['url'], 'addon_id={}'.format(control.addonInfo('id'))])

        additional = {
                'title': u'Various full length movies - Διάφορες ταινίες πλήρους μήκους',
                'url': '{0}?action={1}'.format(sysaddon, 'cartoon_various'),
                'icon': iconname('kids')
            }

        if control.setting('show_alt_vod') == 'true':
            self.data.insert(0, additional)

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

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    def educational(self):

        self.data = [
            {
                'title': u'Learn about animals - Μάθε για τα ζώα',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRboPyGr30sIRMnc20C77ui/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/_fDdVYJA9Vk/mqdefault.jpg'
            }
            ,
            {
                'title': u'Secondary school education - Εκπαίδευση Δημοτικού Σχολείου',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LQvxn7RyUySvQy6C6hTUTXf/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/isxjo7M2h74/mqdefault.jpg'
            }
            ,
            {
                'title': u'Sexual Education for children - Σεξουαλική Αγωγή για παιδιά',
                'url': '{0}/channel/UCsKQX1G7XQO2a5nD9nrse-Q/playlist/PL7Adbo89X3LRy-LRQEeRdT_kf5iFdofsu/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/l9gN1F6S3bc/mqdefault.jpg'
            }
            ,
            {
                'title': u'World\'s Seven Ancient Miracles - Τα Επτά Θαύματα του Αρχαίου Κόσμου',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeThKG7GK1k2DRgB5im-vPHc/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/5nEDQ_jYJIo/mqdefault.jpg'
            }
            ,
            {
                'title': u'The land of Knowledge - Η Χώρα των Γνώσεων',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeS-ZVlk0vgNdx5igsFvYN8s/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/K-Ba9l2uDDk/mqdefault.jpg'
            }
            ,
            {
                'title': u'Ancient Egypt - Αρχαία Αίγυπτος',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeTrRcdIHjtziNEkqPqalUOa/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/pV8EMy8gaXI/mqdefault.jpg'
            }
            ,
            {
                'title': u'Explorers & Seafarers - Εξερευνητές και Θαλασσοπόροι',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeQRBb7ayyynWgYEUbkQKPpJ/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/SPdnnVNZgwc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Mini Encyclopaedia - Μικρή Εγκυκλοπαίδεια',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeTLMi1bFqLC_cn5ZAtqSvlV/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/o31_SNQFYhc/mqdefault.jpg'
            }
            ,
            {
                'title': u'Miscellaneous Documentaties - Διάφορα Ντοκυμαντέρ',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRY94Yga82ZYsPJ9Xbe3OiZ/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/Vf_o_Q5ZQRg/mqdefault.jpg'
            }
            ,
            {
                'title': u'Learn Ancient Greek - Μάθετε Αρχαία Ελληνικά',
                'url': '{0}/channel/UC5quWsvOBNUaR-Duv3K-JFA/playlist/PLxqCshQO3A1HnlHwxda3wX_kzY-C0gpZq/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/st01jb_Xb7g/mqdefault.jpg'
            }
            ,
            {
                'title': u'Drawings - Ζωγραφιές',
                'url': '{0}/channel/UC5quWsvOBNUaR-Duv3K-JFA/playlist/PLxqCshQO3A1FmjzGXbfIjTSXcysLfPfKM/'.format(YT_ADDON),
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

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

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
                'url': '{0}/channel/UCUmGu9Ncu5NeaEjwpLXW0PQ/'.format(YT_ADDON),
                'icon': 'https://yt3.ggpht.com/-MVbyrB7DJrY/AAAAAAAAAAI/AAAAAAAAAAA/WjLUCzyX3zI/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Greek songs with lyrics No.2 - Ελληνικά παιδικά τραγούδια με στίχους No.2',
                'url': '{0}/channel/UCyENiZwRYzfXzbwP-Mxk9oA/'.format(YT_ADDON),
                'icon': 'https://yt3.ggpht.com/-Jdrq5I2r5Tc/AAAAAAAAAAI/AAAAAAAAAAA/z7IPqFS7jqA/s256-c-k-no-mo-rj-c0xffffff/photo.jpg'
            }
            ,
            {
                'title': u'Greek Karaoke - Ελληνικό Καραόκε',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRlD0w1GXbitRL6sbyMscVi/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/Iz5P8xJel-U/mqdefault.jpg'
            }
            ,
            {
                'title': u'Karaoke for English Learning - Μαθαίνω Αγγλικά με καραόκε',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeSL-M5Q0qG3Eszj0I1O98bT/'.format(YT_ADDON),
                'icon': 'https://i.ytimg.com/vi/L2atYpQ7Zbg/mqdefault.jpg'
            }
            ,
            {
                'title': u'Learning Music for Kids - Μαθαίνω Μουσική, για παιδιά',
                'url': '{0}/channel/UCp_0VMwvn5LeJMhtreBFIcA/playlist/PLP25S0MkvCeRr5VH-HylSX89MHXQ_KyS0/'.format(YT_ADDON),
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

        control.addItems(syshandle, self.list)
        control.directory(syshandle)

    @cache_method(cache_duration(180))
    def _cartoon_various(self, url):

        if url is None:
            url = '{0}/genre/gamato/'.format(GK_BASE)

        html = client.request(url)

        next_link = client.parseDOM(html, 'a', attrs={'class': 'arrow_pag'}, ret='href')[-1]

        html = client.parseDOM(html, 'div', attrs={'class': 'items'})[0]

        items = client.parseDOM(html, 'article', attrs={'id': r'post-\d+'})

        for item in items:

            h3 = client.parseDOM(item, 'h3')[0]
            title = client.parseDOM(h3, 'a')[0]
            title = client.replaceHTMLCodes(title)
            url = client.parseDOM(h3, 'a', ret='href')[0]

            meta = client.parseDOM(item, 'div', attrs={'class': 'metadata'})[0]

            try:

                span = client.parseDOM(meta, 'span')
                etos = [s for s in span if len(s) == 4][0]
                plot = client.parseDOM(item, 'div', attrs={'class': 'texto'})[0]
                duration = [s for s in span if s.endswith('min')][0]
                duration = int(re.search(r'(\d+)', duration).group(1)) * 60

            except IndexError:

                plot = u'Μεταγλωτισμένο'
                etos = '2020'
                duration = 3600

            year = ''.join(['(', etos, ')'])
            label = ' '.join([title, year])
            image = client.parseDOM(item, 'img', ret='src')[0]

            i = {
                'title': label, 'url': url, 'image': image, 'nextlabel': 30334, 'next': next_link,
                'plot': plot, 'duration': duration, 'year': int(etos), 'nexticon': iconname('next')
            }

            self.list.append(i)

        return self.list

    def cartoon_various(self, url):

        self.list = self._cartoon_various(url)

        for item in self.list:

            item.update({'action': 'play', 'isFolder': 'False', 'nextaction': 'cartoon_various'})

            refresh_cm = {'title': 30054, 'query': {'action': 'refresh'}}
            unwatched_cm = {'title': 30228, 'query': {'action': 'toggle_watched'}}
            item.update({'cm': [refresh_cm, unwatched_cm]})

        directory.add(self.list)
