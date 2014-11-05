import os
import urllib2
from threading import Thread
from Queue import Queue
from time import sleep
from ReadProp import ReadProp
from ReadStocksList import ReadStocksList
from LinkOfPriceAndVolume import LinkOfPriceAndVolume
from LinkOfShortAndLongInfo import LinkOfShortAndLongInfo
from ReadStockDatabase import ReadStockDatabase
from bs4 import *

class RThreadBase(object):
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
    
    def doingWork(self, code):
        rtd = ReadStockDatabase(code)
        if rtd.IsOK():
            #rtd.IsInMinimum()
            #rtd.PrintMinimum()
            rtd.LoopAndPrintMinimum()
    