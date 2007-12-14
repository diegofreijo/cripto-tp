# TP
# Matias
# Uso:
# import CantoEnvido

class _cantoenvido:
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
    if issubclass(otro, _cantoenvido):
      return (self.codigo == otro.codigo and self.valor == otro.valor)
    raise ValueError('Argumento de tipo no permitido: ' + str(otro))

  def __ne__(self, otro):
    return not (self == otro)

  def __hash__(self):
    return self.codigo.__hash__()

  def __str__(self):
    return self.codigo

  def __repr__(self):
    return 'CantoEnvido('+repr(self.codigo)+', '+repr(self.valor)+')'

class _cantoenvidotantos(_cantoenvido):
  tantos = 0

  def __init__(self, codigo, valor, tantos = 0):
    if not isinstance(codigo, str) or not isinstance(valor, int) or not isinstance(tantos, int):
      raise ValueError('Argumentos de tipo no permitido - deben ser str, int, int.');
    self.codigo = codigo
    self.valor = valor
    self.tantos = tantos

  def __str__(self):
    return self.codigo + ':' + repr(self.tantos)

  def __repr__(self):
    return 'CantoEnvido.Tantos('+repr(self.tantos)+')'


# pseudo constantes
ENVIDO = _cantoenvido('Envido', 1)
ENVIDOENVIDO = _cantoenvido('Envido Envido', 2)
REALENVIDO = _cantoenvido('Real Envido', 3)
FALTAENVIDO = _cantoenvido('Falta Envido', 4)
QUIERO = _cantoenvido('Quiero', 0)
NOQUIERO = _cantoenvido('No quiero', 0)

# pseudo constructor
def Tantos(tantos):
  return _cantoenvidotantos('Tantos', 0, tantos)

