# -*- coding: cp1252 -*-
execfile(r'..\..\setpath_viejo.py')

import os
import re
import doctest


def _test():
  # Reemplazar con el directorio donde estén los archivos *.test y
  # este script (UnitTestingManoTruco.py)
  os.chdir(r'C:\Documents and Settings\malbanesi\Mis documentos\_personal\workspace\cripto-tp\test\truco_viejo')
  #os.chdir(r'D:\mac@sion.com\workspace\cripto-tp\test\truco_viejo')
  regexp = re.compile('^ManoTruco.+\\.test$', re.IGNORECASE)
  t = os.listdir('.')
  lista = []
  for e in t:
    if os.path.isfile(e) and regexp.match(e):
      lista.append(e)
  # Ejecutar los tests uno por uno, hasta que alguno falle
  for e in lista:
    cantFallas, cantTests = doctest.testfile(e) # , verbose=True
    if cantFallas > 0:
      break
    else:
      print 'Test \'' + e + '\' exitoso.'


if __name__ == "__main__":
    _test()
