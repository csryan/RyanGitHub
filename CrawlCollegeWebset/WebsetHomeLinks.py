import os

########################################################################
class WebsetHomeLinks(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, linkfile):
        """Constructor"""
        self.linkFile = linkfile
        self.linkList = []
    
    def get(self):
        with open(self.linkFile) as f:
            for link in f:
                self.linkList.append(link)
            f.close()
        return self.linkList
    