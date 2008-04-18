# -*- coding: cp1252 -*-
# cuando se dice quiero o no quiero del envido o truco hay que ver a quien le tocaba jugar. LLamo a terminoSbMano

# El caso es el siguiente. Si me toca jugar, muestro las jugadas posibles y le pido al usuario que seleccione una.
# El usuario le manda la jugada con el metodo Jugar y actualizo los valores de las variables para ver si termino el juego.
# Si no me toca jugar, recibo la jugada que hizo el otro y actualizo los valores de las variables.
# En ambos casos, si se da alguna de las condiciones de la finalizacion de la partida, muestro un cartel y el score final.
# La actualizacion de las variables consiste en corroborar el estado de las cartas, los cantos y a quien le toca el turno.
# Me falta ver como funciona el cambio de los turnos.


from Carta import *
from Palo import *
from CantoEnvido import *
from CantoEnvido import _cantoEnvido
from CantoEnvido import _cantoEnvidoTantos
from CantoTruco import _cantoTruco
from CantoTruco import *

class ManoTruco:
   # variables de instancia
  soyMano = False # esta en True si es el servidor, si no, False
  manoEnSubManoActual=None
  
  esMiTurno = None # vale True si soy mano en _manoEnSubManoActual o si me llega un canto del otro lado y tengo que responder
  cartasQueTengo = None # una lista que contiene las posibles cartas a jugar. Cuando se juega una, se la saca de la lista
  juegoMio= None		# me parece mejoruno  que _cartaMiaEnSubManoActual = None 
  juegoOtro= None 	# me parece mejor que _cartaContricanteEnSubManoActual = None

  estadoEnvido=ENVIDONOCANTADO
  PtosEnvidoOtro = None
  PtosEnvidoQuerido=None
  PtosEnvidoNQuerido=None
  tengoTantas=None
  intercambiandoTantos=None
  canteMisTantos=None
  cartasEnvido=None
  manoDelOtro=None # cuando se termina la partida y se quizo el envido y no se jugaron todas las cartas, mando a pedir el juego del otro para
                      # ver cuantos puntos tiene y si mintio o no. Es la lista de las cartas del otro.
  envidoNoQuerido=None # vale true si yo dije no quiero. De lo Contrario, False. Esto se usa para cuando termina la mano se contabilizan los puntos
                      # tengo que saber quien no queria el envido asi como tambien quien canto el truco
  
  estadoTruco=TRUCONOCANTADO
  PtosTrucoQuiero=None
  PtostrucoNQuiero=None
  ultimoEstadoTruco=None
  canteTruco=None

  ganePartida=None
  meFuiAlMazo=None

  
  # Ahora definimos el diccionario que contiene las cartas con los niveles
  mazo={Carta(1,Palo.ESPADA):0,Carta(2,Palo.ESPADA):5,Carta(3,Palo.ESPADA):4,Carta(4,Palo.ESPADA):13,Carta(5,Palo.ESPADA):12,Carta(6,Palo.ESPADA):11,
Carta(7,Palo.ESPADA):2,Carta(10,Palo.ESPADA):9,Carta(11,Palo.ESPADA):8,Carta(12,Palo.ESPADA):7,Carta(1,Palo.ORO):6,Carta(2,Palo.ORO):5,Carta(3,Palo.ORO):4,
Carta(4,Palo.ORO):13,Carta(5,Palo.ORO):12,Carta(6,Palo.ORO):11,Carta(7,Palo.ORO):3,Carta(10,Palo.ORO):9,Carta(11,Palo.ORO):8,Carta(12,Palo.ORO):7,
Carta(1,Palo.BASTO):1,Carta(2,Palo.BASTO):5,Carta(3,Palo.BASTO):4,Carta(4,Palo.BASTO):13,Carta(5,Palo.BASTO):12,Carta(6,Palo.BASTO):11,Carta(7,Palo.BASTO):10,
Carta(10,Palo.BASTO):9,Carta(11,Palo.BASTO):8,Carta(12,Palo.BASTO):7,Carta(1,Palo.COPA):6,Carta(2,Palo.COPA):5,Carta(3,Palo.COPA):4,Carta(4,Palo.COPA):13,
Carta(5,Palo.COPA):12,Carta(6,Palo.COPA):11,Carta(7,Palo.COPA):10,Carta(10,Palo.COPA):9,Carta(11,Palo.COPA):8,Carta(12,Palo.COPA):7}

# las dos ultimas variables son las listas que contienen las jugadas de ambos jugadores de tal manera que si el otro juega una carta o yo decido hacerla, se agregan los elementos a la lista.
# en caso de jugar una carta mia tengo que sacarla de _cartasQueTengo

  def __init__(self, cartasIniciales, soyMano):
    self.soyMano = soyMano
    self.cartasQueTengo = cartasIniciales # cartasIniciales es una lista de las tres cartas del juego de la forma (1,'ESPADA')
    self.esMiTurno = soyMano
    self.manoEnSubManoActual=soyMano

    self.juegoMio=[]
    self.juegoOtro=[]

    self.estadoEnvido=ENVIDONOCANTADO
    self.PtosEnvidoOtro = -1
    self.PtosEnvidoQuerido=-1
    self.PtosEnvidoNQuerido=-1
    self.intercambiandoTantos=False
    self.canteMisTantos=False
    self.cartasEnvido=self.calcularEnvido(self.cartasQueTengo) # esto es un par que contiene los puntos y las cartas que forman el envido. Se usa para la verificacion
    self.tengoTantas=_cantoEnvidoTantos('Cantar tantos',-1) #,self.cartasEnvido[0]) # tengoTantas le pide al usuario que diga los puntos que tiene (en este caso le permitiria mentir)
    self.envidoNoQuerido=False
    self.tantosMios=0
    self.manoDelOtro=None
    
    self.estadoTruco=TRUCONOCANTADO
    self.PtosTrucoQuiero=-1
    self.PtostrucoNQuiero=-1
    self.ultimoEstadoTruco=TRUCONOCANTADO
    self.canteTruco=False

    self.ganePartida=None
    self.meFuiAlMazo=0 # 1 si yo me fui. -1 si se fue el otro

  def SoyMano(self):
    """True si soy mano (no soy pie, reparti yo, y fui mano en la primera submano), False si no."""
    return self.soyMano

  def nivelCarta(self,carta):
    #carta es de la forma (1,'ESPADA')
    if isinstance(carta,Carta):
      return self.mazo[carta]
    else:
      raise ValueError('La carta no tiene el formato esperado (1,''ESPADA'')!!')
    
  def ganeMano(self, mano):
    #esta funcion me dice quien gano la mano. Si es uno, gane yo, si es -1 el otro y 0, es parda
      if self.nivelCarta(self.juegoMio[mano])<self.nivelCarta(self.juegoOtro[mano]):
        return 1
      elif self.nivelCarta(self.juegoMio[mano])>self.nivelCarta(self.juegoOtro[mano]):
        return -1
      else: #si fue parda
        return 0
  
  def terminado(self):
    """Si el juego esta terminado o no"""
    """ Esta funcion devuelve None en manoActual si la partida se termino. De lo contrario, la mano que se juega"""
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
        #print "uno: " + str(uno) + "   dos:   " + str(dos) + "   tres:  " + str(tres) + " Cantidad de Manos Ganadas " + str(cont)
        if cont>1:
          self.ganePartida=True
        else:
          self.ganePartida=False
      else:
        if self.ganeMano(1)==0 and self.ganeMano(2)==1:
          self.ganePartida=True
        elif self.ganeMano(1)==0 and self.ganeMano(2)==-1:
          self.ganePartida=False
        elif self.ganeMano(2)==0 and self.ganeMano(0)==1:
          self.ganePartida=True
        elif self.ganeMano(2)==0 and self.ganeMano(0)==-1:
          self.ganePartida=False
      return None
    elif len(self.juegoMio)==len(self.juegoOtro)==2:
      if self.ganeMano(0)==0 and self.ganeMano(1)==1: # la primera fue parda y gano alguno de los dos
        self.ganePartida=True
        return None
      elif self.ganeMano(0)==0 and self.ganeMano(1)==-1: # la primera fue parda y gano alguno de los dos
        self.ganePartida=False
        return None
      elif self.ganeMano(0)==self.ganeMano(1)==-1:
        self.ganePartida=False
        return None
      elif self.ganeMano(0)==self.ganeMano(1)==1:
        self.ganePartida=True
        return None
    elif self.estadoEnvido==FALTAENVIDO:
      print "Cantaron Falta Envido"
      return None
    elif self.estadoTruco==NOQUIEROTRUCO:
      if self.canteTruco==True:
        print "Gane el truco porque el otro no quizo"
      else:
        print "Perdi el truco porque dije que no queria"
      return None
    elif self.meFuiAlMazo==1 or self.meFuiAlMazo==-1 :
      return None
    return False

  def turnoDeJuego(self):
    # cuando soy mano; cuando gane la anterior, o cuando el otro jugo y yo no
    if len(self.juegoMio) > len(self.juegoOtro):
      self.esMiTurno = False
    elif len(self.juegoMio) < len(self.juegoOtro):
      self.esMiTurno = True
    elif len(self.juegoMio) == len(self.juegoOtro) and len(self.juegoOtro) == 0: # caso inicial
      self.manoEnSubManoActual = self.soyMano
      self.esMiTurno = self.soyMano
    elif len(self.juegoMio) == len(self.juegoOtro) and len(self.juegoOtro) > 0: # se termino la mano, me fijo quien la gano e
                                                                                # incremento subManoActual y esMiTurno
      largo=len(self.juegoMio)
      if self.ganeMano(largo-1)==-1:
        self.esMiTurno=False
      elif self.ganeMano(largo-1)==1:
        self.esMiTurno=True
      elif self.ganeMano(largo-1)==0:
        self.esMiTurno=self.soyMano
      else:
        print "es un caso que no tengo contemplado self.ganeMano(largo-1) " + self.ganeMano(largo-1)
        self.esMiTurno=False
        print "es un caso que no tengo contemplado"
    self.manoEnSubManoActual = self.esMiTurno
    return self.esMiTurno

  def turnoDeJuegoEnvido(self):
    if not self.envidoCerrado() and self.estadoEnvido!=ENVIDONOCANTADO:
      self.esMiTurno = not self.esMiTurno
    elif self.estadoEnvido==QUIEROENVIDO:
      if self.intercambiandoTantos == True:
        self.esMiTurno=not self.esMiTurno
      elif self.estadoTruco != TRUCONOCANTADO and not self.trucoCerrado():
        self.esMiTurno = not self.canteTruco
      else:
        self.turnoDeJuego()
    elif self.estadoEnvido == NOQUIEROENVIDO:
      if self.estadoTruco != TRUCONOCANTADO and not self.trucoCerrado():
          self.esMiTurno=not self.canteTruco
      else:
          self.turnoDeJuego()
    return self.esMiTurno
          
    
  def turnoDeJuegoTruco(self):
    if self.trucoCerrado():
      self.turnoDeJuego()
    elif not self.trucoCerrado() and self.estadoTruco!=TRUCONOCANTADO:
      self.esMiTurno = not self.esMiTurno
    return self.esMiTurno


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
    if (self.estadoEnvido==ENVIDONOCANTADO or (self.envidoCerrado() and (self.canteMisTantos==True or self.intercambiandoTantos==False))) and \
    (self.estadoTruco==TRUCONOCANTADO or self.trucoCerrado()) :
      JPosibles=self.cartasQueTengo
    if (len(self.juegoMio)==0 or len(self.juegoOtro)==0) and self.estadoEnvido in CANTOS_ENVIDO and \
       (self.estadoTruco==TRUCONOCANTADO or self.estadoTruco==TRUCO) :
      lista=cantosMayores(self.estadoEnvido)
      if self.estadoEnvido==ENVIDONOCANTADO:
        lista.remove(ENVIDOENVIDO)
      JPosibles=JPosibles + lista
      if self.estadoEnvido!=ENVIDONOCANTADO:
        JPosibles.append(QUIEROENVIDO)
        JPosibles.append(NOQUIEROENVIDO)
    elif (len(self.juegoMio)==0 or len(self.juegoOtro)==0) and self.estadoEnvido == QUIEROENVIDO and self.intercambiandoTantos == True:
        if self.PtosEnvidoOtro > 0:
          JPosibles.append(NOTENGOTANTOS)
        JPosibles.append(self.tengoTantas)
    if (self.envidoCerrado() or self.estadoEnvido==ENVIDONOCANTADO) and self.intercambiandoTantos==False and \
       (self.estadoTruco in CANTOS_TRUCO or self.estadoTruco==QUIEROTRUCO) and self.canteTruco==False:
      JPosibles=JPosibles+cantoSiguiente(self.ultimoEstadoTruco)
      if self.estadoTruco!=TRUCONOCANTADO and not self.trucoCerrado():
        JPosibles.append(QUIEROTRUCO)
        JPosibles.append(NOQUIEROTRUCO)
    if (self.envidoCerrado() or self.estadoEnvido==ENVIDONOCANTADO) and \
       (self.trucoCerrado() or self.estadoTruco==TRUCONOCANTADO) and self.intercambiandoTantos==False:
      JPosibles.append("AL_MAZO")
    return JPosibles # me parece que convendria devolver la lista con las opciones posibles que son las que forman el menu

  def actualizarCanto(self,jugada,jugar): # True si el usuario pide jugar algo y False si recibe una jugada
    if isinstance(jugada,str):
      if jugada == "AL_MAZO":
        if jugar == True:
          self.meFuiAlMazo = 1
        else:
          self.meFuiAlMazo = -1
      return        
    if isinstance(jugada, _cantoEnvidoTantos):  # or jugada==NOTENGOTANTOS: # para el envido cuando hay que cantar los puntos se van a mandar objetos de la clase _cantoEnvidoTanto
                                                # de tal manera que si cuando se dice quiero una manda los puntos en este objeto. El otro responde con otro
                                                #  paquete que contiene 0 si le gane o los puntos si no le gane (el otro puede mandar los puntos sabiendo)
                                                # que igualmente pierde. Quedara en el contrincante pedir que se muestren las cartas y modificar el score
      if jugar == False: #estoy recibiendo la jugada
        self.PtosEnvidoOtro = Tantos(jugada)
        if self.canteMisTantos == True:
          self.intercambiandoTantos = False
      elif jugar == True:
        #pido los puntos que voy a cantar y lo almaceno en la variable que contiene los puntos que cante
        if jugada!=NOTENGOTANTOS:
          jugada.tantos=int(raw_input("Ingrese la cantidad de Puntos a cantar: "))
        self.tengoTantas.tantos = jugada.tantos
        print "     Tengo " + str(self.tengoTantas.tantos)
        self.canteMisTantos=True
      if jugar == True and self.PtosEnvidoOtro >= 0:
        self.intercambiandoTantos=False
      if self.PtosEnvidoOtro >= 0 and self.tengoTantas.tantos >= 0:
        if self.PtosEnvidoOtro > self.tengoTantas.tantos:
          print "Perdi el Envido"
        elif self.PtosEnvidoOtro < self.tengoTantas.tantos:
          print "Gane el Envido"
        elif self.PtosEnvidoOtro == self.tengoTantas.tantos:
          print "Gano la mano porque pardaron en los puntos."
      self.turnoDeJuegoEnvido()
      return True
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
      elif jugada==NOQUIEROENVIDO:
        self.estadoEnvido=NOQUIEROENVIDO
        if jugar==True: #estoy diciendo que no quiero
          self.envidoNoQuerido=True
      if jugada==QUIEROENVIDO:
        self.esMiTurno=self.soyMano
      else:
        self.turnoDeJuegoEnvido()
      return True
    if isinstance(jugada,_cantoTruco):
      if jugada==TRUCO:
        self.PtosTrucoQuerido=2
        self.PtosTrucoNQuerido=1
        self.estadoTruco=TRUCO
        self.ultimoEstadoTruco=TRUCO
        if jugar==True: self.canteTruco=True
        else: self.canteTruco=False
      elif jugada==RETRUCO:
        self.PtosTrucoQuerido=self.PtosTrucoQuerido+1
        self.PtosTrucoNQuerido=self.PtosTrucoNQuerido+1
        self.estadoTruco=RETRUCO
        self.ultimoEstadoTruco=RETRUCO
        if jugar==True: self.canteTruco=True
        else: self.canteTruco=False
      elif jugada==VALE4:
        self.PtosTrucoQuerido=self.PtosTrucoQuerido+1
        self.PtosTrucoNQuerido=self.PtosTrucoNQuerido+1
        self.estadoTruco=VALE4
        self.ultimoEstadoTruco=VALE4
        if jugar==True: self.canteTruco=True
        else: self.canteTruco=False
      elif jugada==QUIEROTRUCO:
        self.estadoTruco=QUIEROTRUCO
      elif jugada==NOQUIEROTRUCO:
        self.estadoTruco=NOQUIEROTRUCO
      self.turnoDeJuegoTruco()
      return True
    raise ValueError('El canto o la carta no tiene el formato establecido o no existe!!')
    return False

    
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
    # Irse al mazo!!!
    
    if not self.esMiTurno:
      return False
    if isinstance(jugada,Carta):
      self.cartasQueTengo.remove(jugada)
      self.juegoMio.append(jugada)
      self.turnoDeJuego()
    elif isinstance(jugada,tuple):
      print "Le paso mis puntos al otro"
    else:
      self.actualizarCanto(jugada,True)
    return  True
      
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
    if isinstance(jugada, Carta):
      self.juegoOtro.append(jugada)
      self.turnoDeJuego()
    else:
      self.actualizarCanto(jugada, False)
    return True
  

  def calcularEnvido(self,juego):
    # calculamos cual es el palo que tiene mas cantidad de cartas
    # si no hay ninguno entonces me fijo en la carta con mas valor
    # basto,copa,oro,espada  cantidad de puntos y cartas que lo forman
    palos={BASTO:[],COPA:[],ORO:[],ESPADA:[]}
    i=0
    maximacarta=juego[0] #self.cartasQueTengo[0]
    while i < len(juego): #self.cartasQueTengo):
      #palos[self.cartasQueTengo[i].palo].append(self.cartasQueTengo[i])
      palos[juego[i].palo].append(juego[i])
      uno=maximacarta.numero
      #dos=self.cartasQueTengo[i].numero
      dos=juego[i].numero
      if maximacarta.numero < juego[i].numero: #self.cartasQueTengo[i].numero:
        maximacarta=juego[i] #self.cartasQueTengo[i]
      i=i+1
    claves=palos.keys()
    maximopalo=claves.pop(0)
    while claves!=[]:
      i=claves.pop(0)
      if len(palos[maximopalo]) < len(palos[i]):
        maximopalo=i
    # ahora cuento la cantidad de puntos que hay
    # si tengo un 10,11,12 vale 20.
    if len(palos[maximopalo])==1:
      return (maximacarta.numero,maximacarta.palo)
    else:
      tantos=20
      indice=0
      palos[maximopalo].sort(cmp= lambda x,y: cmp(x.numero,y.numero) )
      while indice <2:
        carta=palos[maximopalo][len(palos[maximopalo])-indice-1]
        if carta.numero<10:
          tantos=tantos+carta.numero
        indice=indice+1
      return (tantos,palos[maximopalo])

  def ptosGanados(self):
    puntos = 0
    mensajes = ''
    # calculo los puntos del envido en caso que se haya cantado y lo haya ganado
    # y verifico que no me hayan mentido!!
    if self.estadoEnvido == QUIEROENVIDO:
      if self.tengoTantas.tantos > self.PtosEnvidoOtro or \
      (self.tengoTantas.tantos == self.PtosEnvidoOtro and self.soyMano == True):
        if self.cartasEnvido[0] == self.tengoTantas.tantos:
          mensajes = mensajes + "No menti con los puntos. Gane en buena ley\n"
          puntos = puntos + self.PtosEnvidoQuerido
        else:
          mensajes = mensajes + "Mentiste! los puntos se los lleva el otro"
      else:
        #############
        ## TODO: hay que calcular cuanto envido tenia el otro a partir de la lista de cartas del otro (su mano) en self.manoDelOtro
        #############
        if self.manoDelOtro == self.PtosEnvidoOtro: ### ACA TENGO QUE CALCULAR LOS PUNTOS DEL OTRO
          mensajes = mensajes + "El otro me gano en buena ley, no me mintio. Perdi el envido\n"
        else:
          mensajes = mensajes + "Me mintieron!! Los puntos van para mi!!\n"
          puntos = puntos+self.PtosEnvidoQuerido
    if self.estadoEnvido==NOQUIEROENVIDO and self.envidoNoQuerido == False:
      puntos=puntos+self.PtosEnvidoNQuerido # gane yo porque el otro dijo NO QUIERO
      mensajes = mensajes + "Gane Envido por no querido\n"
    # calculo los puntos en caso que se haya cantando truco y los haya ganado
    if self.estadoTruco==QUIEROTRUCO and self.ganePartida==True:
      puntos=puntos+self.PtosTrucoQuerido
      mensajes = mensajes + "Gane truco querido\n"
    if self.estadoTruco==NOQUIEROTRUCO and self.canteTruco==True:
      puntos=puntos+self.PtosTrucoNQuerido # me sumo los puntos porque cante y el otro dijo que no queria
      mensajes = mensajes + "Gane truco por no querido\n"
    if self.estadoTruco==TRUCONOCANTADO and self.ganePartida==True:
      puntos=puntos+1
      mensajes = mensajes + "Gane partida y no se canto truco y se jugo mas de una mano\n"
    # calculo los puntos en caso que el otro se haya ido al mazo. Los puntos del otro son para mi
    if self.estadoTruco==TRUCONOCANTADO and self.estadoEnvido==ENVIDONOCANTADO and self.meFuiAlMazo==-1:
      # el otro se fue. los puntos los gano yo
      if  len(self.juegoMio)==0 or len(self.juegoOtro)==0: 
        puntos=puntos+2 # como si se hubiera cantado envido y truco y no se quisieron los dos
        mensajes = mensajes + "Se fue al mazo si cantar envido y truco\n"
      else:
        puntos = puntos+1 # como si no se quizo el truco
        mensajes = mensajes + "Se fue al mazo si cantar truco\n"
    elif self.estadoEnvido!=ENVIDONOCANTADO and self.estadoTruco==TRUCONOCANTADO and self.meFuiAlMazo==-1:
        puntos = puntos+1
    return mensajes, puntos

  def jugueTodaLaMano(self):
    return len(self.juegoMio)==3

  def manoDelOponente(self, cartas):
    self.manoDelOtro = cartas
    
    