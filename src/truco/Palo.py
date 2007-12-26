# TP
# Matias
# Uso:
# import Palo
# Luego usar como un tipo enumerado: Palo.BASTO, Palo.ORO, p = Palo.BASTO
# p.esBasto(), p == q, etc

class _palo:
  palo = None

  def __init__(self, palo):
    if esPalo(palo):
      self.palo = palo.palo
    elif palo == 'BASTO' or palo == 'COPA' or palo == 'ESPADA' or palo == 'ORO':
      self.palo = palo
    else:
      raise ValueError('Argumento de tipo no permitido: ' + repr(palo))

  def esBasto(self):
    return (self.palo == BASTO.palo)

  def esCopa(self):
    return (self.palo == COPA.palo)

  def esEspada(self):
    return (self.palo == ESPADA.palo)

  def esOro(self):
    return (self.palo == ORO.palo)

  def __eq__(self, otro):
    if isinstance(otro, _palo): return (self.palo == otro.palo)
    if isinstance(otro, str): return (self.palo == otro)
    return False

  def __ne__(self, otro):
    return not (self == otro)

  def __hash__(self):
    return self.palo.__hash__()

  def __str__(self):
    return str(self.palo)

  def __repr__(self):
    return 'Palo('+repr(self.palo)+')'

def esPalo(obj):
  return isinstance(obj, _palo)

BASTO = _palo('BASTO')
COPA = _palo('COPA')
ESPADA = _palo('ESPADA')
ORO = _palo('ORO')

__all__ = ['esPalo', 'BASTO', 'COPA', 'ESPADA', 'ORO']
