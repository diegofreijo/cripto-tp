import sys
sys.path.append("red")
# import LogicaRed
sys.path.append("truco")

import Palo
from Carta import *
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

TrucoMano =ManoTruco( cartasMano, True )
TrucoPie = PieTruco( cartasPie, False )

print "\n TrucoMano.juegomio " + str(TrucoMano.juegoMio)
print "\n TrucoMano.juegootro " + str(TrucoMano.juegoOtro)
print "\n TrucoMano.esMiTurno "  + str(TrucoMano.esMiTurno)
print "\n Trucopie.juegomio " + str(TrucoPie.juegoMio)
print "\n Trucopie.juegootro " + str(TrucoPie.juegoOtro)
print "\n Trucopie.esMiTurno " + str(TrucoPie.esMiTurno)
        
while TrucoMano.terminado() != None or TrucoPie.terminado() != None:
    salida=TrucoMano.esMiTurno
    print "esMiTurno de Mano" + str(salida)
    if TrucoMano.esMiTurno:
        jugadas = TrucoMano.jugadasPosibles()
        print str( jugadas )
        print "\nElija el numero de la opcion a jugar: (empezando en 0)"
        opcionInt = int(raw_input("Ingrese la opcion (empezando por 0) "))
        opcionJugada = jugadas[opcionInt]
        TrucoMano.jugar( opcionJugada );
        print "\nUsted eligio jugar ",
        print str( opcionJugada )
        TrucoPie.recibirJugada( opcionJugada );
    salida=TrucoPie.esMiTurno
    print "esMiTurno de Pie" + str(salida)
    if TrucoPie.esMiTurno:
        jugadas = TrucoPie.jugadasPosibles()
        jugadaElegida = jugadas[0]
        TrucoPie.jugar( jugadaElegida)
        TrucoMano.recibirJugada( jugadaElegida)
        print "\n\nLa compu juega "
        print str( jugadaElegida )
    print "\nLoopeando..."
    
    print "\n TrucoMano.juegomio " + str(TrucoMano.juegoMio)
    print "\n TrucoMano.juegootro " + str(TrucoMano.juegoOtro)
    print "\n TrucoMano.esMiTurno "  + str(TrucoMano.esMiTurno)
    print "\n Trucopie.juegomio " + str(TrucoPie.juegoMio)
    print "\n Trucopie.juegootro " + str(TrucoPie.juegoOtro)
    print "\n Trucopie.esMiTurno " + str(TrucoPie.esMiTurno)
