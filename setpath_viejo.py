import os
import sys
base = r'C:\Documents and Settings\malbanesi\Mis documentos\_personal\workspace\cripto-tp'
if not os.path.exists(base):
  print ''
  print 'ERROR: modificar setpath.py'
  print '(cambiar la variable "base" para que apunte a la copia local del repositorio cripto-tp)'
  print ''
  quit()
#for path in (base + r'\src\lib', base + r'\src\red', base + r'\src\truco', base + r'\src\truco\Maura'):
for path in (base + r'\src\lib', base + r'\src\red', base + r'\src\truco', base + r'\src\truco_v1'):
  if os.path.exists(path):
    sys.path.append(path)
