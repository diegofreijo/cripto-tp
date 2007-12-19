import sys
sys.path.append("red")
# import LogicaRed
sys.path.append("truco")
import Palo
import Carta
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
  if TrucoMano.turnoDeJuego():
    jugadas = TrucoMano.jugadasPosibles()
    print str( jugadas )
    print "Elija el numero de la carta a jugar: (entre 0 y 2)"
    opcionInt = int(raw_input(">"))
    opcionJugada = jugadas[opcionInt]
    TrucoMano.jugar( opcionJugada );
    TrucoPie.recibirJugada( opcionJugada );
    print "Usted eligio jugar la carta"
    print str( opcionJugada )
  if TrucoPie.turnoDeJuego():
    jugadas = TrucoPie.jugadasPosibles()
    jugadaElegida = jugadas[0]
    TrucoPie.jugar( jugadaElegida )
    TrucoMano.recibirJugada( jugadaElegida )
    print "La compu juega el "
    print str( jugadaElegida )

if TrucoMano.ganeYo():
  print "bien, ganaste!"
else:
  print "looser!"
