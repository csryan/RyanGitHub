from ReadProp import ReadProp

class ReadStocksList(object):
    '''
    read stocks list, and reture stocks' code
    '''
    
    #----------------------------------------------------------------------
    def __init__(self):
        rp = ReadProp()
        tfile = rp.getStocksCodeListFile()
        f = open(tfile, 'r')
        self.stocksList = []
        
        for line in f:
            stockInfo = line.split()
            stockCode = stockInfo[0]
            self.stocksList.append(stockCode)
        
    def getStockList(self):
        return self.stocksList
    

'''
if __name__ == '__main__':
    lists = ReadStocksList().getStockList()
    for index in range(len(lists)):
        print lists[index], type(lists[index])
'''