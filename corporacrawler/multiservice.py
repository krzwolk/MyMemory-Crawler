# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from .corporaservice import CorporaService

class MultiService(CorporaService):

    """Docstring for MultiService. """

    def __init__(self, lang_pair):
        """TODO: to be defined1.

        :lang_pair: TODO

        """
        CorporaService.__init__(self, lang_pair)

        self.services = []

    def register(self, service, conf=None):
        """TODO: Docstring for register.

        :service: TODO
        :conf: TODO
        :returns: TODO

        """
        if conf is None:
            conf = {}
        new_service = service(self.lang_pair)
        new_service.update_config(conf)
        self.services.append(new_service)

    def update_config(self, conf):
        """TODO: Docstring for update_config.

        :conf: TODO
        :returns: TODO

        """
        pass

    def get_corpora(self, phrase, proxy=None):
        """TODO: Docstring for get_corpora.

        :phrase: TODO
        :proxy: TODO
        :returns: TODO

        """
        for service in self.services:
            for pair in service.get_corpora(phrase, proxy):
                yield pair
