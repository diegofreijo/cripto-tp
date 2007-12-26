# -*- coding: cp1252 -*-
# TP
# Matias
# Uso:
# from Carta import *
# c = Carta(Palo.COPA, 4)
# c2 = Carta(4, Palo.COPA)
import Palo

class Carta:
  _palo = None
  _numero = None

  def __init__(self, numero, palo):
    arg0 = numero
    arg1 = palo
    if Palo.esPalo(arg0) and isinstance(arg1, int):
      palo = arg0
      numero = arg1
    elif isinstance(arg0, int) and Palo.esPalo(arg1):
      palo = arg1
      numero = arg0
    else:
      raise ValueError('Argumentos de tipo no permitido - deben ser int y Palo.')
    if numero < 1 or (numero >= 8 and numero <= 9) or numero > 12:
      raise ValueError('Numero de la carta incorrecto: ' + str(numero))
    self._palo = palo
    self._numero = numero

  def palo(self):
    return self._palo

  def numero(self):
    return self._numero

  def esBasto(self):
    return self._palo.esBasto()

  def esCopa(self):
    return self._palo.esCopa()

  def esEspada(self):
    return self._palo.esEspada()

  def esOro(self):
    return self._palo.esOro()

  def esFigura(self):
    return self._numero >= 10

  def __eq__(self, otra):
    if isinstance(otra, Carta):
      return (self._palo == otra._palo and self._numero == otra._numero)
    raise ValueError('Argumento de tipo no permitido: ' + str(otra))

  def __ne__(self, otra):
    return not (self == otra)

  def __hash__(self):
    return self._palo.__hash__() ^ self._numero.__hash__()

  def __str__(self):
    sn = str(self._numero)
    if (self._numero == 1): sn = 'Ancho'
    if (self._numero == 12): sn = 'Rey'
    return sn + ' de ' + str(self._palo)

  def __repr__(self):
    return 'Carta('+repr(self._numero)+', '+repr(self._palo)+')'

