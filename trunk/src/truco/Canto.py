# TP
# Matias
# Uso:
# import Canto
# Luego usar como un tipo enumerado: Canto.ME_VOY_AL_MAZO, etc.

TRUCO = "Truco"
AL_MAZO = "Me voy al mazo"
QUIERO = "Quiero"
NO_QUIERO = "No Quiero"
CUANTO_TENGO_DE_ENVIDO = "Yo tengo: "

class Canto:
  tipoCanto = None
  numeroDelEnvido = 0


  def __init__(self, queCanta, cuantoCanta):
    self.tipoCanto = queCanta
    self.numeroDelEnvido = cuantoCanta

  def __init__(self, queCanta):
    self.tipoCanto = queCanta
    self.numeroDelEnvido = 0

  def __eq__(self, otra):
    if isinstance(otra, Canto):
      return (self.tipoCanto == otra.tipoCanto and self.numeroDelEnvido == otra.numeroDelEnvido)
    raise ValueError('Argumento de tipo no permitido: ' + str(otra))

  def __ne__(self, otra):
    return not (self == otra)

  def __hash__(self):
    return self.tipoCanto.__hash__() ^ self.numeroDelEnvido.__hash__()

  def __str__(self):
    if self.tipoCanto == CUANTO_TENGO_DE_ENVIDO:
      return 'Canto (' + str(self.tipoCanto) + ', ' +str(self.numeroDelEnvido) + ')'
    return 'Canto (' + str(self.tipoCanto) + ') '

  def __repr__(self):
    if self.tipoCanto == CUANTO_TENGO_DE_ENVIDO:
      return 'Canto (' + repr(self.tipoCanto) + ', ' +repr(self.numeroDelEnvido) + ')'
    return 'Canto (' + repr(self.tipoCanto) + ') '

