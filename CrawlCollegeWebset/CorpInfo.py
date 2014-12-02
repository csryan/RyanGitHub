import os

########################################################################
class CorpInfo(self):
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        """
        'name':u'Google' #Corporation name
        'date': u'2014-11-21 12:55:18' #post date
        'link': u'http://career.nankai.edu.cn/index.php/Corpinternmsg/detail/id/5472' #specified link
        'content': u'&nbsp; 天津外国语大学附属外国语学校 2015 年公开招聘工作实...'    #the content of the link
        'address': u'天津' #address that the program calculated
        'position': u'教师'#job position that the program calculated
        
        {'name':{'date':'', 'link':'', 'content':'', 'address':'', 'position':''}}
        """
        
    #----------------------------------------------------------------------
    def reload(self):
        """reload corporation information"""
        pass
    
    #----------------------------------------------------------------------
    def addCorp(self, nameStr, dateStr, linkStr):
        """add corporation information"""
        pass
    
    #----------------------------------------------------------------------
    def isContained(self, nameStr, dateStr, linkStr):
        """check if the name is in CorpInfo or not"""
        return False
    
    #----------------------------------------------------------------------
    def getCertainDate(self, startDateStr, stopDateStr):
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
        