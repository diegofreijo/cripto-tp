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
    if isinstance(otro,_cantoEnvido):   # antes decis issubclass me parece que es un error
      return (self.codigo == otro.codigo )
    raise ValueError('Argumento de tipo no permitido: ')

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
    if isinstance(codigo, str) and isinstance(tantos, int):
      self.codigo = codigo
      self.tantos = tantos
    else:
      raise ValueError('Argumentos de tipo no permitido - deben ser str, int.');

  def __str__(self):
    return self.codigo + ':' #+ repr(self.tantos)

  def __repr__(self):
    return 'CantoEnvido.Tantos('+repr(self.tantos)+')'


# pseudo constantes
ENVIDONOCANTADO=_cantoEnvido('NADA')
ENVIDO = _cantoEnvido('Envido')
ENVIDOENVIDO = _cantoEnvido('Envido Envido')
REALENVIDO = _cantoEnvido('Real Envido')
FALTAENVIDO = _cantoEnvido('Falta Envido')
QUIEROENVIDO = _cantoEnvido('Quiero')
NOQUIEROENVIDO = _cantoEnvido('No quiero')
NOTENGOTANTOS=_cantoEnvidoTantos('TANTOS')

# pseudo constructor
def Tantos(puntos):
  return puntos.tantos
#  return _cantoEnvidoTantos('Tantos', tantos)


CANTOS_ENVIDO = [ENVIDONOCANTADO,ENVIDO, ENVIDOENVIDO, REALENVIDO, FALTAENVIDO]

def cantosMayores(canto):
  i = None
  if canto==ENVIDONOCANTADO:
    i=1
  elif canto == ENVIDO:
    i = 2
  elif canto == ENVIDOENVIDO:
    i = 3
  elif canto == REALENVIDO:
    i = 4
  elif canto == FALTAENVIDO:
    i = 5
  else:
    raise ValueError('No es un canto de envido: ' + repr(canto))
  return CANTOS_ENVIDO[i:]
