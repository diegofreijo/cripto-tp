import sys
sys.path.append("red")
# import LogicaRed
sys.path.append("truco")
import Palo
import Carta
from CantoEnvido import *
from CantoTruco import *
import ManoTruco

cartasMano = []
cartasMano.append( Carta.Carta( 1,Palo.ESPADA ) )
cartasMano.append( Carta.Carta( 2,Palo.ESPADA ) )
cartasMano.append( Carta.Carta( 3,Palo.ESPADA ) )
cartasPie = []
cartasPie.append( Carta.Carta( 1,Palo.BASTO ) )
cartasPie.append( Carta.Carta( 2,Palo.ORO ) )
cartasPie.append( Carta.Carta( 3,Palo.ORO ) )

TrucoMano = ManoTruco.ManoTruco( cartasMano, True )
TrucoPie = ManoTruco.ManoTruco( cartasPie, False )

while (not TrucoMano.terminado()) or (not TrucoPie.terminado()):
  if TrucoMano.esMiTurno:
    jugadas = TrucoMano.jugadasPosibles()
    print str( jugadas )
    print "Elija el numero de la opcion a jugar: (empezando en 0)"
    opcionInt = int(raw_input(">"))
    opcionJugada = jugadas[opcionInt]
    TrucoMano.jugar( opcionJugada );
    TrucoPie.recibirJugada( opcionJugada );
    print "Usted eligio jugar "
    print str( opcionJugada )
    #opcionInt = int(raw_input(">"))
  if TrucoPie.esMiTurno:
    jugadas = TrucoPie.jugadasPosibles()
    print str( jugadas )
    print "ELIJA LA OPCION QUE JUEGA LA COMPU: (empezando en 0)"
    opcionInt = int(raw_input(">"))
    opcionJugada = jugadas[opcionInt]
    TrucoPie.jugar( opcionjugada )
    TrucoMano.recibirJugada( opcionjugada )
    print "La compu juega "
    print str( opcionjugada )
    print "\n TrucoMano.juegomio " + str(TrucoMano.juegoMio)
    print "\n TrucoMano.juegootro " + str(TrucoMano.juegoOtro)
    print "\n TrucoMano.esMiTurno "  + str(TrucoMano.esMiTurno)
    print "\n Trucopie.juegomio " + str(TrucoPie.juegoMio)
    print "\n Trucopie.juegootro " + str(TrucoPie.juegoOtro)
    print "\n Trucopie.esMiTurno " + str(TrucoPie.esMiTurno)
