# -*- coding: cp1252 -*-
from Carta import *

class ManoTruco:
  # Pseudo-constantes

  # variables de instancia
  _soyMano = None
  _cartasQueTengo = None
  _subManoActual = None
  _fuiManoEnSubManoActual = None
  _esMiTurno = None
  _cartaMiaEnSubManoActual = None
  _cartaContricanteEnSubManoActual = None

  def __init__(self, cartasIniciales, soyMano):
    self._soyMano = soyMano
    self._cartasQueTengo = cartasIniciales

    # inicializacion del estado
    self._manoActual = 1
    self._esMiTurno = soyMano
    self._fuiManoEnSubManOActual = soyMano

  def soyMano(self):
    """True si soy mano (no soy pie, reparti yo, y fui mano en la primera submano), False si no."""
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


  def turnoDeJuego(self):
    """A quién le toca jugar. Notar que NO ES LO MISMO que soyMano()"""
    return self._esMiTurno
    
  def jugadasPosibles(self):
    # esto seria: for each _cartasQueTengo armar una jugada que sea poner esa carta y agregarla a una lista, y retornar esa lista
    return self._cartasQueTengo

  def jugar(self, jugada):
    """realizar una lista de jugadas (o sea, Cantos y/o Cartas) que hace esta parte"""
    # si me voy al mazo, perdi, y es el fin del juego
    # extraigo carta de la jugada y la guardo como _cartaMiaEnSubManoActual
    # sacar carta jugada de la lista _cartasQueTengo
    # si no _fuiManoEnSubManoActual, termina una submano
    if not self._fuiManoEnSubManoActual:
      _terminaSubMano(self)
    else:
      # si _fuiManoEnSubManoActual, le cambia el turno (le toca al otro) y nada mas
      self._esMiTurno = not self._esMiTurno

  def recibirJugada(self, jugada):
    """recibir las jugadas que realiza la contraparte (Cantos y/o Cartas)
    que hace mi contrincante"""
    # si se fue al mazo, perdio y es el fin del juego
    # extraigo carta de la jugada que recibo y la guardo como _cartaContricanteEnSubManoActual
    # si _fuiManoEnSubManoActual, termina una submano
    if self._fuiManoEnSubManoActual:
      _terminaSubMano(self)
    else:
      # si no _fuiManoEnSubManoActual, le cambia el turno (me toca a mi) y nada mas
      self._esMiTurno = not self._esMiTurno

  def _terminaSubMano(self):
    #   el que mata, sigue jugando
    #   si parda la primera, sigue la mano
    #   si parda la segunda, sigue el que hizo primera, si parda la primera, sigue la mano
    #   si juego la tercera, y no _fuiManoEnSubManoActual, entonces es el fin del juego

    # reseteo variables de subMano
    _cartaMiaEnSubManoActual = None
    _cartaContricanteEnSubManoActual = None

  def puntaje(self):
    """mi puntaje"""

  def puntajeContrincante(self):
    """puntaje de mi contrincante"""

  def recibirFinJuego(self, cartasMostradas):
    """Mi contrincante cierra el juego mostrando las cartas en cartasMostradas"""