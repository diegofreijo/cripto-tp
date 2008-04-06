# -*- coding: cp1252 -*-
# Si es distinto de None, se fuerza una ubicación del proyecto
base = None
# Rutas de fuentes Python que deben agregarse a sys.path
srcList = [r'src/lib', r'src/red', r'src/truco', r'src/truco/Maura']
# Rutas de librerias binarias que deben agregarse a sys.path
# Se les agregará automáticamente ".win32" o ".linux-x86_64" según el equipo donde se ejecute
libList = [r'lib']

import os
if base == None:
  import inspect
  base = inspect.getsourcefile( lambda:None )
if base != None:
  base = os.path.abspath(base)
  if base != None: base = os.path.split(base)[0]
else:
  base = os.getcwd()
##print base

if not os.path.exists(base):
  print ''
  print 'ERROR: setpath.py no puede encontrar la ubicacion del proyecto cripto-tp'
  print '(cambiar la variable "base" para que apunte a la copia local del repositorio cripto-tp)'
  print ''
  quit()

# Crear la lista de directorios que hay que agregar a sys.path
pathList = srcList[:]
# Agregar antes los directorios "lib"
if libList != None:
  pathList = libList + pathList
# Agregar primero que todo los directorios "lib._plataforma_"
pathListTmp = []
try:
  import distutils.util
  plataforma = distutils.util.get_platform()
  pyversion = None
  try:
    import platform
    pyversion = platform.python_version()
  except:
    pass
  for libPrefijo in libList:
    p = libPrefijo + '.' + plataforma
    pathListTmp.append(p)
    if pyversion != None:
      p = p + '-' + pyversion
      pathListTmp.append(p)
  pathList = pathListTmp + pathList
except:
  pass
# Agregar los que existan
import sys
##print pathList
for pathSufijo in pathList:
  path = os.path.join(base, pathSufijo)
  if os.path.exists(path):
    #print '(setpath.py) agregando ' + path + ' a sys.path'
    sys.path.append(path)
