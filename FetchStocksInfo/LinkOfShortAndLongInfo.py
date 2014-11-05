import os
from ReadTimeController import ReadTimeController

########################################################################
class LinkOfShortAndLongInfo(object):
    '''
    get the short and long information of the stock
    link demo:
        "http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml?symbol=sh601333&bdate=2013-11-01&edate=2014-03-23"
    '''

    #----------------------------------------------------------------------
    def __init__(self, stock):
        if not stock.isdigit():
            print 'Error: stock No. is NOT a digit'
            return
        code     = int(stock)
        timeCtrl = ReadTimeController()
        
        stringBeforeSymbol    = 'http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml?symbol='
        stringBeforeBeginData = '&bdate='
        stringBeforeEndData   = '&edate='
        StringSuffix = ''
        
        if code < 600000:
            self.symbol = "sz%.6d" % code
        else:
            self.symbol = "sh%.6d" % code
        
        bd = timeCtrl.getStartTime()
        ed = timeCtrl.getStopTime()
        self.beginDate = bd[0:4] + '-' + bd[4:6] + '-' + bd[6:8]
        self.endDate   = ed[0:4] + '-' + ed[4:6] + '-' + ed[6:8]
#        self.beginDate = '2013-01-01'
#        self.endDate   = '2014-01-01'
        
        self.link = stringBeforeSymbol + self.symbol + stringBeforeEndData + self.endDate \
            + stringBeforeBeginData + self.beginDate + StringSuffix
        
    def GetLink(self):
        return self.link
    
'''
if __name__ == '__main__':
    lsl = LinkOfShortAndLongInfo('000001')
    print 'link: ', lsl.GetLink()
'''