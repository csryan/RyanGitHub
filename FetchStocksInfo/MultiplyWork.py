import os
import urllib2
from threading import Thread
from Queue import Queue
from time import sleep
from ReadProp import ReadProp
from ReadStocksList import ReadStocksList
from LinkOfPriceAndVolume import LinkOfPriceAndVolume
from LinkOfShortAndLongInfo import LinkOfShortAndLongInfo
from bs4 import *

class MultiplyWork(object):
    '''
    imporve the program efficiency by multiply thread
    '''
    def __init__(self):
        #initialize work queue
        self.workQueue = Queue()
        map(self.workQueue.put, ReadStocksList().getStockList())
#        stockList = ReadStocksList().getStockList()
#        list = [self.workQueue.put(code) for code in stockList]
        
        #initialize cpu core number
        self.cpuCore = ReadProp().getCPUCore()
        
        #clear error message
        errorTxt = ReadProp().getErrorMessageFile()
        if os.path.exists(errorTxt):
            os.remove(errorTxt)
    
    def doingWork(self, code):
        '''
        write stock information to file, file format: 
            'date    openPrice    closePrice    highestPrice lowestPrice    volume    long    short'
        '''
        openPriceDict = {}
        closePriceDict = {}
        highestPriceDict = {}
        lowestPriceDict = {}
        volumeDict = {}
        shortDict  = {}
        longDict   = {}
        
        #get volume and close price information
        lpv = LinkOfPriceAndVolume(code).GetLink()
        try:
            response = urllib2.urlopen(lpv)
        except urllib2.URLError:
            print 'price volume url open error while opening (%s)' % lpv
            return
        html = response.read()
        lines = html.split()
        for line in lines:
            perDayInfo = line.split(',')
            dateInfo = perDayInfo[0][0:4]+perDayInfo[0][5:7]+perDayInfo[0][8:10]
            openPriceDict[dateInfo] = perDayInfo[1]
            closePriceDict[dateInfo] = perDayInfo[3]
            highestPriceDict[dateInfo] = perDayInfo[2]
            lowestPriceDict[dateInfo] = perDayInfo[4]
            volumeDict[dateInfo] = perDayInfo[5]
        
        #get short and long information
        lsl = LinkOfShortAndLongInfo(code).GetLink()
        try:
            response = urllib2.urlopen(lsl)
        except urllib2.URLError:
            print 'long short url open error while opening (%s)' % lsl
            return
        html = response.read()
        soup = BeautifulSoup(html)
        trs = soup.findAll('tr')
        for i in range(len(trs)-3):
            sdate  = trs[i+3].contents[3].string
            slong  = trs[i+3].contents[5].string
            sshort = trs[i+3].contents[13].string
            dateInfo = sdate[0:4]+sdate[5:7]+sdate[8:10]
            shortDict[dateInfo] = sshort
            longDict[dateInfo] = slong
        
        savePath = ReadProp().getStocksInfoSavePath()
        if '/' != savePath[-1]:
            savePath = savePath + '/'
        if not os.path.exists(savePath):
            os.makedirs(savePath)
        
        appendix = ReadProp().getStockInfoFileAppendix()
        fname = savePath+code+appendix
        f = open(fname, 'wb+')
        e = open(ReadProp().getErrorMessageFile(), 'ab+')
        for k in sorted(closePriceDict):
            if k not in shortDict:
                estr = 'error(%s): date %s NOT exists in short or long data\n' % (code, k)
                e.write(estr)
                continue
            linestr = k+'\t'+str(openPriceDict[k])+'\t'+str(closePriceDict[k])+'\t'+str(highestPriceDict[k])+'\t'\
                +str(lowestPriceDict[k])+'\t'+str(volumeDict[k])+'\t'+str(longDict[k])+'\t'+str(shortDict[k])+os.linesep
            #linestr = k+'\t'+str(closePriceDict[k])+'\t'+str(volumeDict[k])+'\t'+str(shortDict[k])+'\t'+str(longDict[k])+os.linesep
            f.write(linestr)
            #print k, openPriceDict[k], closePriceDict[k], highestPriceDict[k], \
                #lowestPriceDict[k], volumeDict[k], longDict[k], shortDict[k]
        f.close()
        e.close()
        
    def threadWork(self):
        while True:
            code = self.workQueue.get()
            self.doingWork(code)
            sleep(1)
            self.workQueue.task_done()
    
    def startWork(self):
        for i in range(self.cpuCore):
            t = Thread(target=self.threadWork)
            t.setDaemon(True)
            t.start()
    
    def finishWork(self):
        self.workQueue.join()
        
