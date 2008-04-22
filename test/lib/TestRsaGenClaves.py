if __name__ == '__main__':
  execfile('../../setpath.py')
import Rsa
from math import log

pruebas = 1000
mal = 0
bien = 0
for i in range(pruebas):
  print str(i) + '  ',
  n, e, d = Rsa.GenerarClaves(256)
  if Rsa.DesencriptarTexto(Rsa.EncriptarTexto('HolaComoTeVa',e,n),d,n) == 'HolaComoTeVa':
    bien = bien + 1
  else:
    mal = mal + 1
    

print 'bien: ' + str(bien)
print 'mal: ' + str(mal)
