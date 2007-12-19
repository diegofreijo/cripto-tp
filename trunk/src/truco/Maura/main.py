import sys
sys.path.append("red")
sys.path.append("truco")

from ManoTruco import *

esServer=None
x=str(raw_input('Es un servidor??'))
opcion=-1
Mano=ManoTruco(cartas,esServer)

if x=='s':
  esServer=True
  cartas=[(1,'ESPADA'),(7,'ORO'),(3,'ORO')]
else:
  esServer=False
  cartas=[(1,'BASTO'),(7,'BASTO'),(3,'COPA')]
  
while (opcion!=-1):
  if Mano.turnoDeJuego()==True:
      opcion=-1


# El caso es el siguiente. Si me toca jugar, muestro las jugadas posibles y le pido al usuario que seleccione una.
# El usuario le manda la jugada con el metodo Jugar y actualizo los valores de las variables para ver si termino el juego.
# Si no me toca jugar, recibo la jugada que hizo el otro y actualizo los valores de las variables.
# En ambos casos, si se da alguna de las condiciones de la finalizacion de la partida, muestro un cartel y el score final.
# La actualizacion de las variables consiste en corroborar el estado de las cartas, los cantos y a quien le toca el turno.
# Me falta ver como funciona el cambio de los turnos.

print "Por ahora no hago nada!"

