# -*- coding: cp1252 -*-

# El caso es el siguiente. Si me toca jugar, muestro las jugadas posibles y le pido al usuario que seleccione una.
# El usuario le manda la jugada con el metodo Jugar y actualizo los valores de las variables para ver si termino el juego.
# Si no me toca jugar, recibo la jugada que hizo el otro y actualizo los valores de las variables.
# En ambos casos, si se da alguna de las condiciones de la finalizacion de la partida, muestro un cartel y el score final.
# La actualizacion de las variables consiste en corroborar el estado de las cartas, los cantos y a quien le toca el turno.
# Me falta ver como funciona el cambio de los turnos.


from Carta import *
from CantoEnvido import *
from CantoTruco import *

class ManoTruco:
   # variables de instancia
  soyMano = None # esta en 1 si es el servidor, si no, 0
  cartasQueTengo = None # una lista que contiene las posibles cartas a jugar. Cuando se juega una, se la saca de la lista
  subManoActual = None # numero de mano que se esta jugando 1,2,3
  manoEnSubManoActual=None # me parece mejor nombre que _fuiManoEnSubManoActual = None
			# _manoEnSubManoActual=1 si _subManoActual=1 y _soyMano
			# 				o si _subManoActual=2 o _subManoActual=3, el que gano la mano anterior
			#				si no _manoEnSubManoActual=0
  esMiTurno = None # vale 1 si soy mano en _manoEnSubManoActual o si me llega un canto del otro lado y tengo que responder
  juegoMio=None 		# me parece mejoruno  que _cartaMiaEnSubManoActual = None 
  juegoOtro=None 	# me parece mejor que _cartaContricanteEnSubManoActual = None
  estadoEnvido=cantoenvido('',0)
  estadoTruco=cantotruco('',0)
  PtosEnvidoMios=0 # Los puntos los deberia guardar para despues comprobar cuando termine la mano
  PtosEnvidoOtro=0
  PtosEnvidoQuerido=0
  PtosEnvidoNQuerido=0
  PtosTrucoQuiero=0
  PtostrucoNQuiero=0
  alMaso=None
  
  # Ahora definimos el diccionario que contiene las cartas con los niveles
  maso={(1,'ESPADA'):0,(2,'ESPADA'):5,(3,'ESPADA'):4,(4,'ESPADA'):13,(5,'ESPADA'):12,(6,'ESPADA'):11,(7,'ESPADA'):2,(10,'ESPADA'):9,(11,'ESPADA'):8,(12,'ESPADA'):7,
        (1,'ORO'):6,(2,'ORO'):5,(3,'ORO'):4,(4,'ORO'):13,(5,'ORO'):12,(6,'ORO'):11,(7,'ORO'):3,(10,'ORO'):9,(11,'ORO'):8,(12,'ORO'):7,
        (1,'BASTO'):1,(2,'BASTO'):5,(3,'BASTO'):4,(4,'BASTO'):13,(5,'BASTO'):12,(6,'BASTO'):11,(7,'BASTO'):10,(10,'BASTO'):9,(11,'BASTO'):8,(12,'BASTO'):7,
        (1,'COPA'):6,(2,'COPA'):5,(3,'COPA'):4,(4,'COPA'):13,(5,'COPA'):12,(6,'COPA'):11,(7,'COPA'):10,(10,'COPA'):9,(11,'COPA'):8,(12,'COPA'):7}

# las dos ultimas variables son las listas que contienen las jugadas de ambos jugadores de tal manera que si el otro juega una carta o yo decido hacerla, se agregan los elementos a la lista.
# en caso de jugar una carta mia tengo que sacarla de _cartasQueTengo

  def __init__(self, cartasIniciales, soyMano):
    self.soyMano = soyMano
    self.cartasQueTengo = cartasIniciales # cartasIniciales es una lista de las tres cartas del juego de la forma (1,'ESPADA')

    # inicializacion del estado
    self.manoActual = 1
    self.esMiTurno = soyMano
    #self._fuiManoEnSubManOActual = soyMano

  def soyMano(self):
    """True si soy mano (no soy pie, reparti yo, y fui mano en la primera submano), False si no."""
    return self.soyMano

  def manoActual(self):
    """Mano actual, de 1 a 3. None si el juego esta terminado"""
    return self.manoActual

  def nivelCarta(carta):
    #carta es de la forma (1,'ESPADA')
    if isinstance(Carta,carta):
      return maso[carta]
    else:
      raise ValueError('La carta no tiene el formato esperado (1,''ESPADA'')!!')
    
  def ganeMano(mano):
    #esta funcion me dice quien gano la mano. Si es uno, gane yo, si es -1 el otro y 0, es parda
      if nivelCarta(juegoMio[mano])>nivelCarta(juegoOtro[mano]):
        return 1
      elif nivelCarta(juegoMio[mano])<nivelCarta(juegoOtro[mano]):
        return -1
      else:
        return 0
    
  def terminado(self):
    """Si el juego esta terminado o no"""
    # Cuando se jugaron las 6 cartas. Si hay parda en tercera gana el que gano primera. Me tengo que fijar como se jugaron las cartas
    # Cuando hay parda en primera y se juegan las dos cartas en la segunda. Si hay parda en segunda estoy en el caso anterior
    # Cuando se va al maso alguno de los dos
    # Cuando se canta falta envido ( lo podemos considerar por ahora por simplicidad)
    # seteo la variable a None si se da alguna de las condiciones
    cont=0
    if len(juegoMio)==len(juegoOtro)==3:
      # Tengo que contemplar todas las posibles jugadas, ganar dos de tres manos o que alguno o mas sean pardas
      if ganeMano(1)!=0 and ganeMano(2)!=0 and ganeMano(3)!=0:
        for i in range(1,3):
          if ganeMano(i):
            cont=cont+1
        if cont>1:
          print ("Gane la Mano")
        else:
          print ("Perdi la Mano")
      else:
        if ganeMano(2)==0 and ganeMano(3)==1:
          print ("Gane la Mano")
        elif ganeMano(2)==0 and ganeMano(3)==-1:
          print ("Perdi la Mano")
        elif ganeMano(3)==0 and ganeMano(1)==1:
          print ("Gane la Mano")
        elif ganeMano(3)==0 and ganeMano(1)==-1:
          print ("Perdi la Mano")
      manoActual=None
    elif len(juegoMio)==len(juegoOtro)==2:
      if ganeMane(1)==0 and ganeMano(1)==1: # la primera fue parda y gano alguno de los dos
        print ("Gane la Mano")
        _manoActual == None
      elif ganeMane(1)==0 and ganeMano(1)==-1: # la primera fue parda y gano alguno de los dos
        print ("Perdi la Mano")
        manoActual == None
    elif alMaso:
      manoActual==None
    elif estadoEnvido.valor==4:
      print ("Cantaron Falta Envido")
    return manoActual

  def turnoDeJuego(self):
    """A quién le toca jugar. Notar que NO ES LO MISMO que soyMano()"""
    # aca me parece que iria el control de las variables _manoEnSubManoActual y _esMiturno ???
    # cuando soy mano; cuando gane la anterior, o cuando el otro jugo y yo no
    if (subManoActual==1 and soyMano):
      manoEnSubManoActual=True
      esMiturno=True
    elif subManoActual>=2 and len(juegoMio)==len(juegoOtro)==subManoActual:
      if subManoActual==2: subManoActual=subManoActual+1
      if ganeMano(subManoActual-1)==1:
        manoEnSubManoActual=True
        esMiTurno=True
      elif ganeMano(subManoActual-1)==-1:
        manoEnSubManoActual=False
        esMiTurno=False
      elif ganeMano(subManoActual-1)==0:
        if soyMano:
          manoEnSubManoActual=True
          esMiTurno=True
        else:
          manoEnSubManoActual=False
          esMiTurno=False
    elif subManoActual>=2 and len(juegoMio)<len(juegoOtro):
      esMiTurno=True
    return esMiTurno
 
  def jugadasPosibles(self):
    # esto seria: for each _cartasQueTengo armar una jugada que sea poner esa carta y agregarla a una lista, y retornar esa lista
    # Si _esMiTurno (llamo a turnoDeJuego) muestro las siguientes opciones
    # Para el caso de las cartas en juego muestro la lista _cartasQueTengo
    # Para el caso de Envido
    # 	Si no jugue ninguna carta, y estadoEnvido.valor()>=0 o estadoEnvido.valor()<5
    # 		muestro estadoEnvido.codigo() para estadoEnvido.valor() en [estadoEnvido.valor()+1,4]
    # 	Si no jugue ninguna carta, y estadoEnvido.valor()>=5 y estadoEnvido.codigo='QUIERO' y _soyMano
    # 		muestro las opciones de TENGO TANTO (calculo el envido que tengo)
    # 	Si no jugue ninguna carta, y estadoEnvido.valor()>=5 y estadoEnvido.codigo='QUIERO' y not _soyMano
    # 		muestro las opciones de TANTO SON MEJORES (calculo el envido que tengo)
    # 		muestro las opciones de SON BUENAS
    # Para el caso de Truco
    # 	Si estadoTruco.valor()>=0 o estadoTruco.valor()<4
    # 		muestro estadoTruco.codigo()+ 1
    # 	Si estadoTruco.valor()>=4
    # 		no muestro nada porque esta todo cantado
    # Irse al maso!!!
    JPosibles=[]
    for i in len(cartasQueTengo):
      JPosibles.append(cartasQueTengo[i].str())
    if len(juegoMio)==0 and estadoEnvido.valor()<5:
      for i in range(estadoEnvido.valor()+1,len(estadoEnvido.opciones)):
        JPosibles=JPosobles+ estadoEnvido.opciones[i]
      if estadoEnvido.valor()>0:
        JPosibles.append('QUIERO')
        JPosibles.append('NO QUIERO')
      if estadoEnvido.valor()>=5 and estadoEnvido.codigo=='QUIERO':
        if PtosEnvidoOtro==0:
          JPosibles.append('TENGO' + str(CalcularEnvido()))
        else:
          JPosibles.append(str(CalcularEnvido()) + 'SON MEJORES')
          JPosibles.append('SON BUENAS')
    if estatoTruco.valor()<4:
      for i in range(estadoTruco+1, len(estadoTruco.opciones)):
        JPosibles.append(estadoTruco.opciones[i])
      if estadoTruco.valor()<4:
          JPosibles.append('QUIERO')
          JPosibles.append('NO QUIERO')
    return JPosibles # me parece que convendria devolver la lista con las opciones posibles que son las que forman el menu

  def actualizarCanto(jugada):
    if jugada==ENVIDO:
      PtosEnvidoQuerido=2
      PtosEnvidoNQuerido=1
      estadoEnvido=ENVIDO
    elif jugada==ENVIDOENVIDO:
      PtosEnvidoQuerido=PtosEnvidoQuerido+2
      PtosEnvidoNQuerido=PtosEnvidoNQuerido+1
      estadoEnvido=ENVIDOENVIDO
    elif jugada==REALENVIDO:
      PtosEnvidoQuerido=PtosEnvidoQuerido+3
      PtosEnvidoNQuerido=PtosEnvidoNQuerido+1
      estadoEnvido=REALENVIDO
    elif jugada==FALTAENVIDO:
      PtosEnvidoQuerido=PtosEnvidoQuerido+4
      PtosEnvidoNQuerido=PtosEnvidoNQuerido+1
      estadoEnvido=FALTAENVIDO
    elif jugada==QUIEROENVIDO:
      estadoEnvido=QUIEROENVIDO
    elif jugada==NOQUIEROENVIDO:
      estadoEnvido=NOQUIEROENVIDO
    elif jugada==TRUCO:
      PtosTrucoQuerido=2
      PtosTrucoNQuerido=1
      estadoTruco=TRUCO
    elif jugada==RETRUCO:
      PtosTrucoQuerido=PtosTrucoQuerido+1
      PtosTrucoNQuerido=PtosTrucoNQuerido+1
      estadoTruco=RETRUCO
    elif jugada==VALECUATRO:
      PtosTrucoQuerido=PtosTrucoQuerido+1
      PtosTrucoNQuerido=PtosTrucoNQuerido+1
      estadoTruco=VALETRUCO
    elif jugada==QUIEROTRUCO:
      estadoTruco=QUIEROTRUCO
    elif jugada==NOQUIEROTRUCO:
      estadoTruco=NOQUIEROTRUCO
    else:
      raise ValueError('El canto o la carta no tiene el formato establecido o no existe!!')
    
  def jugar(self, jugada):
    """realizar una lista de jugadas (o sea, Cantos y/o Cartas) que hace esta parte"""
    # si me voy al mazo, perdi, y es el fin del juego
    # extraigo carta de la jugada y la guardo como _cartaMiaEnSubManoActual
    # sacar carta jugada de la lista _cartasQueTengo
    # si no _fuiManoEnSubManoActual, termina una submano
#    if not self._fuiManoEnSubManoActual then
#      _terminaSubMano(self)
#    else 
#      # si _fuiManoEnSubManoActual, le cambia el turno (le toca al otro) y nada mas
#      self._esMiTurno = not self._esMiTurno
    
    # me parece que esta funcion la tiene que invocar el usuario cuando selecciona una opcion. Por lo tanto, lo que hay que hacer es procesarla y ver los cambios que pueden producir
    # como se que tipo de jugada es?? Aca es donde decian que hacia falta la clase Jugada??
    # Si se juega una carta
    #		la agrego a la lista _juegoMio y si len(_juegoMio)==len(_juegoMio)==_subManoActual
    # 			me fijo cual de los dos gano la mano. Si soy yo entonces _esMiTurno=1 (aca tendria que llamar a turnoDeJuego)
    # Si juego un canto de Envido
    # 	debo actualizar los puntos en juego del envido querido y no querido
    #		si jugada=ENVIDO, _PtosEnvidoQuerido=2,_PtosEnvidoNQuerido=1
    #		si jugada=ENVIDOENVIDO, _PtosEnvidoQuerido+=2,_PtosEnvidoNQuerido+=1
    #		si jugada=REALENVIDO, _PtosEnvidoQuerido+=3,_PtosEnvidoNQuerido+=1
    #		si jugada=FALTAENVIDO, _PtosEnvidoQuerido+=2,_PtosEnvidoNQuerido+=1 (puede ser que termine el juego. Hay que ver el Score)
    #		si jugada=QUIERO, no incremento el score.Luego en el menu va a aprecer la opcion TENGO TANTO
    #		si jugada=NOQUIERO, no incremento el score
    #	Si juego un canto de Truco
    #		si jugada=TRUCO, _PtosTrucoQuerido+=2,_PtosTrucoNQuerido+=1
    #		si jugada=RETRUCO, _PtosEnvidoQuerido+=1,_PtosEnvidoNQuerido+=1
    #		si jugada=VALE4, _PtosEnvidoQuerido+=1,_PtosEnvidoNQuerido+=1
    #		si jugada=QUIERO, no incremento el score. Cuando se termine la mano veo quien gano y actualizo el score
    #		si jugada=NOQUIERO, no incremento el score. Cuando se termine la mano veo quien gano y actualizo el score
    # Si se jugaba un canto de carta y canto se dividia en dos y se trataba por separado sin necesidad de preguntar dos veces??
    # Irse al maso!!!

    if isinstance(Carta,jugada):
      cartasQueTengo.remove(jugada)
      juegoMio.append(jugada)
    else:
      actualizarCanto(jugada)
    
      
  def recibirJugada(self, jugada):
    """recibir las jugadas que realiza la contraparte (Cantos y/o Cartas)
    que hace mi contrincante"""
    # si se fue al mazo, perdio y es el fin del juego
    # extraigo carta de la jugada que recibo y la guardo como _cartaContricanteEnSubManoActual
    # si _fuiManoEnSubManoActual, termina una submano
#   if self._fuiManoEnSubManoActual then
#     _terminaSubMano(self)
#     else 
#      # si no _fuiManoEnSubManoActual, le cambia el turno (me toca a mi) y nada mas
#      self._esMiTurno = not self._esMiTurno

    # lo que hay que hacer es procesarla y ver los cambios que pueden producir
    # como se que tipo de jugada es?? Aca es donde decian que hacia falta la clase Jugada??
    # Si llego una carta
    #		la agrego a la lista _juegoOtro y si len(_juegoOtro)==len(_juegoMio)==_subManoActual
    # 			me fijo cual de los dos gano la mano. Si soy yo entonces _esMiTurno=1 (aca llamo a turnoDeJuego)
    # Si llego un canto de Envido
    # 	debo actualizar los puntos en juego del envido querido y no querido
    #		si jugada=ENVIDO, _PtosEnvidoQuerido=2,_PtosEnvidoNQuerido=1
    #		si jugada=ENVIDOENVIDO, _PtosEnvidoQuerido+=2,_PtosEnvidoNQuerido+=1
    #		si jugada=REALENVIDO, _PtosEnvidoQuerido+=3,_PtosEnvidoNQuerido+=1
    #		si jugada=FALTAENVIDO, _PtosEnvidoQuerido+=2,_PtosEnvidoNQuerido+=1 (puede ser que termine el juego. Hay que ver el Score)
    #		si jugada=QUIERO, no incremento el score.Luego en el menu va a aprecer la opcion TENGO TANTO
    #		si jugada=NOQUIERO, no incremento el score
    #	Si llego un canto de Truco
    #		si jugada=TRUCO, _PtosTrucoQuerido+=2,_PtosTrucoNQuerido+=1
    #		si jugada=RETRUCO, _PtosEnvidoQuerido+=1,_PtosEnvidoNQuerido+=1
    #		si jugada=VALE4, _PtosEnvidoQuerido+=1,_PtosEnvidoNQuerido+=1
    #		si jugada=QUIERO, no incremento el score. Cuando se termine la mano veo quien gano y actualizo el score
    #		si jugada=NOQUIERO, no incremento el score. Cuando se termine la mano veo quien gano y actualizo el score
    # Si se jugaba un canto de carta y canto se dividia en dos y se trataba por separado sin necesidad de preguntar dos veces??
    if isinstance(Carta,jugada):
      juegoOtro.append(jugada)
    else:
      actualizarCanto(jugada)

  def _terminaSubMano(self):
    # ME PARECE QUE POR AHORA ESTA FUNCION NO HACE FALTA
    # Esta funcion debe ser llamada despues de hacer una jugada o recibir una jugada pero no se si en realidad hace falta o no
    #   el que mata, sigue jugando
    #   si parda la primera, sigue la mano
    #   si parda la segunda, sigue el que hizo primera, si parda la primera, sigue la mano
    #   si juego la tercera, y no _fuiManoEnSubManoActual, entonces es el fin del juego

    # reseteo variables de subMano
    #_cartaMiaEnSubManoActual = None
    #_cartaContricanteEnSubManoActual = None

    # Para mi deberia ser asi:
    # Si len(_juegoOtro)==len(_juegoMio)==_subManoActual, _subManoActual+=1
    # y despues llamar turnoDeJuego y si me toca llamo a JugadasPosibles
    return 0

  def calcularEnvido(self):
	# si hay tres cartas del mismo palo tomo las dos mas altas
	# si hay dos cartas con el mismo palo las sumo
	# si hay palos distintos devuelvo la mas alta
	# Puede ser que tenga que calcular los puntos cuando yo ya haya jugado (el caso en que canta el otro y diga quiero)
	# Para el caso anterior me fijo en _cartasQueTengo y _juegoMio
    PtosEnvidoMios=20
    return PtosEnvidoMios

  def puntaje(self):
    """mi puntaje"""

  def puntajeContrincante(self):
    """puntaje de mi contrincante"""

  def recibirFinJuego(self, cartasMostradas):
    """Mi contrincante cierra el juego mostrando las cartas en cartasMostradas"""
