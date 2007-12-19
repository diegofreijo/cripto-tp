import Palo
import Carta
import Canto

class ManoTruco:

  def __init__(self, cartasIniciales, soyMano):
    self._soyMano = soyMano
    self._cartasQueTengo = cartasIniciales

    # inicializacion del estado
    self._esMiTurno = soyMano
    self._fuiManoEnSubManoActual = soyMano
    self._fuiManoEnSubManoActual = soyMano
    self._subManoActual = 1
    self._vieneParda = False


  def terminado(self):
    """Si el juego esta terminado o no"""
    return self._subManoActual == 0

  def turnoDeJuego(self):
    """true si me toca a mi. False si ya terminamos o si le toca (cantar o jugar o responder canto) al otro"""
    if self.terminado():
      return False
    else:
      return self._esMiTurno

  def jugadasPosibles(self):
    jugadas = list(self._cartasQueTengo)
    jugadas.append( Canto.Canto( Canto.AL_MAZO ) )
    return jugadas

  def jugar( self, laJugada ):
    """realizar una lista de jugadas (o sea, Cantos y/o Cartas) que hace esta parte"""
    # si me voy al mazo, perdi, y es el fin del juego
    # extraigo carta de la jugada y la guardo como _juegoMio
    # sacar carta jugada de la lista _cartasQueTengo
    # si no _fuiManoEnSubManoActual, termina una submano
    if not self._esMiTurno:
      return False

    if isinstance( laJugada, Canto.Canto ):
      if laJugada.tipoCanto == Canto.AL_MAZO:
        # perdi
        self._subManoActual = 0
        self._ganeYo = False
        return
      return

    # asumo que  laJugada es una carta
    self._juegoMio = laJugada
    self._cartasQueTengo.remove( self._juegoMio ) # ojo que aca no estoy validando que la carta sea una de las mias!
    if not self._fuiManoEnSubManoActual:
      self._terminaSubMano()
    else:
      # si _fuiManoEnSubManoActual, le cambia el turno (le toca al otro) y nada mas
      self._esMiTurno = not self._esMiTurno
    return True

  def recibirJugada( self, laJugada ):
    if self._esMiTurno:
      return False

    if isinstance( laJugada, Canto.Canto ):
      if laJugada.tipoCanto == Canto.AL_MAZO:
        # gane
        self._subManoActual = 0
        self._ganeYo = True
        return
      return

    # asumo que la jugada es una carta
    self._juegoOtro = laJugada
    if self._fuiManoEnSubManoActual:
      self._terminaSubMano()
    else:
      # si !_fuiManoEnSubManoActual, le cambia el turno (le toca al otro) y nada mas
      self._esMiTurno = not self._esMiTurno
    return True

  def ganeYo( self ):
    if not self.terminado():
      return False
    return self._ganeYo

  _soyMano = None # esta en 1 si es el servidor, si no, 0
  _ganeYo = None
  _cartasQueTengo = None # una lista que contiene las posibles cartas a jugar. Cuando se juega una, se la saca de la lista
  _subManoActual = None # numero de mano que se esta jugando 1,2,3, 0 si ya termino y None si no empezo
  _esMiTurno = False # vale True si me toca jugar o si me llega un canto del otro lado y tengo que responder
  _vieneParda = False # vale True si el que mata gana
  _ganePrimera = False
  _fuiManoEnSubManoActual = None
  _juegoMio = None
  _juegoOtro = None

  def valorRelativo( self, carta ):
    if carta.numero == 4:
      return 0
    if carta.numero == 5:
      return 1
    if carta.numero == 6:
      return 2
    if carta.numero == 7 and ( carta.esCopa() or carta.esBasto() ):
      return 3
    if carta.numero == 10:
      return 4
    if carta.numero == 11:
      return 5
    if carta.numero == 12:
      return 6
    if carta.numero == 1 and ( carta.esCopa() or carta.esOro() ):
      return 7
    if carta.numero == 2:
      return 8
    if carta.numero == 3:
      return 9
    if carta.numero == 7 and carta.esOro():
      return 10
    if carta.numero == 7 and carta.esEspada():
      return 11
    if carta.numero == 1 and carta.esBasto():
      return 12
    if carta.numero == 1 and carta.esEspada():
      return 13
    return -1

  def mata( self, carta1, carta2 ):
    return self.valorRelativo( carta1 ) > self.valorRelativo( carta2 )

  def _terminaSubMano( self ):
    #   el que mata, sigue jugando
    #   si parda la primera, sigue la mano
    #   si parda la segunda, gana la primera. Si parda la primera sigue la mano
    #   si juego la tercera, y no _fuiManoEnSubManoActual, entonces es el fin del juego
    if self.mata( self._juegoMio, self._juegoOtro ):
      if self._subManoActual == 1:
        self._ganePrimera = True
      if self._vieneParda or self._subManoActual == 3 or ( self._subManoActual == 2 and self._ganePrimera ):
        # gane
        self._subManoActual = 0
        self._ganeYo = True
        return
      self._esMiTurno = True
    else:
      if self.mata( self._juegoOtro, self._juegoMio ):
        if self._subManoActual == 1:
          self._ganePrimera = False
        if self._vieneParda or self._subManoActual == 3 or ( self._subManoActual == 2 and not self._ganePrimera ):
          # perdi
          self._subManoActual = 0
          self._ganeYo = False
          return;
        self._esMiTurno = False
      else:
        self._esMiTurno = self._soyMano # parda! sigue la mano
        if self._subManoActual == 3:
          # todo parda! gana la mano!
          self._subManoActual = 0
          self._ganeYo = self._soyMano
          return
        if self._subManoActual == 2:
          # si parda la segunda, gana el que hizo primera
          # salvo que la primera haya sido parda tambien...
          if not self._vieneParda:
            # gana el que hizo primera
            self._subManoActual = 0
            self._ganeYo = self._ganePrimera
            return
        self._vieneParda = True
    self._subManoActual = self._subManoActual + 1
    self._fuiManoEnSubManoActual = self._esMiTurno
    return
