import sys
#sys.path.append("red")
# import LogicaRed
#sys.path.append("truco")
import Palo
from Carta import *
import ManoTruco
from Score import _Score

Score=_Score()

def mostrarLista(jugadas):
  i=0
  while i<len(jugadas):
    print "\t" + str(i) + "- " + str(jugadas[i])
    i=i+1
  return

while Score.partidoGanado()==0:
  cartasMano = []
  cartasMano.append( Carta( 1,Palo.ESPADA ) )
  cartasMano.append( Carta( 2,Palo.ESPADA ) )
  cartasMano.append( Carta( 3,Palo.BASTO ) )
  cartasPie = []
  cartasPie.append( Carta( 1,Palo.BASTO ) )
  cartasPie.append( Carta( 2,Palo.ORO ) )
  cartasPie.append( Carta( 3,Palo.ORO ) )

  TrucoMano = ManoTruco.ManoTruco( cartasMano, True )
  TrucoPie = ManoTruco.ManoTruco( cartasPie, False )

  while TrucoMano.terminado()!=None or TrucoPie.terminado()!=None:
    if TrucoMano.esMiTurno:
      jugadas=[]
      jugadas = TrucoMano.jugadasPosibles()
      mostrarLista(jugadas)
      print "Elija el numero de la opcion a jugar: (empezando en 0)"
      opcionInt = int(raw_input("> "))
      opcionJugada = jugadas[opcionInt]
      print "Usted eligio jugar  ",
      print str( opcionJugada )
      TrucoMano.jugar( opcionJugada );
      TrucoPie.recibirJugada( opcionJugada );
      opcionInt = raw_input("Presione una tecla para continuar...")
    elif TrucoPie.esMiTurno:
      jugadas=[]
      jugadas = TrucoPie.jugadasPosibles()
      mostrarLista(jugadas)
      print "\nELIJA LA OPCION QUE JUEGA LA COMPU: (empezando en 0)"
      opcionInt = int(raw_input("> "))
      opcionJugada = jugadas[opcionInt]
      print "La compu juega  ",
      print str( opcionJugada )
      TrucoPie.jugar( opcionJugada )
      TrucoMano.recibirJugada( opcionJugada )


     
  # Aca muestro el Score y juego una nueva Mano
  print "El estado del Score es:\n"
  mano=TrucoMano.ptosGanados(TrucoPie.juegoMio+ TrucoPie.cartasQueTengo)
#  pie=TrucoPie.ptosGanados(TrucoMano.juegoMio+ TrucoMano.cartasQueTengo)
  Score.incrementarSocreMio(mano[1])
#  Score.incrementarScoreOtro(mano[2])
  print str(Score)
  
print "\tRESULTADO FINAL DEL SCORE:"
print str(Score)
