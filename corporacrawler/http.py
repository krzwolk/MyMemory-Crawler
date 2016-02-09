# -*- coding: utf-8 -*-
"""
Description: 
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import urllib

def iter_proxies(path):
    """TODO: Docstring for iter_proxies.

    :path: TODO
    :returns: TODO

    """
    with open(path) as f:
        for line in f:
            proxy = line.strip()
            yield dict(
                http=proxy,
                https=proxy
            )

class ProxyPool(object):

    """Proxy pool, proxy cycled using round robin"""

    def __init__(self, proxies):
        """TODO: to be defined1.

        :proxies: TODO

        """
        self.proxies = proxies
        self.n = 0

    def get(self):
        """TODO: Docstring for get.
        :returns: TODO

        """
        if self.n >= len(self.proxies):
            self.n = 0
        proxy = self.proxies[self.n]
        self.n += 1
        return proxy
