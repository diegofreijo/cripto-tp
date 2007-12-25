# TP
# Matias
# Uso:
# from Carta import *
# c = Carta(Palo.COPA, 4)
# c2 = Carta(4, Palo.COPA)
import Palo

class Carta:
  palo = None
  numero = None

  def __init__(self, numero, palo):
    arg0 = numero
    arg1 = palo
    if isinstance(arg0, Palo._palo) and isinstance(arg1, int):
      palo = arg0
      numero = arg1
    elif isinstance(arg0, int) and isinstance(arg1, Palo._palo):
      palo = arg1
      numero = arg0
    else:
      raise ValueError('Argumentos de tipo no permitido - deben ser int y Palo.')
    if numero < 1 or (numero >= 8 and numero <= 9) or numero > 12:
      raise ValueError('Numero de la carta incorrecto: ' + str(numero))
    self.palo = palo
    self.numero = numero

  def palo():
    return self.palo

  def numero():
    return self.numero

  def esBasto(self):
    return self.palo.esBasto()

  def esCopa(self):
    return self.palo.esCopa()

  def esEspada(self):
    return self.palo.esEspada()

  def esOro(self):
    return self.palo.esOro()

  def esFigura(self):
    return self.numero >= 10

  def __eq__(self, otra):
    if not isinstance(otra, Carta): return False
    return (self.palo == otra.palo and self.numero == otra.numero)

  def __ne__(self, otra):
    return not (self == otra)

  def __hash__(self):
    return self.palo.__hash__() ^ self.numero.__hash__()

  def __str__(self):
    sn = str(self.numero)
    if (self.numero == 1): sn = 'Ancho'
    if (self.numero == 12): sn = 'Rey'
    return sn + ' de ' + str(self.palo)

  def __repr__(self):
    return 'Carta('+repr(self.numero)+', '+repr(self.palo)+')'

