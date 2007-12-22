import os
import sys
base = r'D:\mac@sion.com\workspace\cripto-tp'
if not os.path.exists(base):
  print ''
  print 'ERROR: modificar setpath.py'
  print '(cambiar la variable "base" para que apunte a la copia local del repositorio cripto-tp)'
  print ''
  quit()
for path in (base + r'\src\lib', base + r'\src\red', base + r'\src\truco'):
  if os.path.exists(path):
    sys.path.append(path)
