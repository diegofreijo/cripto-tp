# TP
# Matias
# Uso:
# import CantoTruco

class _cantotruco:
  codigo = None

  def __init__(self, codigo):
    if not isinstance(codigo, str) :
      raise ValueError('Argumentos de tipo no permitido - debe ser str');
    self.codigo = codigo

  def codigo():
    return self.codigo

  def __eq__(self, otro):
    if isinstance(otro, _cantotruco):
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
TRUCO = _cantotruco('TRUCO')
RETRUCO = _cantotruco('RETRUCO')
VALE4 = _cantotruco('VALE4')
QUIEROTRUCO = _cantotruco('QUIERO')
NOQUIEROTRUCO = _cantotruco('NO QUIERO')
