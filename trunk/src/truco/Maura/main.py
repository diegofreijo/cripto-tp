import sys
sys.path.append("red")
sys.path.append("truco")

from ManoTruco import *

esServer=None
x=str(raw_input('Es un servidor??  '))
opcion=-2

print x
c1=Carta(1,Palo.ESPADA)
c2=Carta(7,Palo.ORO)
c3=Carta(3,Palo.ORO)
c4=Carta(1,Palo.BASTO)
c5=Carta(7,Palo.BASTO)
c6=Carta(3,Palo.COPA)

if x=='s':
  esServer=True
  cartas=[c1,c2,c3]
else:
  esServer=False
  cartas=[c4,c5,c6]

Mano=ManoTruco(cartas,esServer)

while opcion!=-1:
  if Mano.turnoDeJuego()==True:
    jugadas=Mano.jugadasPosibles()
    print jugadas
    opcion=raw_input('Ingrese la jugada a realizar:  ')
    print jugadas[opcion]
    Mano.jugar(jugadas[opcion])
  else:
    Mano.recibirJugada(jugada)
  if Mano.terminado()==None:
      print "Terimno el Partido"
      opcion=-1


# El caso es el siguiente. Si me toca jugar, muestro las jugadas posibles y le pido al usuario que seleccione una.
# El usuario le manda la jugada con el metodo Jugar y actualizo los valores de las variables para ver si termino el juego.
# Si no me toca jugar, recibo la jugada que hizo el otro y actualizo los valores de las variables.
# En ambos casos, si se da alguna de las condiciones de la finalizacion de la partida, muestro un cartel y el score final.
# La actualizacion de las variables consiste en corroborar el estado de las cartas, los cantos y a quien le toca el turno.
# Me falta ver como funciona el cambio de los turnos.

print "Por ahora no hago nada!"

