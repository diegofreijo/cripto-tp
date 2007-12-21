# TP
# Matias
# Uso:
# import CantoEnvido

class _cantoEnvido:
  codigo = None
  
  def __init__(self, codigo):
    if not isinstance(codigo,str):
     raise ValueError('Argumentos de tipo no permitido - deben ser str e int.');
    self.codigo = codigo

  def codigo():
    return self.codigo

  def __eq__(self, otro):
    if issubclass(otro, cantoenvido):
      return (self.codigo == otro.codigo )
    raise ValueError('Argumento de tipo no permitido: ' + str(otro))

  def __ne__(self, otro):
    return not (self == otro)

  def __hash__(self):
    return self.codigo.__hash__()

  def __str__(self):
    return self.codigo

  def __repr__(self):
    return 'CantoEnvido('+repr(self.codigo)+')'

class _cantoEnvidoTantos(_cantoEnvido):
  tantos = 0

  def __init__(self, codigo,tantos = 0):
    if not isinstance(codigo, str) or not isinstance(tantos, int):
      raise ValueError('Argumentos de tipo no permitido - deben ser str, int.');
    self.codigo = codigo
    self.tantos = tantos

  def __str__(self):
    return self.codigo + ':' + repr(self.tantos)

  def __repr__(self):
    return 'CantoEnvido.Tantos('+repr(self.tantos)+')'


# pseudo constantes
ENVIDO = _cantoEnvido('Envido')
ENVIDOENVIDO = _cantoEnvido('Envido Envido')
REALENVIDO = _cantoEnvido('Real Envido')
FALTAENVIDO = _cantoEnvido('Falta Envido')
QUIEROENVIDO = _cantoEnvido('Quiero')
NOQUIEROENVIDO = _cantoEnvido('No quiero')

# pseudo constructor
def Tantos(tantos):
  return _cantoEnvidoTantos('Tantos', tantos)


CANTOS_ENVIDO = [ENVIDO, ENVIDOENVIDO, REALENVIDO, FALTAENVIDO]

def cantosMayores(canto):
  i = None
  if canto == ENVIDO:
    i = 1
  elif canto == ENVIDOENVIDO:
    i = 2
  elif canto == REALENVIDO:
    i = 3
  elif canto == FALTAENVIDO:
    i = 4
  else:
    raise ValueError('No es un canto de envido: ' + repr(canto))
  return CANTOS_ENVIDO[i:]
