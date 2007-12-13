# TP
# Matias
# Uso:
# import CantoTruco

class _cantotruco:
  codigo = None
  valor = 0

  def __init__(self, codigo, valor):
    if not isinstance(codigo, str) or not isinstance(valor, int):
      raise ValueError('Argumentos de tipo no permitido - deben ser str e int.');
    self.codigo = codigo
    self.valor = valor

  def codigo():
    return self.codigo

  def valor():
    return self.valor

  def __eq__(self, otro):
    if isinstance(otro, _cantotruco):
      return (self.codigo == otro.codigo and self.valor == otro.valor)
    raise ValueError('Argumento de tipo no permitido: ' + str(otro))

  def __ne__(self, otro):
    return not (self == otro)

  def __hash__(self):
    return self.codigo.__hash__()

  def __str__(self):
    return self.codigo

  def __repr__(self):
    return 'CantoTruco('+repr(self.codigo)+', '+repr(self.valor)+')'

# pseudo constantes
TRUCO = _cantotruco('TRUCO', 1)
RETRUCO = _cantotruco('RETRUCO', 2)
VALE4 = _cantotruco('VALE4', 4)
QUIERO = _cantotruco('QUIERO', 0)
NOQUIERO = _cantotruco('NOQUIERO', 0)
