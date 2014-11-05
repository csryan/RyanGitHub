import os
import datetime
from ReadProp import ReadProp

########################################################################
class ReadTimeController(object):
    '''
    read time information
    '''

    #----------------------------------------------------------------------
    def __init__(self):
        rp = ReadProp()
        tfile = rp.getStocksTimeControllerFile()
        f = open(tfile, 'r')
        
        #set last day as default value
        d = datetime.date.today() - datetime.timedelta(days=1)
        defaultTimeStr = '%.4d%.2d%.2d' % (d.year, d.month, d.day)
        startd = datetime.date(int(defaultTimeStr[0:4]),int(defaultTimeStr[4:6]),int(defaultTimeStr[6:8]))
        stopd  = startd
        
        self.startTime = defaultTimeStr
        self.stopTime  = defaultTimeStr
        self.maxDays   = '365'
        
        StartTime = ''
        StopTime  = ''
        MaximumDays = ''        
        for line in f:
            if 'StartTime' in line:
                exec line
                StartTime = StartTime.strip()
                #fullfill format YYYY-MM-DD
                if StartTime[0:4].isdigit() and StartTime[5:7].isdigit() and StartTime[8:10].isdigit():
                    self.startTime = StartTime[0:4]+StartTime[5:7]+StartTime[8:10]
            elif 'StopTime' in line:
                exec line
                StopTime = StopTime.strip()
                #fullfill format YYYY-MM-DD
                if StopTime[0:4].isdigit() and StopTime[5:7].isdigit() and StopTime[8:10].isdigit():
                    self.stopTime = StopTime[0:4]+StopTime[5:7]+StopTime[8:10]
            elif 'MaximumDays' in line:
                exec line
                MaximumDays = MaximumDays.strip()
                #fullfill format XXX
                if MaximumDays.isdigit():
                    self.maxDays = MaximumDays
        
        #get start date and stop date
        startEffective = self.startTime.isdigit() and len(self.startTime) == 8
        stopEffective  = self.stopTime.isdigit() and len(self.stopTime) == 8
        if startEffective:
            startd = datetime.date(int(self.startTime[0:4]),int(self.startTime[4:6]),int(self.startTime[6:8]))
        if stopEffective:
            stopd  = datetime.date(int(self.stopTime[0:4]),int(self.stopTime[4:6]),int(self.stopTime[6:8]))
        
        #incase one of start time or stop time is ineffective
        if startEffective and not stopEffective:
            stopd = startd + datetime.timedelta(days=int(self.maxDays))
        elif not startEffective and stopEffective:
            startd = stopd - datetime.timedelta(days=int(self.maxDays))
        elif not startEffective and not stopEffective:
            print 'Error: in resources/time, start and stop time are both ineffective'
            pass
        
        #incase start date or stop date is expanded
        if startd > d:
            startd = d
        if stopd > d:
            stopd = d
        
        #set start time and stop time avalible
        self.startTime = '%.4d%.2d%.2d' % (startd.year, startd.month, startd.day)
        self.stopTime  = '%.4d%.2d%.2d' % (stopd.year, stopd.month, stopd.day)
        
    def getStartTime(self):
        '''return type is YYYYMMDD'''
        return self.startTime
    
    def getStopTime(self):
        '''return type is YYYYMMDD'''
        return self.stopTime
    
    def getMaxDays(self):
        return self.maxDays
    
'''
if __name__ == '__main__':
    rtc = ReadTimeController()
    print 'start time is:   ', rtc.getStartTime()
    print 'stop time is:    ', rtc.getStopTime()
    print 'maximum days is: ', rtc.getMaxDays()
'''