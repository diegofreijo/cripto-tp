# -*- coding: cp1252 -*-
# cuando se dice quiero o no quiero del envido o truco hay que ver a quien le tocaba jugar. LLamo a terminoSbMano

# El caso es el siguiente. Si me toca jugar, muestro las jugadas posibles y le pido al usuario que seleccione una.
# El usuario le manda la jugada con el metodo Jugar y actualizo los valores de las variables para ver si termino el juego.
# Si no me toca jugar, recibo la jugada que hizo el otro y actualizo los valores de las variables.
# En ambos casos, si se da alguna de las condiciones de la finalizacion de la partida, muestro un cartel y el score final.
# La actualizacion de las variables consiste en corroborar el estado de las cartas, los cantos y a quien le toca el turno.
# Me falta ver como funciona el cambio de los turnos.

# constantes:
FINAL = 30

AL_MAZO_NADIE = 0
AL_MAZO_ME_FUI = 1
AL_MAZO_SE_FUE_EL_OTRO = -1


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

  esMiTurno = None # vale True si soy mano en la Sub-Mano actual o si me llega un canto del otro lado y tengo que responder
  cartasQueTengo = None # una lista que contiene las posibles cartas a jugar. Cuando se juega una, se la saca de la lista
  juegoMio = None	# lista con mis cartas ya bajadas, en el orden en que las jugue
  juegoOtro = None 	# lista con cartas bajadas por el otro

  estadoEnvido=ENVIDONOCANTADO
  PtosEnvidoOtro = None
  PtosEnvidoQuerido=None
  PtosEnvidoNQuerido=None
  tengoTantas=None
  intercambiandoTantos=None
  canteMisTantos=None
  cartasEnvido=None
  canteFaltaEnvido=None
  manoDelOtro=None # cuando se termina la partida y se quiso el envido y no se jugaron todas las cartas, mando a pedir el juego del otro para
                      # ver cuantos puntos tiene y si mintio o no. Es la lista de las cartas del otro.
  envidoNoQuerido=None # vale true si yo dije no quiero. De lo Contrario, False. Esto se usa para cuando termina la mano se contabilizan los puntos
                      # tengo que saber quien no queria el envido asi como tambien quien canto el truco
  
  estadoTruco=TRUCONOCANTADO
  PtosTrucoQuerido=None
  PtosTrucoNQuerido=None
  ultimoEstadoTruco=None
  canteTruco=None

  ganeElTruco = None
  meFuiAlMazo = None

  scoreAcumuladoMio = None
  scoreAcumuladoOtro = None

  # Ahora definimos el diccionario que contiene las cartas con los niveles
  mazo = {Carta(1,Palo.ESPADA):0,Carta(2,Palo.ESPADA):5,Carta(3,Palo.ESPADA):4,Carta(4,Palo.ESPADA):13,Carta(5,Palo.ESPADA):12,Carta(6,Palo.ESPADA):11,
Carta(7,Palo.ESPADA):2,Carta(10,Palo.ESPADA):9,Carta(11,Palo.ESPADA):8,Carta(12,Palo.ESPADA):7,Carta(1,Palo.ORO):6,Carta(2,Palo.ORO):5,Carta(3,Palo.ORO):4,
Carta(4,Palo.ORO):13,Carta(5,Palo.ORO):12,Carta(6,Palo.ORO):11,Carta(7,Palo.ORO):3,Carta(10,Palo.ORO):9,Carta(11,Palo.ORO):8,Carta(12,Palo.ORO):7,
Carta(1,Palo.BASTO):1,Carta(2,Palo.BASTO):5,Carta(3,Palo.BASTO):4,Carta(4,Palo.BASTO):13,Carta(5,Palo.BASTO):12,Carta(6,Palo.BASTO):11,Carta(7,Palo.BASTO):10,
Carta(10,Palo.BASTO):9,Carta(11,Palo.BASTO):8,Carta(12,Palo.BASTO):7,Carta(1,Palo.COPA):6,Carta(2,Palo.COPA):5,Carta(3,Palo.COPA):4,Carta(4,Palo.COPA):13,
Carta(5,Palo.COPA):12,Carta(6,Palo.COPA):11,Carta(7,Palo.COPA):10,Carta(10,Palo.COPA):9,Carta(11,Palo.COPA):8,Carta(12,Palo.COPA):7}

  def __init__(self, cartasIniciales, soyMano):
    self.soyMano = soyMano
    self.cartasQueTengo = cartasIniciales # cartasIniciales es una lista de las tres cartas del juego de la forma (1,'ESPADA')
    self.esMiTurno = soyMano

    self.juegoMio = []
    self.juegoOtro = []

    self.estadoEnvido = ENVIDONOCANTADO
    self.PtosEnvidoOtro = -1
    self.PtosEnvidoQuerido = -1
    self.PtosEnvidoNQuerido = -1
    self.intercambiandoTantos = False
    self.canteMisTantos = False
    self.cartasEnvido = self.calcularEnvido(self.cartasQueTengo) # esto es un par que contiene los puntos y las cartas que forman el envido. Se usa para la verificacion
    self.tengoTantas = _cantoEnvidoTantos('Cantar tantos',-1) # tengoTantas le pide al usuario que diga los puntos que tiene (en este caso le permitiria mentir)
    self.controlPtosOtro = ()
    self.envidoNoQuerido = False
    self.manoDelOtro = None
    self.canteFaltaEnvido = False

    self.estadoTruco = TRUCONOCANTADO
    self.PtosTrucoQuerido = -1
    self.PtosTrucoNQuerido = -1
    self.ultimoEstadoTruco = TRUCONOCANTADO
    self.canteTruco = False

    self.ganeElTruco = None
    self.meFuiAlMazo = AL_MAZO_NADIE

    self.scoreAcumuladoMio = 0
    self.scoreAcumuladoOtro = 0
    
  def SoyMano(self):
    """True si soy mano, False si no."""
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
    # Esta funcion devuelve True si la partida se termino.
    #
    # Cuando se jugaron las 6 cartas. Si hay parda en tercera gana el que gano primera. Me tengo que fijar como se jugaron las cartas
    # Cuando hay parda en primera y se juegan las dos cartas en la segunda. Si hay parda en segunda estoy en el caso anterior
    # Cuando se va al mazo alguno de los dos
    # Cuando se canta falta envido
    cont = 0
    if len(self.juegoMio) == len(self.juegoOtro) == 3:
      # Tengo que contemplar todas las posibles jugadas, ganar dos de tres manos o que alguno o mas sean pardas
      if self.ganeMano(0)!=0 and self.ganeMano(1)!=0 and self.ganeMano(2)!=0: # si ninguna de las tres fue parda cuento la cantidad de manos que gane
        if self.ganeMano(0) == 1: cont = cont + 1
        if self.ganeMano(1) == 1: cont = cont + 1
        if self.ganeMano(2) == 1: cont = cont + 1
        if cont > 1:
          self.ganeElTruco = True
        else:
          self.ganeElTruco = False
      else:
        if self.ganeMano(1)==0 and self.ganeMano(2)==1:
          self.ganeElTruco=True
        elif self.ganeMano(1)==0 and self.ganeMano(2)==-1:
          self.ganeElTruco=False
        elif self.ganeMano(2)==0 and self.ganeMano(0)==1:
          self.ganeElTruco=True
        elif self.ganeMano(2)==0 and self.ganeMano(0)==-1:
          self.ganeElTruco=False
      return True
    elif len(self.juegoMio)==len(self.juegoOtro)==2:
      if self.ganeMano(0)==0 and self.ganeMano(1)==1: # la primera fue parda y gano alguno de los dos
        self.ganeElTruco=True
        return True
      elif self.ganeMano(0)==0 and self.ganeMano(1)==-1: # la primera fue parda y gano alguno de los dos
        self.ganeElTruco=False
        return True
      elif self.ganeMano(0)==self.ganeMano(1)==-1:
        self.ganeElTruco=False
        return True
      elif self.ganeMano(0)==self.ganeMano(1)==1:
        self.ganeElTruco=True
        return True
    elif self.estadoTruco==NOQUIEROTRUCO:
      return True
    elif self.meFuiAlMazo != AL_MAZO_NADIE: # alguien se fue al mazo
      return True
    return False

  def turnoDeJuego(self):
    # cuando soy mano; cuando gane la anterior, o cuando el otro jugo y yo no
    if len(self.juegoMio) > len(self.juegoOtro):
      self.esMiTurno = False
    elif len(self.juegoMio) < len(self.juegoOtro):
      self.esMiTurno = True
    elif len(self.juegoMio) == len(self.juegoOtro) and len(self.juegoOtro) == 0: # caso inicial
      self.esMiTurno = self.soyMano
    elif len(self.juegoMio) == len(self.juegoOtro) and len(self.juegoOtro) > 0: # se termino la mano, me fijo quien la gano
      largo = len(self.juegoMio)
      # actualizo esMiTurno
      if self.ganeMano(largo-1) == -1:
        self.esMiTurno=False
      elif self.ganeMano(largo-1) == 1:
        self.esMiTurno=True
      elif self.ganeMano(largo-1) == 0:
        self.esMiTurno=self.soyMano
      else:
        self.esMiTurno=False
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
    # devuelve una lista con las posibles jugadas
    JPosibles = []
    if (self.estadoEnvido==ENVIDONOCANTADO or \
    (self.envidoCerrado() and \
    (self.canteMisTantos==True or self.intercambiandoTantos==False))) and \
    (self.estadoTruco==TRUCONOCANTADO or self.trucoCerrado()) :
      JPosibles = JPosibles + self.cartasQueTengo
    if (len(self.juegoMio)==0 or len(self.juegoOtro)==0) and self.estadoEnvido in CANTOS_ENVIDO and \
       (self.estadoTruco==TRUCONOCANTADO or self.estadoTruco==TRUCO) :
      lista = cantosMayores(self.estadoEnvido)
      if self.estadoEnvido==ENVIDONOCANTADO:
        lista.remove(ENVIDOENVIDO)
      JPosibles = JPosibles + lista
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
    return JPosibles # lista con las opciones posibles que son las que forman el menu

  def actualizarCanto(self,jugada,jugar): # True si el usuario pide jugar algo y False si recibe una jugada
    if isinstance(jugada,str):
      if jugada == "AL_MAZO":
        if jugar == True:
          self.meFuiAlMazo = AL_MAZO_ME_FUI
        else:
          self.meFuiAlMazo = AL_MAZO_SE_FUE_EL_OTRO
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
      if jugada == ENVIDO:
        self.PtosEnvidoQuerido = 2
        self.PtosEnvidoNQuerido = 1
        self.estadoEnvido = ENVIDO
      elif jugada == ENVIDOENVIDO:
        self.PtosEnvidoQuerido = self.PtosEnvidoQuerido + 2
        self.PtosEnvidoNQuerido = self.PtosEnvidoNQuerido + 1
        self.estadoEnvido = ENVIDOENVIDO
      elif jugada == REALENVIDO:
        self.PtosEnvidoQuerido = self.PtosEnvidoQuerido + 3
        self.PtosEnvidoNQuerido = self.PtosEnvidoNQuerido + 1
        self.estadoEnvido = REALENVIDO
      elif jugada == FALTAENVIDO:
        self.PtosEnvidoNQuerido = self.PtosEnvidoNQuerido + 1
        self.estadoEnvido = FALTAENVIDO
        self.canteFaltaEnvido = True
      elif jugada == QUIEROENVIDO:
        self.estadoEnvido = QUIEROENVIDO
        self.intercambiandoTantos = True
      elif jugada == NOQUIEROENVIDO:
        self.estadoEnvido = NOQUIEROENVIDO
        if jugar == True: #estoy diciendo que no quiero
          self.envidoNoQuerido = True
      if jugada == QUIEROENVIDO:
        self.esMiTurno = self.soyMano
      else:
        self.turnoDeJuegoEnvido()
      return True
    if isinstance(jugada,_cantoTruco):
      if jugada == TRUCO:
        self.PtosTrucoQuerido = 2
        self.PtosTrucoNQuerido = 1
        self.estadoTruco = TRUCO
        self.ultimoEstadoTruco = TRUCO
        if jugar == True:
          self.canteTruco = True
        else:
          self.canteTruco = False
      elif jugada == RETRUCO:
        self.PtosTrucoQuerido = self.PtosTrucoQuerido + 1
        self.PtosTrucoNQuerido = self.PtosTrucoNQuerido + 1
        self.estadoTruco = RETRUCO
        self.ultimoEstadoTruco = RETRUCO
        if jugar == True:
          self.canteTruco = True
        else:
          self.canteTruco = False
      elif jugada == VALE4:
        self.PtosTrucoQuerido = self.PtosTrucoQuerido + 1
        self.PtosTrucoNQuerido = self.PtosTrucoNQuerido + 1
        self.estadoTruco = VALE4
        self.ultimoEstadoTruco = VALE4
        if jugar == True: self.canteTruco=True
        else: self.canteTruco=False
      elif jugada == QUIEROTRUCO:
        self.estadoTruco = QUIEROTRUCO
      elif jugada == NOQUIEROTRUCO:
        self.estadoTruco = NOQUIEROTRUCO
      self.turnoDeJuegoTruco()
      return True
    raise ValueError('El canto o la carta no tiene el formato establecido o no existe!!')
    return False

    
  def jugar(self, jugada): 
    #realizar jugada (o sea, Cantos y/o Cartas) que hace esta parte
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
    if self.esMiTurno:
      return False
    if isinstance(jugada, Carta):
      self.juegoOtro.append(jugada)
      self.turnoDeJuego()
    elif isinstance(jugada,tuple):
      self.controlPtosOtro = jugada
    else:
      self.actualizarCanto(jugada, False)
    return True
  

  def calcularEnvido(self,juego):
    # calculamos cual es el palo que tiene mas cantidad de cartas
    # si no hay ninguno entonces me fijo en la carta con mas valor
    # basto,copa,oro,espada  cantidad de puntos y cartas que lo forman
    if juego == []:
      return (0,[])
    palos = {BASTO:[],COPA:[],ORO:[],ESPADA:[]}
    i = 0
    maximacarta = juego[0]
    while i < len(juego):
      palos[juego[i].palo].append(juego[i])
      if maximacarta.numero < juego[i].numero:
        maximacarta = juego[i]
      i = i + 1
    claves = palos.keys()
    maximopalo = claves.pop(0)
    while claves != []:
      i = claves.pop(0)
      if len(palos[maximopalo]) < len(palos[i]):
        maximopalo = i
    # ahora cuento la cantidad de puntos que hay
    # si tengo un 10,11,12 vale 20.
    if len(palos[maximopalo]) == 1:
      return (maximacarta.numero,maximacarta.palo)
    tantos = 20
    indice = 0
    palos[maximopalo].sort(cmp= lambda x,y: cmp(x.numero,y.numero) )
    while indice < 2:
      carta = palos[maximopalo][len(palos[maximopalo])-indice-1]
      if carta.numero < 10:
        tantos = tantos + carta.numero
      indice = indice + 1
    return (tantos,palos[maximopalo])


  def ptosGanados(self):
    puntosMios = 0
    puntosOtro = 0
    mensajes = ''
    # calculo los puntos del envido en caso que se haya cantado y lo haya ganado
    # y verifico que no me hayan mentido!!
    if self.estadoEnvido == QUIEROENVIDO and self.canteFaltaEnvido == False:
      self.controlPtosOtro = self.calcularEnvido( self.manoDelOtro )
      if self.cartasEnvido[0] > self.controlPtosOtro[0] or \
      ( self.cartasEnvido[0] == self.controlPtosOtro[0] and self.soyMano == True ):
          mensajes = mensajes + "Gane el Envido\n"
          puntosMios = puntosMios + self.PtosEnvidoQuerido
      else:
          puntosOtro=puntosOtro+ self.PtosEnvidoQuerido
          mensajes = mensajes + "Perdi en envido"
            
    if self.estadoEnvido == NOQUIEROENVIDO:
      if self.envidoNoQuerido == False:
        puntosMios = puntosMios + self.PtosEnvidoNQuerido # gane yo porque el otro dijo NO QUIERO
        mensajes = mensajes + "Gane Envido por no querido\n"
      else:
        puntosOtro = puntosOtro + self.PtosEnvidoNQuerido # gano el otro porque dije NO QUIERO
        mensajes = mensajes + "El otro Gano Envido por no querido\n"
        
    # calculo los puntos en caso que se haya cantando truco y los haya ganado
    if self.estadoTruco == QUIEROTRUCO:
      if self.ganeElTruco == True:
        puntosMios = puntosMios + self.PtosTrucoQuerido
        mensajes = mensajes + "Gane truco querido\n"
      else:
        puntosOtro = puntosOtro + self.PtosTrucoQuerido
        mensajes = mensajes + "El otro Gano truco querido\n"
      
    if self.estadoTruco == NOQUIEROTRUCO:
      if self.canteTruco == True:
        puntosMios = puntosMios + self.PtosTrucoNQuerido # me sumo los puntos porque cante y el otro dijo que no queria
        mensajes = mensajes + "Gane truco por no querido\n"
      else:
        puntosOtro=puntosOtro+self.PtosTrucoNQuerido # me sumo los puntos porque cante y el otro dijo que no queria
        mensajes = mensajes + "El otro Gano truco por no querido\n"
        
    if self.estadoTruco == TRUCONOCANTADO and self.meFuiAlMazo == AL_MAZO_NADIE:
      if self.ganeElTruco==True:
        puntosMios = puntosMios + 1
        mensajes = mensajes + "Gane partida y no se canto truco y se jugo mas de una mano\n"
      else:
        puntosOtro = puntosOtro + 1
        mensajes = mensajes + "El otro Gano partida y no se canto truco y se jugo mas de una mano\n"
        
    # calculo los puntos en caso que el otro se haya ido al mazo. Los puntos del otro son para mi
    if self.estadoTruco==TRUCONOCANTADO and self.estadoEnvido==ENVIDONOCANTADO:
      if  len(self.juegoMio)==0 or len(self.juegoOtro)==0:
        if self.meFuiAlMazo == AL_MAZO_SE_FUE_EL_OTRO:
          puntosMios = puntosMios + 2 # como si se hubiera cantado envido y truco y no se quisieron los dos
          mensajes = mensajes + "Se fue al mazo si cantar envido y truco\n"
        elif self.meFuiAlMazo == AL_MAZO_ME_FUI:
          puntosOtro = puntosOtro + 2 # como si se hubiera cantado envido y truco y no se quisieron los dos
          mensajes = mensajes + "Yo me fui al mazo si cantar envido y truco\n"
      else:
        if self.meFuiAlMazo == AL_MAZO_SE_FUE_EL_OTRO:
          puntosMios = puntosMios + 1 # como si no se quiso el truco
          mensajes = mensajes + "Se fue al mazo si cantar truco\n"
        elif self.meFuiAlMazo == AL_MAZO_ME_FUI:
          puntosOtro = puntosOtro + 1 # como si no se quiso el truco
          mensajes = mensajes + "Yo me fui al mazo si cantar truco\n"
          
    if self.estadoEnvido!=ENVIDONOCANTADO and self.estadoTruco==TRUCONOCANTADO:
      print "Se canto el envido y no se canto el truco"
      if self.meFuiAlMazo == AL_MAZO_SE_FUE_EL_OTRO:
        puntosMios = puntosMios + 1
      elif self.meFuiAlMazo == AL_MAZO_ME_FUI:
        puntosOtro = puntosOtro + 1
                     
    if self.estadoEnvido == QUIEROENVIDO and self.canteFaltaEnvido == True:
      self.controlPtosOtro = self.calcularEnvido(self.manoDelOtro)
      if self.scoreAcumuladoMio < 15 and self.scoreAcumuladoOtro < 15:
        # gana la partida el que haya ganado esta falta envido
        if self.cartasEnvido[0] > self.controlPtosOtro[0] or \
        (self.cartasEnvido[0] == self.controlPtosOtro[0] and self.soyMano == True):
            mensajes = mensajes + "Gane el Envido\n"
            puntosMios = puntosMios + FINAL - self.scoreAcumuladoMio
        else:
            puntosOtro = puntosOtro + FINAL - self.scoreAcumuladoOtro
            mensajes = mensajes + "Perdi en envido"
      else:
        # alguno de los dos ya esta en las buenas

        if self.scoreAcumuladoMio > self.scoreAcumuladoOtro:
          self.PtosEnvidoQuerido = FINAL - self.scoreAcumuladoMio
        else:
          self.PtosEnvidoQuerido = FINAL - self.scoreAcumuladoOtro
        # ahora cargo los puntos en donde van
        if self.cartasEnvido[0] > self.controlPtosOtro[0] or \
        (self.cartasEnvido[0] == self.controlPtosOtro[0] and self.soyMano == True):
            mensajes = mensajes + "Gane el Envido\n"
            puntosMios = puntosMios + self.PtosEnvidoQuerido
        else:
            mensajes = mensajes + "Perdi en envido"
            puntosOtro = puntosOtro + self.PtosEnvidoQuerido
    return mensajes, puntosMios, puntosOtro


  def manoDelOponente(self, cartas):
    self.manoDelOtro = cartas

    
  def envidoCantado(self):
    return self.estadoEnvido == QUIEROENVIDO
