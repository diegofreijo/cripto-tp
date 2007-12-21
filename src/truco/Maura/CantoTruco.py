# TP
# Matias
# Uso:
# import CantoTruco

class _cantoTruco:
  codigo = None

  def __init__(self, codigo):
    if not isinstance(codigo, str) :
      raise ValueError('Argumentos de tipo no permitido - debe ser str');
    self.codigo = codigo

  def codigo():
    return self.codigo

  def __eq__(self, otro):
    if isinstance(otro, _cantoTruco):
      return (self.codigo == otro.codigo)
    raise ValueError('Argumento de tipo no permitido: ' + str(otro))

  def __ne__(self, otro):
    return not (self == otro)

  def __hash__(self):
    return self.codigo.__hash__()

  def __str__(self):
    return self.codigo

  def __repr__(self):
    return 'CantoTruco('+repr(self.codigo)+')'

# pseudo constantes
TRUCONOCANTADO=_cantoTruco('NADA')
TRUCO = _cantoTruco('TRUCO')
RETRUCO = _cantoTruco('RETRUCO')
VALE4 = _cantoTruco('VALE4')
QUIEROTRUCO = _cantoTruco('QUIERO')
NOQUIEROTRUCO = _cantoTruco('NO QUIERO')

CANTOS_TRUCO=[TRUCONOCANTADO,TRUCO,RETRUCO,VALE4]

def cantoSiguiente(canto):
  i = None
  if canto == TRUCONOCANTADO:
    i=1
  elif canto ==TRUCO:
    i = 2
  elif canto == RETRUCO:
    i = 3
  elif canto == VALE4:
    i = 4
  else:
    raise ValueError('No es un canto de truco: ' + repr(canto))
  return CANTOS_TRUCO[i]
