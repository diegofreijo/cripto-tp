import sys
sys.path.append("red")
# import LogicaRed
sys.path.append("truco")
import Palo
from Carta import *
import ManoTruco

def mostrarLista(jugadas):
  i=0
  while i<len(jugadas):
    print "\t" + str(i) + "- " + str(jugadas[i])
    i=i+1
  return

cartasMano = []
cartasMano.append( Carta( 1,Palo.ESPADA ) )
cartasMano.append( Carta( 2,Palo.ESPADA ) )
cartasMano.append( Carta( 3,Palo.ESPADA ) )
cartasPie = []
cartasPie.append( Carta( 1,Palo.BASTO ) )
cartasPie.append( Carta( 2,Palo.ORO ) )
cartasPie.append( Carta( 3,Palo.ORO ) )

TrucoMano = ManoTruco.ManoTruco( cartasMano, True )
TrucoPie = ManoTruco.ManoTruco( cartasPie, False )

while (TrucoMano.terminado()!=None) or (TrucoPie.terminado()!=None):
  if TrucoMano.esMiTurno:
    jugadas = TrucoMano.jugadasPosibles()
    mostrarLista(jugadas)
    print "Elija el numero de la opcion a jugar: (empezando en 0)"
    opcionInt = int(raw_input("> "))
    opcionJugada = jugadas[opcionInt]
    print "Usted eligio jugar  ",
    print str( opcionJugada )
    TrucoMano.jugar( opcionJugada );
    print "TrucoMano.juegomio " + str(TrucoMano.juegoMio)
    print "TrucoMano.juegootro " + str(TrucoMano.juegoOtro)
    print "TrucoMano.esMiTurno "  + str(TrucoMano.esMiTurno)
    print "Trucopie.juegomio " + str(TrucoPie.juegoMio)
    print "Trucopie.juegootro " + str(TrucoPie.juegoOtro)
    print "Trucopie.esMiTurno " + str(TrucoPie.esMiTurno)
    TrucoPie.recibirJugada( opcionJugada );
    print "TrucoMano.juegomio " + str(TrucoMano.juegoMio)
    print "TrucoMano.juegootro " + str(TrucoMano.juegoOtro)
    print "TrucoMano.esMiTurno "  + str(TrucoMano.esMiTurno)
    print "Trucopie.juegomio " + str(TrucoPie.juegoMio)
    print "Trucopie.juegootro " + str(TrucoPie.juegoOtro)
    print "Trucopie.esMiTurno " + str(TrucoPie.esMiTurno)
    opcionInt = raw_input("Presione una tecla para continuar...")
  if TrucoPie.esMiTurno:
    jugadas = TrucoPie.jugadasPosibles()
    mostrarLista(jugadas)
    print "\nELIJA LA OPCION QUE JUEGA LA COMPU: (empezando en 0)"
    opcionInt = int(raw_input("> "))
    opcionJugada = jugadas[opcionInt]
    print "La compu juega  ",
    print str( opcionJugada )
    TrucoPie.jugar( opcionJugada )
    print "TrucoMano.juegomio " + str(TrucoMano.juegoMio)
    print "TrucoMano.juegootro " + str(TrucoMano.juegoOtro)
    print "TrucoMano.esMiTurno "  + str(TrucoMano.esMiTurno)
    print "Trucopie.juegomio " + str(TrucoPie.juegoMio)
    print "Trucopie.juegootro " + str(TrucoPie.juegoOtro)
    print "Trucopie.esMiTurno " + str(TrucoPie.esMiTurno)

    TrucoMano.recibirJugada( opcionJugada )
    print "TrucoMano.juegomio " + str(TrucoMano.juegoMio)
    print "TrucoMano.juegootro " + str(TrucoMano.juegoOtro)
    print "TrucoMano.esMiTurno "  + str(TrucoMano.esMiTurno)
    print "Trucopie.juegomio " + str(TrucoPie.juegoMio)
    print "Trucopie.juegootro " + str(TrucoPie.juegoOtro)
    print "Trucopie.esMiTurno " + str(TrucoPie.esMiTurno)

