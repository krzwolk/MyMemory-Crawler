# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

class CorporaService(object):

    """Docstring for CorporaService. """

    def __init__(self, lang_pair):
        """TODO: to be defined1.

        :lang_pair: TODO

        """
        self.lang_pair = lang_pair

    def update_config(self, conf):
        """TODO: Docstring for update_config.

        :conf: TODO
        :returns: TODO

        """
        raise NotImplementedError

    def get_corpora(self, phrase, proxy=None):
        """TODO: Docstring for get_corpora.

        :phrase: TODO
        :proxy: TODO
        :returns: TODO

        """
        raise NotImplementedError
