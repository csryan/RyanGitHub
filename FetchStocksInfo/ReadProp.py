import os

PROPERTY_FILE = 'fsi.prop'

########################################################################
class ReadProp(object):
    '''
    test
    read property information(fsi.prop, pointed to fetch stock information property)
    '''
    #----------------------------------------------------------------------
    def __init__(self):
        fileName = PROPERTY_FILE
        f = open(fileName, 'r')
        
        self.stocksCodeListFile = ''
        self.stocksTimeControllerFile = ''
        self.stocksInfoSavePath    = 'cluster/'
        self.stockInfoFileAppendix = '.txt'
        self.CPUCore = 2
        self.errorMsg = 'errors.txt'
        self.rangeOfPeriod = 30
        self.referPeriod = 1
        
        for line in f:
            if 'StocksCodeListFile' in line:
                exec line
                self.stocksCodeListFile = StocksCodeListFile
            elif 'StocksTimeControllerFile' in line:
                exec line
                self.stocksTimeControllerFile = StocksTimeControllerFile
            elif 'StocksInfoSavePath' in line:
                exec line
                self.stocksInfoSavePath = StocksInfoSavePath
            elif 'StockInfoFileAppendix' in line:
                exec line
                self.stockInfoFileAppendix = StockInfoFileAppendix
            elif 'CPUCore' in line:
                exec line
                self.CPUCore = CPUCore
            elif 'ErrorMessage' in line:
                exec line
                self.errorMsg = ErrorMessage
            elif 'RangeOfPeriod' in line:
                exec line
                self.rangeOfPeriod = RangeOfPeriod
            elif 'ReferPeriod' in line:
                exec line
                self.referPeriod = ReferPeriod
        
    def getStocksCodeListFile(self):
        return self.stocksCodeListFile
    
    def getStocksTimeControllerFile(self):
        return self.stocksTimeControllerFile
    
    def getStocksInfoSavePath(self):
        return self.stocksInfoSavePath
    
    def getStockInfoFileAppendix(self):
        return self.stockInfoFileAppendix
    
    def getCPUCore(self):
        return self.CPUCore
    
    def getErrorMessageFile(self):
        return self.errorMsg
    
    def getRangeOfPeriod(self):
        return self.rangeOfPeriod
    
    def getReferPeriod(self):
        return self.referPeriod
    
'''
if __name__ == '__main__':
    rp = ReadProp()
    print 'stocks code list file:       ', rp.getStocksCodeListFile()
    print 'stocks time controller file: ', rp.getStocksTimeControllerFile()
    print 'stocks info save path:       ', rp.getStocksInfoSavePath()
    print 'stock info file appendix:    ', rp.getStockInfoFileAppendix()
    print 'stock error message:         ', rp.getErrorMessageFile()
    print 'stock range of period:       ', rp.getRangeOfPeriod()
    print 'stock refer period:          ', rp.getReferPeriod()
'''
