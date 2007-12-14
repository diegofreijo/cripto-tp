# -*- coding: cp1252 -*-
import random
from Primalidad import *
import time

b = 1024
q = 5000
t0 = time.clock()
for i in range(q):
  n = random.getrandbits(b)
  rv = MillerRabin(n, 10) # e < 0.25**(-10) ~ e < 10**(-6)
  if rv:
    print n, rv
#
t1 = time.clock()
print 'probados', q, 'numeros en', (t1-t0), 'segundos'
