import re

########################################################################
class RecompileOfLink(object):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, link):
        """Constructor"""
        self.link = link
        self.keys = {'nankai.edu.cn': re.compile(r'<div class="work_titleone">.*?</div>', re.S)}
    #----------------------------------------------------------------------
    def get(self):
        """"""
        for key in self.keys:
            if re.findall(key, self.link):
                return self.keys[key]
        return None