# TP
# Matias
# Uso:
# import Canto
# Luego usar como un tipo enumerado: Canto.AL_MAZO, etc.

TRUCO = "Truco"
AL_MAZO = "Me voy al mazo"
QUIERO = "Quiero"
NO_QUIERO = "No Quiero"
CUANTO_TENGO_DE_ENVIDO = "Yo tengo: "

class Canto:
  tipoCanto = None
  numeroDelEnvido = 0


  def __init__(self, queCanta, cuantoCanta = 0):
    if isinstance(queCanta, Canto):
      self.tipoCanto = queCanta.tipoCanto
      self.cuantoCanta = queCanta.cuantoCanta
      if cuantoCanta > 0: self.cuantoCanta = cuantoCanta
    else:
      self.tipoCanto = queCanta
      self.numeroDelEnvido = cuantoCanta

  def __eq__(self, otra):
    if not isinstance(otra, Canto): return False
    return (self.tipoCanto == otra.tipoCanto and self.numeroDelEnvido == otra.numeroDelEnvido)

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

