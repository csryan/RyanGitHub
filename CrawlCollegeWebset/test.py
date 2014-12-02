#!/usr/bin/env python

import re
import os
import urllib2
from threading import Thread
from Queue import Queue
import time

########################################################################
class ProcessJobsListLink(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, link):
        """Constructor"""
        self.link = link
    
    def process(self):
        """
        try:
            response = urllib2.urlopen(self.link)
        except urllib2.URLError:
            print 'price volume url open error while opening (%s)' % lpv
            return
        html = response.read()
        """
        html = ''
        with open(r'3[1].txt') as f:
            html = f.read()
            f.close()
#        print html
        
        href_title_c = re.compile(r'<p><a .*?</a></p>', re.S)
        self.href_title = href_title_c.findall(html)
        hrefc = re.compile(r'href=".*?"', re.S)
        self.href = map(lambda h: hrefc.findall(h)[0][6:-2], self.href_title)
        print self.href
        titlec = re.compile(r'">.*?</a>', re.S)
        self.title = map(lambda h: titlec.findall(h)[0][2:-4].decode('utf-8'), self.href_title)
        print self.title
        print self.title[0]
        time_c = re.compile(r'<div class="work_read_left">.*?</div>', re.S)
        self.time_str = map(lambda t: t.split()[2]+' '+t.split()[3], time_c.findall(html))
        self.time = map(lambda t: time.strptime(t, '%Y-%m-%d %H:%M:%S'), self.time_str)
        print self.time
        
    
    #----------------------------------------------------------------------
    def getCompile(self, link):
        """"""
        #check if it's Nankai University
#        gc = re.compile(r'<div class="work_titleone">.*</div>')
        gc = re.compile(r'<div class="work_titleone">.*?</div>', re.S)
        
        return gc
    
if __name__ == '__main__':
    pjll = ProcessJobsListLink('http://career.nankai.edu.cn/index.php/Corpinternmsg/index/type/1')
    pjll.process()
    