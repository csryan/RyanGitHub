#!/usr/bin/env python
#coding:utf-8
import os

########################################################################
class TargetWorkAddress(object):
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.work_address = '天津' #tianjin in chinese
#        print 'X=====', self.work_address.decode('utf-8')
    
    def get(self):
        return self.work_address.decode('utf-8')
    
    """
if __name__ == '__main__':
    twa = TargetWorkAddress()
    print 'A-------'
    print twa.get()
    print 'B-------'
    """