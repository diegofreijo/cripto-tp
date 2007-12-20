import os
import sys
base = r'C:\Documents and Settings\Oem\Mis documentos\Cripto2007\Truco Mental\Repositorio'
for path in (base + r'\src\lib', base + r'\src\red', base + r'\test\red'):
  if os.path.exists(path):
    sys.path.append(path)
