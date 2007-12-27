# -*- coding: cp1252 -*-
execfile(r'..\..\setpath_viejo.py')
from Carta import *
import Canto
from ManoTruco import ManoTruco


nroTest = 0
hayErr = False

def test(obj1, obj2):
  global hayErr, nroTest
  nroTest = nroTest + 1
  if obj1 != obj2:
    print str(nroTest) + ') ERROR FATAL: se obtuvo ' + repr(obj1) + ' - se esperaba ' + repr(obj2)
    hayErr = True

def testMezclado(obj1, obj2):
  global hayErr, nroTest
  nroTest = nroTest + 1
  rv = True
  for e in obj2:
    if e not in obj1:
      rv = False
      print str(nroTest) + ') ERROR FATAL: el elemento esperado ' + repr(e) + ' no se encontro en la lista'
  if len(obj1) != len(obj2):
    rv = False
    print str(nroTest) + ') ERROR FATAL: la longitud de la lista (' + str(len(obj1)) + ') no coincide con la esperada (' + str(len(obj2)) + ')'
  if not rv:
    hayErr = True

cartasMano = []
cartasMano.append( Carta(1, Palo.BASTO) )
cartasMano.append( Carta(2, Palo.ESPADA) )
cartasMano.append( Carta(3, Palo.ESPADA) )
cartasPie = []
cartasPie.append( Carta(1, Palo.ESPADA) )
cartasPie.append( Carta(2, Palo.ORO) )
cartasPie.append( Carta(3, Palo.ORO) )

# las jugadas que se espera tener
jugadasMano = cartasMano + [Canto.Canto(Canto.AL_MAZO)]
jugadasPie = cartasPie + [Canto.Canto(Canto.AL_MAZO)]


# 0) Inicio juego
print 'TEST 0'
nroTest = 0
hayErr = False

trucoMano = ManoTruco(cartasMano, True)
trucoPie = ManoTruco(cartasPie, False)

# Tests inicio juego
test(trucoMano.terminado(), False)

test(trucoPie.terminado(), False)

test(trucoMano.turnoDeJuego(), True)

test(trucoPie.turnoDeJuego(), False)

testMezclado(trucoMano.jugadasPosibles(), jugadasMano)

testMezclado(trucoPie.jugadasPosibles(), jugadasPie)

test(trucoMano.ganeYo(), False)

test(trucoPie.ganeYo(), False)

test(trucoMano.recibirJugada(jugadasPie[0]), False)

test(trucoPie.jugar(jugadasPie[0]), False)

if hayErr:
  raise ValueError('ERRORES ENCONTRADOS EN TEST PASO 0')



# 1) Jugada
print 'TEST 1'
nroTest = 0

test(trucoMano.jugar(jugadasMano[0]), True)

test(trucoPie.recibirJugada(jugadasMano[0]), True)

test(trucoMano.terminado(), False)

test(trucoPie.terminado(), False)

test(trucoMano.turnoDeJuego(), False)

test(trucoPie.turnoDeJuego(), True)

test(trucoMano.jugar(jugadasMano[0]), False)

test(trucoPie.recibirJugada(jugadasMano[0]), False)

jugadasMano.remove(jugadasMano[0])

testMezclado(trucoMano.jugadasPosibles(), jugadasMano)

testMezclado(trucoPie.jugadasPosibles(), jugadasPie)

test(trucoMano.ganeYo(), False)

test(trucoPie.ganeYo(), False)

if hayErr:
  raise ValueError('ERRORES ENCONTRADOS EN TEST PASO 1')



# 2) Jugada
print 'TEST 2'
nroTest = 0

test(trucoMano.recibirJugada(jugadasPie[0]), True)

test(trucoPie.jugar(jugadasPie[0]), True) # el ancho de espadas mata al ancho de bastos

test(trucoMano.terminado(), False)

test(trucoPie.terminado(), False)

test(trucoMano.turnoDeJuego(), False)

test(trucoPie.turnoDeJuego(), True)

test(trucoPie.recibirJugada(jugadasMano[0]), False) # debe fallar, porque el pie tiene el turno de jugar

test(trucoMano.jugar(jugadasMano[0]), False)

jugadasPie.remove(jugadasPie[0])

testMezclado(trucoMano.jugadasPosibles(), jugadasMano)

testMezclado(trucoPie.jugadasPosibles(), jugadasPie)

test(trucoMano.ganeYo(), False)

test(trucoPie.ganeYo(), False)

if hayErr:
  raise ValueError('ERRORES ENCONTRADOS EN TEST PASO 2')




print 'Todos los tests se completaron con exito.'
