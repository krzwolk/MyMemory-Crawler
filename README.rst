About
=====

This script uses dictionary of words or phrases, for each word it gets parallel corpora from website http://mymemory.translated.net/ and saves to two parallel files. 

It is possible to use proxies. List of proxies should be saved to file, example
format of such file:

http://1.1.1.1:8000
http://2.2.2.2:8080

Usage
=====

Result corpora is saved in same folder as input file

Supported websites
------------------

http://mymemory.translated.net/

Supported crawling methods (see conf.json):
    * api (as a rule less results)
    * web (default)

Final info
====

Feel free to use this tool if you cite:
Wołk K., Marasek K., “Polish – English Speech Statistical Machine Translation Systems for the IWSLT 2013.”, Proceedings of the 10th International Workshop on Spoken Language Translation, Heidelberg, Germany, p. 113-119, 2013

For more information, see: http://arxiv.org/pdf/1509.09097

For any questions:
| Krzysztof Wolk
| krzysztof@wolk.pl
