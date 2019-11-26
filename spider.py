#!/usr/bin/env python
# encoding=utf8  
'''
Created on Nov 24, 2019
@author: turbine
'''

import requests
import os
from lxml import etree
from Utility import debugDumpTree, debugDumpDiv
import chardet
from Log import Logger
log = Logger(__name__)


def _getIpAndPort(node_list):
    def _travel_elements(nodes):
        index           = 0
        ip_offset       = 4
        port_offset     = ip_offset +1
        protocol_offset = port_offset + 4
        
        _bundle = {}

        for element in nodes.iter():
            index   = index + 1
            # ip:
            if index == ip_offset:
                # log.debug('ip tag=%s attr=%s text=%s' \
                #             % (element.tag, element.attrib, element.text))
                _bundle['ip'] = element.text

            elif index == port_offset:
                # log.debug('port tag=%s attr=%s text=%s' \
                #             % (element.tag, element.attrib, element.text))
                _bundle['port']=element.text
            elif index == protocol_offset:
                # log.debug('protocol tag=%s attr=%s text=%s' \
                #             % (element.tag, element.attrib, element.text))
                _bundle['protocol']=element.text
        
        return _bundle

    if len(node_list)==0:
        log.debug("empty div list %s" % node_list.__name__)
        return

    infos = []
    for div in node_list:
        log.debug('type=%s div = %s attribute= %s' % (repr(div) ,div.tag, div.attrib))
        infos.append(_travel_elements(div))
        
    
    return infos
            


def _parsing(page):
    try:
        tree   = etree.HTML(page)
        nodes  = tree.xpath(u'//tr[@class]')
        log.debug("dump index %s " % repr(nodes))
        proxys = []
        if len(nodes) > 0: proxys = _getIpAndPort(nodes)

        return proxys
        # for items in infos:
        #     log.debug("items %s " % repr(items))
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
    _proxys = _parsing(r.text)


    