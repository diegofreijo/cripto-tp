import sys
sys.path.append("red")
# import LogicaRed
sys.path.append("truco")
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
  cartasMano.append( Carta( 3,Palo.ESPADA ) )
  cartasMano.append( Carta( 2,Palo.ESPADA ) )
  cartasMano.append( Carta( 1,Palo.ESPADA ) )
  cartasPie = []
  cartasPie.append( Carta( 1,Palo.BASTO ) )
  cartasPie.append( Carta( 2,Palo.ORO ) )
  cartasPie.append( Carta( 3,Palo.ORO ) )

  TrucoMano = ManoTruco.ManoTruco( cartasMano, True )
  TrucoPie = ManoTruco.ManoTruco( cartasPie, False )

  while TrucoMano.terminado()!=None or TrucoPie.terminado()!=None:
    if TrucoMano.esMiTurno:
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
      jugadas = TrucoPie.jugadasPosibles()
      mostrarLista(jugadas)
      print "\nELIJA LA OPCION QUE JUEGA LA COMPU: (empezando en 0)"
      opcionInt = int(raw_input("> "))
      opcionJugada = jugadas[opcionInt]
      print "La compu juega  ",
      print str( opcionJugada )
      TrucoPie.jugar( opcionJugada )
      TrucoMano.recibirJugada( opcionJugada )
  
  if TrucoMano.terminado()==None:
    if TrucoMano.ganePartida==True:
      print "La Mano gano la Partida!"
    else:
      print "El Pie gano la Partida!"
  elif TrucoPie.terminado()==None:
    if TrucoPie.ganePartida==False:
      print "La Mano gano la Partida!"
    else:
      print "El Pie gano la Partida!"

  if TrucoMano.cartasEnvido[0]<TrucoMano.PtosEnvidoOtro and TrucoMano.estadoEnvido==QUIEROENVIDO:
    verificar=(raw_intput("Desea pedirle a la otra parte que muestre sus cartas? (s/n)"))
    verificar.lower()
    if verificar=='s':
      # mando el pedido de Mostrar las cartas y el otro le devuelve el mensaje con las cartas
      jugada=["MOSTRAR TANTOS",[]]
      TrucoMano.jugar(jugada)
      jugada[1]=jugada[1]+TrucoMano.cartasEnvido[1]
      TrucoPie.recibirJugada(jugada)
  elif TrucoPie.cartasEnvido[0]<TrucoPie.PtosEnvidoOtro and TrucoPie.estadoEnvido==QUIEROENVIDO:
    verificar=(raw_intput("Desea pedirle a la otra parte que muestre sus cartas? (s/n)"))
    verificar.lower()
    if verificar=='s':
      # mando el pedido de Mostrar las cartas y el otro le devuelve el mensaje con las cartas
      jugada=["MOSTRAR TANTOS",[]]
      TrucoPie.jugar(jugada)
      jugada[1]=jugada[1]+TrucoPie.cartasEnvido[1]
      TrucoMano.recibirJugada(jugada)
  # Aca muetsro el Score y juego una nueva Mano
  print "El estado del Score es:\n"
  mano=TrucoMano.ptosGanados()
  pie=TrucoPie.ptosGanados()
  print "TrucoMano.ptosGanados() " + str(mano)
  print "TrucoPie.ptosGanados() " + str(pie)
  Score.incrementarSocreMio(mano)
  Score.incrementarScoreOtro(pie)
  print str(Score)
  
print "\tRESULTADO FINAL DEL SCORE:"
print str(Score)
