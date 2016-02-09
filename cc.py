# -*- coding: utf-8 -*-
"""
Description: For provided phrases script retrieves parallel corpora from
websites and saves it to two parallel files. Input file should contain phrases -
one per line.

It is possible to use proxies. List of proxies should be saved to file, example
format of such file:

http://1.1.1.1:8000
http://2.2.2.2:8080

Examle command:

    $ python cc.py --input text.pl --lang pl-en --threads 2

Result corpora is saved in same folder as input file

Supported websites
------------------

http://mymemory.translated.net/

Supported crawling methods (see conf.json):
    * api (as a rule less results)
    * web (default)

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import os
import multiprocessing as mp
import json
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
from codecs import open as copen
from corporacrawler.corpora import LangPair
from corporacrawler.multiservice import MultiService
from corporacrawler.mymemorytranslatednet import MMCorporaService
from corporacrawler.http import iter_proxies, ProxyPool

def as_lang_pair(val):
    """TODO: Docstring for as_lang_pair.

    :val: TODO
    :returns: TODO

    """
    return LangPair(*val.split('-'))

def get_output_paths(path, prefix, lang_pair):
    """TODO: Docstring for get_output_paths.

    :path: TODO
    :prefix: TODO
    :lang_pair: TODO
    :returns: TODO

    """
    tmpl = '{}{}_{}'
    name = os.path.basename(path)
    base = os.path.dirname(path)
    return os.path.join(base, tmpl.format(prefix, lang_pair.l1, name)), \
            os.path.join(base, tmpl.format(prefix, lang_pair.l2, name))

def iter_file(path):
    """TODO: Docstring for iter_file.

    :path: TODO
    :returns: TODO

    """
    with copen(path, encoding='utf-8') as in_file:
        for line in in_file:
            yield line.strip()

def as_proxy_pool(path):
    """TODO: Docstring for as_proxy_pool.

    :path: TODO
    :returns: TODO

    """
    if path:
        proxies = list(iter_proxies(path))
        return ProxyPool(proxies)
    else:
        return None

# async support
corpora_service = None
def init_corpora_service(lang_pair, conf=None):
    """TODO: Docstring for init_corpora_service.

    :lang_pair: TODO
    :returns: TODO

    """
    global corpora_service
    corpora_service = MultiService(lang_pair)
    try:
        mm_conf = conf['services']['mymemorytranslatednet']
    except (TypeError, KeyError):
        mm_conf = {}
    corpora_service.register(MMCorporaService, mm_conf)

def get_corpora(data):
    """TODO: Docstring for get_corpora.

    :args: TODO
    :returns: TODO

    """
    phrase = data[0]
    proxy = data[1]
    return list(corpora_service.get_corpora(phrase, proxy))

def iter_phrases(path, proxy_pool):
    """TODO: Docstring for iter_phrases.

    :path: TODO
    :proxy_pool: TODO
    :returns: TODO

    """
    for phrase in iter_file(path):
        proxy = None
        if proxy_pool:
            proxy = proxy_pool.get()
        yield phrase, proxy

if __name__ == '__main__':
    log = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('requests').setLevel(logging.WARN)
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser.add_argument('--input', required=True, help='Path to file with phrases')
    parser.add_argument('--lang', required=True, type=as_lang_pair, help='Language pair used for search (eg. pl-en), first language is language of input file')
    parser.add_argument('--prefix', default='corpora_', help='Prefix used in output file')
    parser.add_argument('--conf', default='conf.json', help='Path to configuration file')
    parser.add_argument('--proxies', type=as_proxy_pool, help='Path to file with proxies, one proxy per line, eg. http://127.0.0.1:8080')
    parser.add_argument('--threads', default=1, type=int, help='Number of threads to be used for crawling')
    args = parser.parse_args()

    with open(args.conf) as f:
        conf = json.load(f)
    pool = mp.Pool(args.threads, init_corpora_service, (args.lang, conf))
    file1_path, file2_path = get_output_paths(args.input, args.prefix, args.lang)
    file1 = copen(file1_path, 'w', encoding='utf-8')
    file2 = copen(file2_path, 'w', encoding='utf-8')

    for i, pairs in enumerate(pool.imap(get_corpora, iter_phrases(args.input, args.proxies))):
        for pair in pairs:
            file1.write(pair[0] + u'\n')
            file2.write(pair[1] + u'\n')
        if i % 100 == 0:
            log.info('Phrase %s', i+1)

    file1.close()
    file2.close()
