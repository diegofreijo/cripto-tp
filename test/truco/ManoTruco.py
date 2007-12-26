# -*- coding: cp1252 -*-
# Tomado de /src/truco/Maura/ManoTruco.py rev. 98

# cuando se dice quiero o no quiero del envido o truco hay que ver a quien le tocaba jugar. LLamo a terminoSbMano

# El caso es el siguiente. Si me toca jugar, muestro las jugadas posibles y le pido al usuario que seleccione una.
# El usuario le manda la jugada con el metodo Jugar y actualizo los valores de las variables para ver si termino el juego.
# Si no me toca jugar, recibo la jugada que hizo el otro y actualizo los valores de las variables.
# En ambos casos, si se da alguna de las condiciones de la finalizacion de la partida, muestro un cartel y el score final.
# La actualizacion de las variables consiste en corroborar el estado de las cartas, los cantos y a quien le toca el turno.
# Me falta ver como funciona el cambio de los turnos.


from Carta import *
from CantoEnvido import *
from CantoEnvido import _cantoEnvido
from CantoEnvido import _cantoEnvidoTantos
from CantoTruco import _cantoTruco
from CantoTruco import *

class ManoTruco:
   # variables de instancia
  soyMano = None # esta en 1 si es el servidor, si no, 0
  cartasQueTengo = None # una lista que contiene las posibles cartas a jugar. Cuando se juega una, se la saca de la lista
  subManoActual = 0 # numero de mano que se esta jugando 1,2,3
  manoEnSubManoActual=None 
  esMiTurno = None # vale 1 si soy mano en _manoEnSubManoActual o si me llega un canto del otro lado y tengo que responder
  juegoMio= None		# me parece mejoruno  que _cartaMiaEnSubManoActual = None 
  juegoOtro= None 	# me parece mejor que _cartaContricanteEnSubManoActual = None
  estadoEnvido=ENVIDONOCANTADO
  estadoTruco=TRUCONOCANTADO
  PtosEnvidoOtro=None
  PtosEnvidoQuerido=None
  PtosEnvidoNQuerido=None
  PtosTrucoQuiero=None
  PtostrucoNQuiero=None
  alMazo=None
  tengoTantas=None
  noTengoNada=None
  intercambiandoTantos=None
  canteMisTantos=None
  ultimoEstadoTruco=None

  # Funcion auxiliar (no es un metodo de la clase)
  def _valorRelativoCarta(carta):
    if carta.numero() == 4:
      return 0
    if carta.numero() == 5:
      return 1
    if carta.numero() == 6:
      return 2
    if carta.numero() == 7 and (carta.esCopa() or carta.esBasto()):
      return 3
    if carta.numero() == 10:
      return 4
    if carta.numero() == 11:
      return 5
    if carta.numero() == 12:
      return 6
    if carta.numero() == 1 and (carta.esCopa() or carta.esOro()):
      return 7
    if carta.numero() == 2:
      return 8
    if carta.numero() == 3:
      return 9
    if carta.numero() == 7 and carta.esOro():
      return 10
    if carta.numero() == 7 and carta.esEspada():
      return 11
    if carta.numero() == 1 and carta.esBasto():
      return 12
    if carta.numero() == 1 and carta.esEspada():
      return 13
    return -1

  # Ahora definimos el diccionario que contiene las cartas con los niveles
  mazo = {}
  for num in [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]:
    for palo in [Palo.BASTO, Palo.COPA, Palo.ESPADA, Palo.ORO]:
      carta = Carta(num, palo)
      nivel = _valorRelativoCarta(carta)
      mazo[carta] = nivel # definir el valor
  #

# las dos ultimas variables son las listas que contienen las jugadas de ambos jugadores de tal manera que si el otro juega una carta o yo decido hacerla, se agregan los elementos a la lista.
# en caso de jugar una carta mia tengo que sacarla de _cartasQueTengo

  def __init__(self, cartasIniciales, soyMano):
    self.soyMano = soyMano
    self.cartasQueTengo = cartasIniciales[:] # cartasIniciales es una lista de las tres cartas del juego de la forma (1,'ESPADA')
    self.tengoTantas=_cantoEnvidoTantos('TANTOS', self.calcularEnvido())
#    print "Tengo tantas " + str(self.tengoTantas)
    # inicializacion del estado
    self.subManoActual = 0 # numero de mano que se esta jugando 1,2,3
    self.esMiTurno = soyMano
    self.manoEnSubManoActual=soyMano
    self.juegoMio=[]
    self.juegoOtro=[]
    self.noTengoNada=NOTENGOTANTOS
    self.PtosEnvidoOtro=-1
    self.estadoEnvido=ENVIDONOCANTADO
    self.estadoTruco=TRUCONOCANTADO
    self.PtosEnvidoQuerido=-1
    self.PtosEnvidoNQuerido=-1
    self.PtosTrucoQuiero=-1
    self.PtostrucoNQuiero=-1
    self.alMazo=0
    self.intercambiandoTantos=False
    self.canteMisTantos=False
    self.ultimoEstadoTruco=TRUCONOCANTADO

  def soyMano(self):
    """True si soy mano (no soy pie, reparti yo, y fui mano en la primera submano), False si no."""
    return self.soyMano

  def nivelCarta(self, carta):
    if carta in self.mazo:
      return self.mazo[carta]
    raise ValueError('No es una carta existente en el mazo: ' + repr(carta))

  def ganeMano(self, mano):
    #esta funcion me dice quien gano la mano. Si es uno, gane yo, si es -1 el otro y 0, es parda
      if self.nivelCarta(self.juegoMio[mano])<self.nivelCarta(self.juegoOtro[mano]):
        return 1
      elif self.nivelCarta(self.juegoMio[mano])>self.nivelCarta(self.juegoOtro[mano]):
        return -1
      else: #si fue parda
        return 0

  def manoActual(self):
    """
    Esta funcion devuelve None si la partida se termino. De lo contrario, la mano que se juega
    """
    # Cuando se jugaron las 6 cartas. Si hay parda en tercera gana el que gano primera. Me tengo que fijar como se jugaron las cartas
    # Cuando hay parda en primera y se juegan las dos cartas en la segunda. Si hay parda en segunda estoy en el caso anterior
    # Cuando se va al mazo alguno de los dos
    # Cuando se canta falta envido ( lo podemos considerar por ahora por simplicidad)
    # seteo la variable a None si se da alguna de las condiciones
    cont=0
    if len(self.juegoMio)==len(self.juegoOtro)==3:
      # Tengo que contemplar todas las posibles jugadas, ganar dos de tres manos o que alguno o mas sean pardas
      if self.ganeMano(0)!=0 and self.ganeMano(1)!=0 and self.ganeMano(2)!=0: # si ninguna de las tres fue parda cuento la cantidad de manos que gane
        uno=self.ganeMano(0)
        dos=self.ganeMano(1)
        tres=self.ganeMano(2)
        if uno==1: cont=cont+1
        if dos==1: cont=cont+1
        if tres==1:cont=cont+1
        print "uno: " + str(uno) + "   dos:   " + str(dos) + "   tres:  " + str(tres) + " Cantidad de Manos Ganadas " + str(cont)
        if cont>1:
          print ("Gane la Mano")
        else:
          print ("Perdi la Mano")
      else:
        if self.ganeMano(1)==0 and self.ganeMano(2)==1:
          print ("Gane la Mano")
        elif self.ganeMano(1)==0 and self.ganeMano(2)==-1:
          print ("Perdi la Mano")
        elif self.ganeMano(2)==0 and self.ganeMano(0)==1:
          print ("Gane la Mano")
        elif self.ganeMano(2)==0 and self.ganeMano(0)==-1:
          print ("Perdi la Mano")
      self.subManoActual=0 # termina la mano porque ya se jugaron todas las posibles cartas
      return None
    elif len(self.juegoMio)==len(self.juegoOtro)==2:
      if self.ganeMano(0)==0 and self.ganeMano(1)==1: # la primera fue parda y gano alguno de los dos
        print ("Gane la Mano")
        self.subManoActual =0
        return None
      elif self.ganeMano(0)==0 and self.ganeMano(1)==-1: # la primera fue parda y gano alguno de los dos
        print ("Perdi la Mano")
        self.subManoActual =0
        return None
    elif self.estadoEnvido==FALTAENVIDO:
      print "Cantaron Falta Envido"
      return None
    elif self.estadoTruco==NOQUIEROTRUCO:
      print "Se temino la partido porque no se quizo el Truco"
      return None
    return self.subManoActual

  def terminado(self):
    """
    Si el juego esta terminado o no
    """
    t = self.manoActual()
    if t == None:
      return True
    return False

  def turnoDeJuego(self):
    """
    A quién le toca jugar. Notar que NO ES LO MISMO que soyMano()
    Devuelve True si me toca a mí, False si le toca a mi contrincante, y None si el juego terminó
    """
    return self.esMiTurno

  def _terminaSubMano(self):
    if len(self.juegoMio)!=len(self.juegoOtro):
      return None
    
    if len(self.juegoMio)==len(self.juegoOtro) and len(self.juegoOtro)==0: # caso inicial
      if self.soyMano:
        self.manoEnSubManoActual=True
        self.esMiTurno=True
      else:
        self.manoEnSubManoActual=False
        self.esMiTurno=False
    elif len(self.juegoMio)==len(self.juegoOtro) and len(self.juegoOtro)>0: # se termino la mano, me fijo quien la gano e incremento subManoActual y esMiTurno
      largo=len(self.juegoMio)
      if self.ganeMano(largo-1)==-1:
        self.esMiTurno=False
      elif self.ganeMano(largo-1)==1:
        self.esMiTurno=True
      elif self.ganeMano(largo-1)==0 and self.soyMano:
        self.esMiTurno=True
      else:
        self.esMiTurno=False
        print "es un caso que no tengo contemplado"
    self.subManoActual=self.subManoActual+1
    self.manoEnSubManoActual=self.esMiTurno
    return self.esMiTurno

  def turnoDeJuegoEnvido(self):
    if self.envidoCerrado():
#      print "self.envidoCerrado() "+ str(self.envidoCerrado())
      self.esMiTurno=self.soyMano
      return
    if not self.envidoCerrado() and self.estadoEnvido!=ENVIDONOCANTADO:
      self.esMiTurno=not self.esMiTurno
      print "not self.envidoCerrado() and self.estadoEnvido!=ENVIDONOCANTADO "+ str(not self.envidoCerrado() and self.estadoEnvido!=ENVIDONOCANTADO)
      return
  def turnoDeJuegoTruco(self):
    if self.trucoCerrado():
      print "self.trucoCerrado() "+ str(self.trucoCerrado())
      if len(self.juegoMio)> len(self.juegoOtro):
        self.esMiTurno=False
      elif len(self.juegoMio)< len(self.juegoOtro):
        self.esMiTurno=True
      else: # si los dos tenemos la misma cantidad de cartas
        self._terminaSubMano()
        print "self._terminaSubMano() "+ str(self._terminaSubMano())
      return

    if not self.trucoCerrado() and self.estadoTruco!=TRUCONOCANTADO:
      self.esMiTurno=not self.esMiTurno
      print "not self.trucoCerrado() and self.estadoTruco!=TRUCONOCANTADO"+ str(not self.trucoCerrado() and self.estadoTruco!=TRUCONOCANTADO)
    return

  def _viejo_turnoDeJuego(self):
    # aca me parece que iria el control de las variables _manoEnSubManoActual y _esMiturno ???
    # cuando soy mano; cuando gane la anterior, o cuando el otro jugo y yo no
    if self._terminaSubMano()==None:
      if len(self.juegoMio)> len(self.juegoOtro):
        self.esMiTurno=False
      elif len(self.juegoMio)< len(self.juegoOtro):
        self.esMiTurno=True
      else: # si los dos tenemos la misma cantidad de cartas
        self._terminaSubMano()
 #       print "self._terminaSubMano() "+ str(self._terminaSubMano())
      return    

  def envidoCerrado(self):
    return self.estadoEnvido==QUIEROENVIDO or self.estadoEnvido==NOQUIEROENVIDO

  def trucoCerrado(self):
    return self.estadoTruco==QUIEROTRUCO or self.estadoTruco==NOQUIEROTRUCO
    
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
    # Irse al mazo!!!
    JPosibles=[]
    #for i in range(0,len(self.cartasQueTengo)):
    i=0
    #hasta que no se cierren los cantos no puedo mostrar la jugada
    print "self.intercambiandoTantos  " + str(self.intercambiandoTantos)
    if (self.estadoEnvido==ENVIDONOCANTADO or (self.envidoCerrado() and self.canteMisTantos==True)) and \
    (self.estadoTruco==TRUCONOCANTADO or self.trucoCerrado()) : 
      while i<len(self.cartasQueTengo):
        JPosibles.append((self.cartasQueTengo[i]))
        i=i+1
        
    if (len(self.juegoMio)==0 or len(self.juegoOtro)==0) and self.estadoEnvido in CANTOS_ENVIDO and \
       (self.estadoTruco==TRUCONOCANTADO or self.estadoTruco==TRUCO) :
      lista=[] + cantosMayores(self.estadoEnvido)
      JPosibles=JPosibles + cantosMayores(self.estadoEnvido)
      if self.estadoEnvido!=ENVIDONOCANTADO:
        JPosibles.append(QUIEROENVIDO)
        JPosibles.append(NOQUIEROENVIDO)
    elif (len(self.juegoMio)==0 or len(self.juegoOtro)==0) and self.estadoEnvido==QUIEROENVIDO and self.intercambiandoTantos==True:
        if self.PtosEnvidoOtro>0:
          JPosibles.append(self.noTengoNada)
        JPosibles.append(self.tengoTantas)
    if (self.envidoCerrado() or self.estadoEnvido==ENVIDONOCANTADO) and self.intercambiandoTantos==False and \
       (self.estadoTruco in CANTOS_TRUCO or self.estadoTruco==QUIEROTRUCO):
      JPosibles.append(cantoSiguiente(self.ultimoEstadoTruco))
      if self.estadoTruco!=TRUCONOCANTADO and self.estadoTruco!=QUIEROTRUCO and self.estadoTruco!=NOQUIEROTRUCO :
        JPosibles.append(QUIEROTRUCO)
        JPosibles.append(NOQUIEROTRUCO)
    return JPosibles # me parece que convendria devolver la lista con las opciones posibles que son las que forman el menu

  def actualizarCanto(self,jugada,jugar): # 0 si el usuario pide jugar algo y 1 si recibe una jugada
    if isinstance(jugada,_cantoEnvidoTantos):# or jugada==NOTENGOTANTOS: # para el envido cuando hay que cantar los puntos se van a mandar objetos de la clase _cantoEnvidoTanto
                                                # de tal manera que si cuando se dice quiero una manda los puntos en este objeto. El otro responde con otro
                                                #  paquete que contiene 0 si le gane o los puntos si no le gane (el otro puede mandar los puntos sabiendo)
                                                # que igualmente pierde. Quedara en el contrincante pedir que se muestren las cartas y modificar el score
      if jugar==1: #esoy recibiendo la jugada
        self.PtosEnvidoOtro=Tantos(jugada)
        print "PtosEnvidoOtro  " + str(self.PtosEnvidoOtro)
        print "Estoy recibiendo los puntos de la otra parte: " + str(self.PtosEnvidoOtro) + "    " + str(Tantos(jugada))
        if self.PtosEnvidoOtro>=0:
          if self.PtosEnvidoOtro>self.tengoTantas.tantos:
            print "Perdi el Envido"
            self.esMiTurno=not self.esMiTurno
          elif self.PtosEnvidoOtro<self.tengoTantas.tantos:
            print "Gane el Envido"
            self.esMiTurno=not self.esMiTurno
          elif self.PtosEnvidoOtro==self.tengoTantas.tantos:
            print "Gano la mano porque pardaron en los puntos. soyMano " + str(self.soyMano)
            self.esMiTurno=not self.esMiTurno
        if self.canteMisTantos==True:
          self.intercambiandoTantos=False
      else:
        self.esMiTurno=not self.esMiTurno
        self.canteMisTantos=True
      if jugar==0 and self.PtosEnvidoOtro>=0:
        self.intercambiandoTantos=False
        self._viejo_turnoDeJuego() # ya se como salio en envido y le contesto al otro para que sepa

      print "IntercambiandoTantos "+ str(self.intercambiandoTantos)
      print "self.tengoTantas.tantos "+ str(self.tengoTantas.tantos)
      print "self.PtoEnvidoOtro "+ str(self.PtosEnvidoOtro)        
      print "self.esMiTurno  " + str(self.esMiTurno)
      return
    if isinstance(jugada,_cantoEnvido):
      if jugada==ENVIDO:
        self.PtosEnvidoQuerido=2
        self.PtosEnvidoNQuerido=1
        self.estadoEnvido=ENVIDO
      elif jugada==ENVIDOENVIDO:
        self.PtosEnvidoQuerido=self.PtosEnvidoQuerido+2
        self.PtosEnvidoNQuerido=self.PtosEnvidoNQuerido+1
        self.estadoEnvido=ENVIDOENVIDO
      elif jugada==REALENVIDO:
        self.PtosEnvidoQuerido=self.PtosEnvidoQuerido+3
        self.PtosEnvidoNQuerido=self.PtosEnvidoNQuerido+1
        self.estadoEnvido=REALENVIDO
      elif jugada==FALTAENVIDO:
        self.PtosEnvidoQuerido=self.PtosEnvidoQuerido+4
        self.PtosEnvidoNQuerido=self.PtosEnvidoNQuerido+1
        self.estadoEnvido=FALTAENVIDO
      elif jugada==QUIEROENVIDO:
        self.estadoEnvido=QUIEROENVIDO
        self.intercambiandoTantos=True
        print "IntercambiandoTantos "+ str(self.intercambiandoTantos)
      elif jugada==NOQUIEROENVIDO:
        self.estadoEnvido=NOQUIEROENVIDO
      self.turnoDeJuegoEnvido()
      return
    if isinstance(jugada,_cantoTruco):
      if jugada==TRUCO:
        self.PtosTrucoQuerido=2
        self.PtosTrucoNQuerido=1
        self.estadoTruco=TRUCO
        self.ultimoEstadoTruco=TRUCO
      elif jugada==RETRUCO:
        self.PtosTrucoQuerido=self.PtosTrucoQuerido+1
        self.PtosTrucoNQuerido=self.PtosTrucoNQuerido+1
        self.estadoTruco=RETRUCO
        self.ultimoEstadoTruco=RETRUCO
      elif jugada==VALE4:
        self.PtosTrucoQuerido=self.PtosTrucoQuerido+1
        self.PtosTrucoNQuerido=self.PtosTrucoNQuerido+1
        self.estadoTruco=VALE4
        self.ultimoEstadoTruco=VALE4
      elif jugada==QUIEROTRUCO:
        self.estadoTruco=QUIEROTRUCO
      elif jugada==NOQUIEROTRUCO:
        self.estadoTruco=NOQUIEROTRUCO
      self.turnoDeJuegoTruco()
      return
    raise ValueError('El canto o la carta no tiene el formato establecido o no existe!!')
    return True

    
  def jugar(self, jugada):
    """
    Realizar una lista de jugadas (o sea, Cantos y/o Cartas) que hace esta parte
    """
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
    # Irse al mazo!!!

    if not self.esMiTurno:
      return False

    if isinstance(jugada, Carta):
      self.cartasQueTengo.remove(jugada)
      self.juegoMio.append(jugada)
      self._viejo_turnoDeJuego()
    else:
      self.actualizarCanto(jugada,0)
    return True
      
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

    if self.esMiTurno:
      return False
    if isinstance(jugada,Carta):
      self.juegoOtro.append(jugada)
      self._viejo_turnoDeJuego()
    else:
      if isinstance(jugada,_cantoEnvidoTantos): print "estoy recibiendo los puntos del otro lado " +  str(jugada)
      self.actualizarCanto(jugada,1)
    return True
  

  def calcularEnvido(self):
	# si hay tres cartas del mismo palo tomo las dos mas altas
	# si hay dos cartas con el mismo palo las sumo
	# si hay palos distintos devuelvo la mas alta
	# Puede ser que tenga que calcular los puntos cuando yo ya haya jugado (el caso en que canta el otro y diga quiero)
	# Para el caso anterior me fijo en _cartasQueTengo y _juegoMio
    if self.soyMano:
      self.PtosEnvidoMios=27
    else:
      self.PtosEnvidoMios=20
    return self.PtosEnvidoMios

  def puntaje(self):
    """mi puntaje"""

  def puntajeContrincante(self):
    """puntaje de mi contrincante"""

  def recibirFinJuego(self, cartasMostradas):
    """Mi contrincante cierra el juego mostrando las cartas en cartasMostradas"""

