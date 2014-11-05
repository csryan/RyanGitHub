import os
from collections import namedtuple

#code = 600005
#k = '20140412'

#estr = 'error(%d): date %s NOT exists in short or long data\n' % (code, k)
#print estr

#e = open('errors.txt', 'ab+')
#e.write(estr)
#e.close()

#i = 0
#for i in range(5):
    #if i == 9:
        #break
#print i

#c = 1.01
#e = 1.0
#for i in range(200):
    #e = e*c
#print e

X = namedtuple('X', 'a b c')
xx = X(a=1, b=2, c=3)
print xx
xx = xx._replace(b=5)
print xx

