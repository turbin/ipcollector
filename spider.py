#!/usr/bin/env python
# encoding=utf8  
'''
Created on Nov 24, 2019
@author: turbine
'''

import requests
import os
from lxml import etree
from Utility import debugDumpTree
import chardet
from Log import Logger
log = Logger(__name__)

def _parsing(page):
    try:
        # log.debug("page coding in %s:" % chardet.detect(page)['encoding'])
        # encoding = chardet.detect(page)['encoding']
        # log.info("page =%s" % page)

        # log.warn("page=" % repr(page))
        tree   = etree.HTML(page)
        items  = tree.xpath(u'//tr[@class="odd"]|//tr[@class]')
        log.debug("dump items %s " % repr(items))
        if len(items) > 0: debugDumpTree(items[0])
    except Exception as e:
        log.error("parser tree error %s" % repr(e))
        return []

def _decode(s, codeset='utf-8'):
    g = s.decode(codeset)
    return g

def _encode(s, codeset='utf-8'):
    g = s.encode(codeset)
    return g

if __name__ == "__main__":
    headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get('https://www.xicidaili.com/nn/',headers=headers)
    log.debug("status code %d" % (r.status_code))
    _parsing(r.text)
    # with open('page.html','w')  as f:
    #     f.write(_decode(r.text))
    #     pass

    