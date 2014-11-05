import os
from ReadTimeController import ReadTimeController

########################################################################
class LinkOfPriceAndVolume(object):
    '''
    get the price and volume link information of the stock
    link demo:
        "http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?&rand=random(10000)&symbol=sz002241&end_date=20130806&begin_date=20130101&type=plain"
    '''

    #----------------------------------------------------------------------
    def __init__(self, stock):
        if not stock.isdigit():
            print 'Error: stock No. is NOT a digit'
            return
        code     = int(stock)
        timeCtrl = ReadTimeController()
        
        stringBeforeSymbol    = 'http://biz.finance.sina.com.cn/stock/flash_hq/kline_data.php?&rand=random(10000)&symbol='
        stringBeforeEndData   = '&end_date='
        stringBeforeBeginData = '&begin_date='
        StringSuffix = '&type=plain'
        
        if code < 600000:
            self.symbol = "sz%.6d" % code
        else:
            self.symbol = "sh%.6d" % code
        
        self.beginDate = timeCtrl.getStartTime()
        self.endDate   = timeCtrl.getStopTime()
#        self.beginDate = '20130101'
#        self.endDate   = '20140101'
        
        self.link = stringBeforeSymbol + self.symbol + stringBeforeEndData + self.endDate \
            + stringBeforeBeginData + self.beginDate + StringSuffix
        
    def GetLink(self):
        return self.link
    
'''
if __name__ == '__main__':
    lpv = LinkOfPriceAndVolume('000001')
    print 'link: ', lpv.GetLink()
'''