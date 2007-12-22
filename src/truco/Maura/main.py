import sys
sys.path.append("red")
# import LogicaRed
sys.path.append("truco")
import Palo
from Carta import *
from CantoEnvido import *
from CantoEnvido import Tantos
from CantoEnvido import _cantoEnvidoTantos
from CantoTruco import *
from ManoTruco import *
from PieTruco import *

cartasMano = []
cartasMano.append( Carta( 1,Palo.ESPADA ) )
cartasMano.append( Carta( 2,Palo.ESPADA ) )
cartasMano.append( Carta( 3,Palo.ESPADA ) )
cartasPie = []
cartasPie.append( Carta( 1,Palo.BASTO ) )
cartasPie.append( Carta( 2,Palo.ORO ) )
cartasPie.append( Carta( 3,Palo.ORO ) )

TrucoMano = ManoTruco( cartasMano, True )
TrucoPie = ManoTruco( cartasPie, False )

while (TrucoMano.terminado()!=None) or (TrucoPie.terminado()!=None):
  if TrucoMano.esMiTurno:
    jugadas = TrucoMano.jugadasPosibles()
    print str( jugadas )
    print "Elija el numero de la opcion a jugar: (empezando en 0)"
    opcionInt = int(raw_input(">"))
    opcionJugada = jugadas[opcionInt]
    TrucoMano.jugar( opcionJugada );
    TrucoPie.recibirJugada( opcionJugada );
    print "Usted eligio jugar  ",
    print str( opcionJugada )
    print "TrucoMano.juegomio " + str(TrucoMano.juegoMio)
    print "TrucoMano.juegootro " + str(TrucoMano.juegoOtro)
    print "TrucoMano.esMiTurno "  + str(TrucoMano.esMiTurno)
    print "Trucopie.juegomio " + str(TrucoPie.juegoMio)
    print "Trucopie.juegootro " + str(TrucoPie.juegoOtro)
    print "Trucopie.esMiTurno " + str(TrucoPie.esMiTurno)
    opcionInt = raw_input("ghehhtrheth")
  if TrucoPie.esMiTurno:
    jugadas = TrucoPie.jugadasPosibles()
    print str( jugadas )
    print "\nELIJA LA OPCION QUE JUEGA LA COMPU: (empezando en 0)"
    opcionInt = int(raw_input(">"))
    opcionJugada = jugadas[opcionInt]
    print "La compu juega  ",
    print str( opcionJugada )
    TrucoPie.jugar( opcionJugada )
    TrucoMano.recibirJugada( opcionJugada )
    print "TrucoMano.juegomio " + str(TrucoMano.juegoMio)
    print "TrucoMano.juegootro " + str(TrucoMano.juegoOtro)
    print "TrucoMano.esMiTurno "  + str(TrucoMano.esMiTurno)
    print "Trucopie.juegomio " + str(TrucoPie.juegoMio)
    print "Trucopie.juegootro " + str(TrucoPie.juegoOtro)
    print "Trucopie.esMiTurno " + str(TrucoPie.esMiTurno)
