# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import requests
import bs4
from .corporaservice import CorporaService

class MMCorporaService(CorporaService):

    """Docstring for MMCorporaService. """

    method = 'api'
    api_url = 'http://api.mymemory.translated.net/get'
    web_url = 'http://mymemory.translated.net/s.php'

    def update_config(self, conf):
        """TODO: Docstring for update_config.

        :conf: TODO
        :returns: TODO

        """
        self.method = conf.get('method', MMCorporaService.method)

    def _get_api_corpora(self, phrase, proxy=None):
        """TODO: Docstring for _get_api_corpora.

        :phrase: TODO
        :proxy: TODO
        :returns: TODO

        """
        params = dict(
            q=phrase,
            langpair='|'.join(self.lang_pair)
        )
        try:
            data = requests.get(self.api_url, params=params, proxies=proxy).json()
        except:
            pass
        else:
            try:
                for pair in data['matches']:
                    yield pair['segment'], pair['translation']
            except:
                pass

    def _get_web_corpora(self, phrase, proxy=None):
        """TODO: Docstring for _get_web_corpora.

        :phrase: TODO
        :proxy: TODO
        :returns: TODO

        """
        def first_non_empty(tags):
            for tag in tags:
                text = ' '.join(tag.stripped_strings)
                if text:
                    return text
            return ''

        params = dict(
            q=phrase,
            sl=self.lang_pair.l1,
            tl=self.lang_pair.l2
        )
        try:
            content = requests.get(self.web_url, params=params, proxies=proxy).content
            soup = bs4.BeautifulSoup(content)
        except:
            pass
        else:
            for table in soup.find_all('table'):
                try:
                    src = first_non_empty(table.find('tr').find_all('td')[0].find_all('span'))
                    tgt = first_non_empty(table.find('tr').find_all('td')[1].find_all('span'))
                except (AttributeError, IndexError):
                    continue
                else:
                    if src and tgt:
                        yield src, tgt

    def get_corpora(self, phrase, proxy=None):
        """TODO: Docstring for get_corpora.

        :phrase: TODO
        :proxy: TODO
        :returns: TODO

        """
        if self.method == 'api':
            for pair in self._get_api_corpora(phrase, proxy):
                yield pair
        elif self.method == 'web':
            for pair in self._get_web_corpora(phrase, proxy):
                yield pair
