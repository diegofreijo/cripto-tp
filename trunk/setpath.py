import os
import sys
base = r'D:\mac@sion.com\Cripto-TP'
for path in (base + r'\src\lib', base + r'\src\red', base + r'\test\red'):
  if os.path.exists(path):
    sys.path.append(path)
