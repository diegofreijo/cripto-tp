# -*- coding: cp1252 -*-
from Cartas import *

ESTADOENVIDO_NOCANTADO_ABIERTO = 0
ESTADOENVIDO_CANTADO_ABIERTO = 1
ESTADOENVIDO_CANTADO_NOQUERIDO = 2
ESTADOENVIDO_CANTADO_QUERIDO = 3
ESTADOENVIDO_NOCANTADO_CERRADO = 4

ESTADOTRUCO_NOCANTADO = 0
ESTADOTRUCO_CANTADO_ABIERTO = 1
ESTADOTRUCO_CANTADO_NOQUERIDO = 2
ESTADOTRUCO_CANTADO_QUERIDO = 3

class ManoTruco:
  # variables de instancia

  def soyMano(self):
    """True si soy mano (si tengo que bajar carta), False si debe bajar mi
    contrincante, None si el juego esta terminado"""
    return self._soyMano

  def manoActual(self):
    """Mano actual, de 1 a 3. None si el juego esta terminado"""
    return self._manoActual

  def terminado(self):
    """Si el juego esta terminado o no
    NOTA: tal vez haya que definir mas de dos estados del juego... por ejemplo
    para el final, cuando ya no se puede jugar pero hay que esperar las
    cartas que quiera mostrar el contrincante.
    """
    return self._manoActual == None

  def estadoEnvido(self):
    """Devolver el estado del envido:
    0 == no cantado; abierto [abierto quiere decir que puede cantarse Envido]
    1 == cantado; abierto [puede cantarse Falta Envido, etc]
    2 == cantado; no querido
    3 == cantado; querido
    4 == no cantado; cerrado [paso la primer mano sin que se cante Envido]
    """
    return self._estadoEnvido

  def estadoEnvidoQuerido(self):
    """Devolver el estado del envido querido:
    0 == no aplica (porque estadoEnvido() != 3)
    1 == la mano debe cantar los tantos, ya sea yo o el otro
    2 == el contrario de la mano debe cantar los tantos, ya sea yo o el otro
      "Son buenas" puede representarse con un canto de CERO TANTOS
    3 == los tantos fueron intercambiados
    """
    return self._estadoEnvidoQuerido

  def mayorEnvido(self):
    """Devolver el mayor envido que se haya cantado:
    None si no hubo canto de envido en el juego
    o el CantoEnvido mayor"""
    return self._mayorEnvido

  def quienCantoNoQuieroEnvido(self):
    """True quiere decir YO"""
    #    return self._quienNoQuieroEnvido
    if self.estadoEnvido() != ESTADOENVIDO_CANTADO_NOQUERIDO: # no querido
      return None
    return (CantoEnvido.NO_QUERIDO in self.cantosEnvidoCantados())

  def cantosEnvidoCantados(self):
    """Los cantos que hice yo"""
    return self._cantosEnvidoCantados

  def cantosEnvidoRecibidos(self):
    """Los cantos que recibí de mi contrincante"""
    return self._cantosEnvidoRecibidos

  def turnoCantoEnvido(self):
    """A quien le toca cantar por envido. True==yo, False==mi contrincante, None==no aplica"""
    if self.estadoEnvido() != ESTADOENVIDO_CANTADO_ABIERTO:
      return None
    return (mayorEnvido() in self.cantosEnvidoRecibidos()) # si el mayor canto lo hizo mi contrincante, me toca a mí

  def estadoTruco(self):
    """
    0 = no cantado
    1 = cantado; abierto
    2 = cantado; no querido
    3 = cantado y querido
    """
    return self._estadoTruco

  def quienCantoNoQuieroTruco(self):
    """True quiere decir YO"""
    #return self._quienNoQuieroTruco
    if self.estadoTruco() != ESTADOTRUCO_CANTADO_NOQUERIDO:
      return None
    return (CantoTruco.NO_QUERIDO in self.cantosTrucoCantados())

  def cantosTrucoCantados(self):
    """Devolver una lista de los cantos propios por Truco, incluyendo el
    Quiero o No Quiero"""
    return self._cantosTrucoCantados

  def cantosTrucoRecibidos(self):
    """Devolver una lista de los cantos de Truco del contricante, incluyendo
    el Quiero o No Quiero"""
    return self._cantosTrucoRecibidos

  def turnoDeJuego(self):
    """A quién le toca jugar. Notar que NO ES LO MISMO que soyMano(),
    porque soyMano() es a quién le toca bajar una carta y turnoDeJuego()
    es quién debe bajar carta o cantar o responder un canto.
    Valores: True (me toca a mí), False (a mi contrincante), None
    (ya no se pueden hacer jugadas)"""
    # si hay envido pendiente, el turno le toca al que debe responder
    rv = self.turnoCantoEnvido()
    if rv != None: return rv
    # etcetera, siganlo...

  def jugadasPosibles(self):
    """EN DUDA"""

  def jugadasPosiblesContrario(self):
    """EN DUDA"""

  def cantarTruco(self, canto):
    self.jugar([canto])

  def recibirCantoTruco(self, canto):
    self.recibirJugada([canto])

  def bajarCarta(self, carta):
    self.jugar([carta])

  def recibirBajadaCarta(self, carta):
    self.recibirJugada([carta])

  def jugar(self, jugadas):
    """realizar una lista de jugadas (o sea, Cantos y/o Cartas) que hace esta parte"""

  def recibirJugada(self, jugadas):
    """recibir las jugadas que realiza la contraparte (Cantos y/o Cartas)
    que hace mi contrincante"""

  def puntaje(self):
    """mi puntaje"""

  def puntajeContrincante(self):
    """puntaje de mi contrincante"""

  def faltaEnviarFinJuego(self):
    """faltan mostrar mis cartas, si decido mostrarlas"""

  def faltaRecibirFinJuego(self):
    """falta que mi contrincante muestre las cartas, si así lo decide"""

  def finJuego(self, cartasAMostrar):
    """Irse al mazo mostrando las cartas en cartasAMostrar"""

  def recibirFinJuego(self, cartasMostradas):
    """Mi contrincante cierra el juego mostrando las cartas en cartasMostradas"""




