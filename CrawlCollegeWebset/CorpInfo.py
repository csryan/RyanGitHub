#!/usr/bin/env python
#coding:utf-8

import os
import re
import pickle
import pprint
import urllib2
import time

########################################################################
class CorpInfo(object):
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        """
        ########self.ci(corporatoin information) format: 'key':{info}, key=int(time.mktime(update_time))##########
        {'key':{'title':'', 'update_time':'', 'link':'', 'content':'', 'address':'', 'position':''}}
        self.ci value format:
            'title': string.(e.g.'Google') #Corporation title
            'update_time': time.struct_time.(e.g.'2014-11-21 12:55:18') #post update time
            'link': string.(e.g. 'http://career.nankai.edu.cn/index.php/Corpinternmsg/detail/id/5472') #specified link
            'content': string.(e.g.u'&nbsp; 天津外国语大学附属外国语学校 2015 年公开招聘工作实...') #the content of the link
            'address': string.(e.g.u'天津') #address that the program calculated
            'position': string. (e.g.u'教师') #job position that the program calculated
        ########self.lut(latest update time) format: int(time.mktime(update_time))###############################
        ########self.dbname(pickle file name)###############################
        """
        self.ci = {} #corporation information
        self.lut = int(time.time()) - 3600*24*30 #last update time will not expand 1 month
        self.dbname = None
    #-----------------reload database by the link---------------------------------------
    def reload(self, link):
        """reload corporation information database by the link"""
        main_page = re.findall('.*.edu.cn', l)[0]
        dbname = filter(None, re.split('[:/.]', main_page))[-3]
        self.dbname = 'database//' + dbname + '.pkl'
        if os.path.exists(self.dbname):
            with open(self.dbname, 'r') as f:
                self.ci = pickle.load(f)
                f.close()
        self.refreshLastUpdateTime()
    
    #----------------------------------------------------------------------
    def update(self, link):
        """add corporation information"""
        #reload self.ci by local storage
        self.reload(link)
        
        #update with link
        try:
            response = urllib2.urlopen(link)
        except urllib2.URLError:
            print 'update error with opening (%s)' % link
            return
        html = response.read()
        
        #get href
        href_title_c = re.compile(r'<p><a .*?</a></p>', re.S)
        href_title = href_title_c.findall(html)
        hrefc = re.compile(r'href=".*?"', re.S)
        href = map(lambda h: hrefc.findall(h)[0][6:-2], href_title)
        #get title
        titlec = re.compile(r'">.*?</a>', re.S)
        title = map(lambda h: titlec.findall(h)[0][2:-4].decode('utf-8'), href_title)
        #get update time
        update_time_c = re.compile(r'<div class="work_read_left">.*?</div>', re.S)
        update_time_str = map(lambda t: t.split()[2]+' '+t.split()[3], update_time_c.findall(html))
        update_time = map(lambda t: time.strptime(t, '%Y-%m-%d %H:%M:%S'), update_time_str)
        #get next page href
        next_page_c = re.compile(r'<li class="Paging_next"><a href=".*?">', re.S)
        next_page = next_page_c.findall(html)[0][33:-2]
        """
        print href
        print title
        print title[0]
        print update_time
        print next_page
        """
        """
        ##################self.ci format: 'key':{info}, key=int(time.mktime(update_time))##################
        {'key':{'title':'', 'update_time':'', 'link':'', 'content':'', 'address':'', 'position':''}}
        """
        ci_key = 0
        for i in range(len(href)):
            ci_key = int(time.mktime(update_time))
            if ci_key <= self.lut:
                break
            ci_value = {}
            ci_value['title'] = title[i]
            ci_value['update_time'] = update_time[i]
            ci_value['link'] = href[i]
            ci_value['content'] = None
            ci_value['address'] = None
            ci_value['position'] = None
            self.ci[ci_key] = ci_value
        if ci_key <= self.lut:
            return
        else:
            self.update(next_page)
    
    #----------------------------------------------------------------------
    def refreshLastUpdateTime(self):
        """refresh last update time after update by link"""
        if self.ci:
            self.lut = max(self.ci.keys())
    
    #----------------------------------------------------------------------
    def getCertainDateCI(self, start_date_str, stop_date_str):
        """return CorpInfo that in the date selection"""
        pass
    
    #----------------------------------------------------------------------
    def getCertainAddress(self, address):
        """return CorpInfo that in the address"""
        pass
    
    #----------------------------------------------------------------------
    def getCertainPosition(self, position):
        """return CorpInfo that is the job position"""
        pass
    
    #----------------------------------------------------------------------
    def getLastUpdateTime(self):
        """return the last updated time"""
        return self.lut
    
    #----------------------------------------------------------------------
    def restore(self):
        """restore corporation information to pickle"""
        with open(self.dbname, 'w+') as f:
            pickle.dump(self.ci, f)
            f.close()
    '''
if __name__ == '__main__':
    l = 'http://career.nankai.edu.cn/index.php/Corpinternmsg/index/type/1'
    main_page = re.findall('.*.edu.cn', l)[0]
    t = filter(None, re.split('[:/.]', main_page))[-3]
    print t
    '''