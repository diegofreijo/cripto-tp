# TP
# Matias
# Uso:
# import CantoEnvido

class cantoenvido:
  codigo = None
  valor = 0
  opciones=['ENVIDO','ENVIDO ENVIDO','REAL ENVIDO','FALTA ENVIDO']

  def __init__(self, codigo, valor):
#    if not isinstance(codigo,str) or not isNumberType(valor):
#     raise ValueError('Argumentos de tipo no permitido - deben ser str e int.');
    self.codigo = codigo
    self.valor = valor

  def codigo():
    return self.codigo

  def valor():
    return self.valor

  def __eq__(self, otro):
    if issubclass(otro, cantoenvido):
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

# pseudo constantes

#NOCANTADO=cantoenvido('',0)
ENVIDO =cantoenvido('Envido', 1)
ENVIDOENVIDO = cantoenvido('Envido Envido', 2)
REALENVIDO = cantoenvido('Real Envido', 3)
FALTAENVIDO = cantoenvido('Falta Envido', 4)
QUIEROENVIDO = cantoenvido('Quiero', 5)
NOQUIEROENVIDO = cantoenvido('No quiero', 5)

#QUIERO = _cantoenvido('Quiero', 0)
#NOQUIERO = _cantoenvido('No quiero', 0)
