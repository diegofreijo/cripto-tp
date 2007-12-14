# Matias, basado en el formato de cartas hasheadas de Diego
# CartasDesdeArchivo
# Uso:
# import CartasDesdeArchivo
# c = CartasDesdeArchivo.carta(numero_con_el_codigo_recibido)
# if c == None:
#   raise ValueError('Eh! esa carta no existe!')
#
from Carta import *

cartaPorCodigo = None
codigoPorCarta = None

def leerCartasDesdeArchivo(arch):
  cartaPorCodigo = {}
  codigoPorCarta = {}
  fEntrada = open(arch, 'r')
  for linea in fEntrada:
    lin = linea.rstrip('\r\n \t').lstrip(' \t')
    if (len(lin) == 0 or lin[0] == '#'): continue # comentario
    try:
      tokens = lin.split(':')
      if len(tokens) != 2:
        print tokens
        raise RuntimeError('Formato de linea incorrecto, se esperaba nnP: codigo, se tiene ' + linea)
      codigo = tokens[1].strip()
      codigo = long(codigo)
      if (codigo in cartaPorCodigo):
        raise RuntimeError('Codigo de carta repetido en la linea: ' + linea)
      scarta = tokens[0].strip()
      spalo = scarta[-1:].upper()
      snum = scarta[:-1]
      palo = None
      if (spalo == 'B'): palo = Palo.BASTO
      elif (spalo == 'C'): palo = Palo.COPA
      elif (spalo == 'E'): palo = Palo.ESPADA
      elif (spalo == 'O'): palo = Palo.ORO
      else:
        raise ValueError('Carta incorrecta ' + tokens[0] + ' en la linea: ' + linea)
      numero = int(snum)
      carta = Carta(numero, palo)
      if (carta in codigoPorCarta):
        raise RuntimeError('Carta repetida en la linea: ' + linea)
      cartaPorCodigo[codigo] = carta
      codigoPorCarta[carta] = codigo
    except StandardError, e:
      print e
  #
  return (cartaPorCodigo, codigoPorCarta)

def inicializar(arch):
  global codigoPorCarta, cartaPorCodigo
  cartaPorCodigo, codigoPorCarta = leerCartasDesdeArchivo(arch)

def codigo(carta):
  try:
    return codigoPorCarta[carta]
  except:
    return None

def carta(codigo):
  try:
    return cartaPorCodigo[codigo]
  except:
    return None

def cartasValidas():
  return len(codigoPorCarta) == 40

# Inicializar los diccionarios para obtener codigo segun carta y viceversa
# en el momento de hacer import (discutible: podria usarse inicializar()
# manualmente para mayor flexibilidad)
inicializar("hasheadas.txt")
