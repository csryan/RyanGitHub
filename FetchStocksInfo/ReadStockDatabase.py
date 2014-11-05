import os
import sys
from ReadStocksList import ReadStocksList
from ReadProp import ReadProp
from collections import namedtuple

DataCountPerLine = 8
DateCursor         = 0
OpenPriceCursor    = 1
ClosePriceCursor   = 2
HighestPriceCursor = 3
LowestPriceCursor  = 4
VolumeCursor       = 5
LongInfoCursor     = 6
ShortInfoCursor    = 7

DaysRemained = 2

########################################################################
class ReadStockDatabase(object):
    '''
    get the stock information from database or file
    '''

    #----------------------------------------------------------------------
    def __init__(self, stock):
        #store stockInfoList and stockInfoDict in reverse order, latest date info is in the front
        self.isOK = False
        self.code = stock
        self.stockInfoDict = {}
        self.stockInfoList = []
        
        #get matching stock file name
        if not stock.isdigit():
            print 'Error: stock No. is NOT a digit'
            return
        fName = ReadProp().getStocksInfoSavePath()
        if '/' != fName[-1]:
            fName = fName + '/'
        fName = fName + stock + ReadProp().getStockInfoFileAppendix()
        if not os.path.exists(fName):
            print 'Error: stock information of %s has NOT found' % (fName)
            return
        self.isOK = True
        
        #read stock file to "self.stockInfoDict"
        f = open(fName, 'r')
        StockData = namedtuple('StockData', 'openPrice closePrice highestPrice lowestPrice volume longInfo shortInfo longDivShort')
        for line in f:
            info = line.split()
            
            if DataCountPerLine == len(info):
                key = info[DateCursor]
                dataOnKey = StockData(openPrice=float(info[OpenPriceCursor]), closePrice=float(info[ClosePriceCursor]), \
                                  highestPrice=float(info[HighestPriceCursor]), lowestPrice=float(info[LowestPriceCursor]), \
                                  volume=int(info[VolumeCursor]), longInfo=float(info[LongInfoCursor]), \
                                  shortInfo=float(info[ShortInfoCursor]), longDivShort=.0-sys.maxint)
                if 0 != int(dataOnKey.shortInfo):
                    lds = dataOnKey.longInfo/dataOnKey.shortInfo
                    dataOnKey = dataOnKey._replace(longDivShort=lds)
                self.stockInfoDict[key] = dataOnKey
        
        #sort "self.stockInfoList" to reverse order
        self.stockInfoList = sorted(self.stockInfoDict.iteritems(), key=lambda x: x[0], reverse=True)
        #print self.stockInfoList
        
    def GetLatestStockInfoDict(self, days):
        if days > len(self.stockInfoList):
            days = len(self.stockInfoList)
        return dict(self.stockInfoList[:days])
    
    def GetNDaysLatestStockInfoDict(self, n, days):
        if days > len(self.stockInfoList)-n:
            days = len(self.stockInfoList)-n
        return dict(self.stockInfoList[n:days+n])
    
    def IsInMinimum(self):
        rangeOfPeriod = ReadProp().getRangeOfPeriod()
        referPeriod   = ReadProp().getReferPeriod()
        
        if int(rangeOfPeriod) > len(self.stockInfoList) or int(referPeriod) > len(self.stockInfoList):
            print 'Error: no enough data(%d) in stock(%s) for range of period(%d) or refer period(%d)' % (len(self.stockInfoList), \
                                                                                               self.code, \
                                                                                               int(rangeOfPeriod), \
                                                                                               int(referPeriod))
            return
        
        ropDict = self.GetLatestStockInfoDict(int(rangeOfPeriod))
        ropList = sorted(ropDict.iteritems(), key=lambda x:x[1].longDivShort, reverse=True)
        
        rpDict = self.GetLatestStockInfoDict(int(referPeriod))
        rpList = sorted(rpDict.iteritems(), key=lambda x:x[0], reverse=True)
        
        isSatisfied = False
        for i in range(len(rpList)):
            if ropList[i][0] != rpList[i][0]:
                isSatisfied = False
                break
            else:
                isSatisfied = True
        if isSatisfied:
            print '==================>', self.code
            #print 'range of period:'
            #print ropList
            #print 'refer period:'
            #print rpList
        
    def IsOK(self):
        return self.isOK
    
    def PrintMinimum(self):
        '''
        if lastThirdDay to range of period stock information satisfy minimum conditions, \
            print the lastDay's and lastSecondDay's price going
        '''
        rangeOfPeriod = ReadProp().getRangeOfPeriod()
        referPeriod   = ReadProp().getReferPeriod()
        
        if int(rangeOfPeriod)+DaysRemained > len(self.stockInfoList) or int(referPeriod)+DaysRemained > len(self.stockInfoList):
            print 'Error: no enough data(%d) in stock(%s) for range of period(%d) or refer period(%d)' % (len(self.stockInfoList), \
                                                                                               self.code, \
                                                                                               int(rangeOfPeriod), \
                                                                                               int(referPeriod))
            return
        
        ropDict = self.GetNDaysLatestStockInfoDict(DaysRemained, int(rangeOfPeriod))
        ropList = sorted(ropDict.iteritems(), key=lambda x:x[1].longDivShort, reverse=True)
        
        rpDict = self.GetNDaysLatestStockInfoDict(DaysRemained, int(referPeriod))
        rpList = sorted(rpDict.iteritems(), key=lambda x:x[0], reverse=True)
        
        isSatisfied = False
        for i in range(len(rpList)):
            if ropList[i][0] != rpList[i][0]:
                isSatisfied = False
                break
            else:
                isSatisfied = True
        if isSatisfied:
            lastDayData = self.stockInfoList[0][1]
            lastSecondDayData = self.stockInfoList[1][1]
            print self.code, '==================>', (lastDayData.openPrice/lastSecondDayData.openPrice - 1.0)*100
        
    def LoopAndPrintMinimum(self):
        '''
        loop entire stock information until lastThirdDay+rangeOfPeriod >= len(self.stockInfoList):
            if lastThirdDay to range of period stock information satisfy minimum conditions, \
                print the lastDay's and lastSecondDay's price going
        '''
        rangeOfPeriod = ReadProp().getRangeOfPeriod()
        referPeriod   = ReadProp().getReferPeriod()
        
        if int(rangeOfPeriod)+DaysRemained > len(self.stockInfoList) or int(referPeriod)+DaysRemained > len(self.stockInfoList):
            print 'Error: no enough data(%d) in stock(%s) for range of period(%d) or refer period(%d)' % (len(self.stockInfoList), \
                                                                                               self.code, \
                                                                                               int(rangeOfPeriod), \
                                                                                               int(referPeriod))
            return
        
        fluctuationList = []
        #print "=============>", self.code
        for k in range(len(self.stockInfoList)-rangeOfPeriod-DaysRemained):
            ropDict = self.GetNDaysLatestStockInfoDict(DaysRemained+k, int(rangeOfPeriod))
            ropList = sorted(ropDict.iteritems(), key=lambda x:x[1].longDivShort, reverse=True)
            
            rpDict = self.GetNDaysLatestStockInfoDict(DaysRemained+k, int(referPeriod))
            rpList = sorted(rpDict.iteritems(), key=lambda x:x[0], reverse=True)
            
            isSatisfied = False
            for i in range(len(rpList)):
                if ropList[i][0] != rpList[i][0]:
                    isSatisfied = False
                    break
                else:
                    isSatisfied = True
            if isSatisfied:
                lastDayData = self.stockInfoList[k][1]
                lastSecondDayData = self.stockInfoList[k+1][1]
                fluctuationList.append(tuple([self.stockInfoList[k][0], (lastDayData.openPrice/lastSecondDayData.openPrice - 1.0)*100]))
                #print '    ', self.stockInfoList[k][0], '--------------------->', (lastDayData.openPrice/lastSecondDayData.openPrice - 1.0)*100
        if 0 < len(fluctuationList):
            sumOfFluctuation = 0.0
            for i in range(len(fluctuationList)):
                sumOfFluctuation = sumOfFluctuation + fluctuationList[i][1]
            avgOfFluctuation = sumOfFluctuation/len(fluctuationList)
            print self.code, "=============>", avgOfFluctuation
        
'''
if __name__ == '__main__':
    rsd = ReadStockDatabase('000001')
    mDict = rsd.GetLatestStockInfoDict(30)
    mList = sorted(mDict.iteritems(), key=lambda x:x[0], reverse=True)
    print mList
    print mList[0][0]
    
    rsd.IsInMinimum()
'''
