# -*- coding: cp1252 -*-
execfile("../setpath.py")
from string import *
import Registro
import Palo
from Carta import *
from CantoEnvido import _cantoEnvidoTantos
from CantoEnvido import _cantoEnvido
from CantoTruco import _cantoTruco
import ManoTruco
import CartasDesdeArchivo
import socket
import Red
import LogicaRed
import LogicaRedHandshakeServer
import LogicaRedHandshakeClient
from Score import _Score # agregue esta linea porque me parece que en este main
                    # tenemos que tener uns instancia de Score para ir viendo
                    # como se incrementan los puntos de la partida. Maura
Score=_Score()


# Inicializar log
logger = Registro.newRegistro()
logger.setConsola(True)
logger.setNivelConsola(Registro.DEBUG)

# Inicializar cartas
CartasDesdeArchivo.inicializar("red/hasheadas.txt")


def obt_texto(mensaje, val = None):
  while True:
    try:
      texto=raw_input(mensaje)
    except EOFError:
      print 'EOFError'
      texto=''
    # Si hay una validacion, ejecutarla
    if val == None: break
    (texto, ok) = val(texto)
    if ok: break
  return texto


def comenzarJuego(modo, direcc, puerto):
  print 'Comienzo del juego'
  
  ## Seteo de logueos
  # Preparar el log seg�n el modo
  if modo == 'S':
    logger.setArchivo("server.log")
  else:
    logger.setArchivo("client.log")
  logger.setNivelArchivo(Registro.DEBUG)
  logger.setNivelConsola(Registro.INFO)
  logger.debug('Inicio del registro de comenzarJuego()')
  # Preparar el log en los m�dulos Red y LogicaRed
  Red.activarRegistro(logger)
  LogicaRed.activarRegistro(logger)
  # Preparar el log en el m�dulo LogicaRedHandshakeServer/Client
  if modo == 'S':
    LogicaRedHandshakeServer.activarRegistro(logger)
  else:
    LogicaRedHandshakeClient.activarRegistro(logger)
  logger.info('Iniciando comunicacion')
  
  ## Inicio del Handshake segun el modo
  if modo == 'S':
    LogicaRed.servirJuego(direcc, puerto)
    logger.info('Conectado, soy mano')
  else:
    LogicaRed.conectarAJuego(direcc, puerto)
    logger.info('Conectado, soy pie')

  ## Bucle principal de partida
  partida_terminada = False
  while not partida_terminada:
    
    ## Reparto de nuevo
    logger.debug(' ==== Nueva mano ==== ')
    if modo == 'S':
      LogicaRed.repartir(modo)
      jugador = ManoTruco.ManoTruco(LogicaRedHandshakeServer.misCartas.keys(), True)
      print "Mi mano: "
      for carta in LogicaRedHandshakeServer.misCartas.keys(): print '  ' + str(carta)
    else:
      LogicaRed.repartir(modo)
      jugador = ManoTruco.ManoTruco(LogicaRedHandshakeClient.misCartas.keys(), False)
      print "Mi mano: "
      for carta in LogicaRedHandshakeClient.misCartas.keys(): print '  ' + str(carta)

    #seteo el Score en la mano que se va a jugar para contabilizar los puntos en caso de Falta Envido
    jugador.scoreAcumuladoMio = Score.ptosMios
    jugador.scoreAcumuladoOtro = Score.ptosOtro
    
    ## Bucle principal de mano
    while jugador.terminado() != True:
      # Veo si tengo que jugar yo o mi contrincante
      if jugador.esMiTurno:
        # Me toca
        jugadas = jugador.jugadasPosibles()
        MostrarJugadas(jugadas)
        opcionJugada = -1
        while opcionJugada not in range(0, len(jugadas)):
          opcionJugada = raw_input("Elegi opcion a jugar: ")
          if opcionJugada == '':
            opcionJugada = -1
          else:
            opcionJugada = int(opcionJugada) - 1
        print "     Jugaste " + str(jugadas[opcionJugada])
        jugador.jugar(jugadas[opcionJugada])
        LogicaRed.enviarJugada(jugadas[opcionJugada])
      else:
        # Le toca
        print "Esperando a que el otro juegue..."
        jugadaContrincante = LogicaRed.recibirJugada()
        jugador.recibirJugada(jugadaContrincante)
        print "     El otro jugo " + str(jugadaContrincante)
      # cada vez que se haga o recibe una jugada hay que chequear el Score para ver si se llegaron a los 30 o no...
      
    # Fin de la partida
    print '\n- Fin de la mano -\n'
    
    # Si se canto envido, muestro y veo las manos
    if jugador.envidoCantado():
      # Si soy el servidor, muestro mi mano y espero la del otro; sino, al revez
      if modo == 'S':
        LogicaRed.mostrarMano(LogicaRedHandshakeServer.misCartas.values())
        jugador.manoDelOponente(LogicaRed.verMano())
      else:
        jugador.manoDelOponente(LogicaRed.verMano())
        LogicaRed.mostrarMano(LogicaRedHandshakeClient.misCartas.values())

    # Aca muestro el Score
    print "El estado del Score es:\n"
    mensajes, puntosMios, puntosOtro=jugador.ptosGanados()
    Score.incrementarSocreMio(puntosMios)
    Score.incrementarScoreOtro(puntosOtro)
    print str(Score)

    # Verifico si alguien gano el partido
    if Score.partidoGanado() == -1 or (Score.partidoGanado() == 2 and modo=='C'):
      print " ++ ��Perdi el partido!! ++"
      partida_terminada = True
    elif Score.partidoGanado() == 1 or (Score.partidoGanado() == 2 and modo=='S'):
      print " ++ ��Gane el partido!! ++"
      partida_terminada = True

  # Finalizo la conexion
  LogicaRed.cerrarConexion()
  
  
def MostrarJugadas(jugadas):
  i = 0
  print '\n'
  while i < len(jugadas):
    print "\t" + str(i+1) + " - " + str(jugadas[i])
    i = i + 1
  print
  return


def _valElegirIp(texto):
  # Chequear si el texto es una direcci�n IP v�lida
  try:
    t = socket.inet_aton(texto)
    return (texto, True)
  except:
    print 'Debe ingresar una direccion IP valida'
    return (None, False)



def _valElegirIpBlanco(texto):
  if texto.strip() == '':
    return ('', True)
  else:
    return _valElegirIp(texto)


def _valElegirIpPuerto(texto):
  try:
    i = int(texto)
    if i >= 1024 and i <= 65535:
      return (str(i), True)
  except:
    pass
  # error
  print 'Debe ingresar un numero entero en el rango 1025-65535'
  return (None, False)


def elegirIp(modo):
  if modo == 'S':
    msg = 'Modo Server. Elegir la direccion ip donde se escucharan conexiones (dejar en blanco para cualquier interfaz): '
    direcc = obt_texto(msg, _valElegirIpBlanco)
  else:
    msg = 'Modo Client. Elegir la direccion ip a donde hay que conectar (requerido): '
    direcc = obt_texto(msg, _valElegirIp)
  
  if modo == 'S':
    msg = 'Modo Server. Elegir el puerto donde se escucharan conexiones (requerido): '
  else:
    msg = 'Modo Client. Elegir el puerto a donde conectarse (requerido): '
  puerto = int(obt_texto(msg, _valElegirIpPuerto))
  
  comenzarJuego(modo, direcc, puerto)

  
def _valElegirModo(texto):
  texto = texto.strip().upper()
  if texto in ['C', 'S', '']:
    return (texto, True)
  print 'Debe ingresar C, S o dejar en blanco para salir'
  return (None, False)

def elegirModo():
  while True:
    modo = obt_texto('Elija el modo (Cliente, Servidor, en blanco para salir): ', _valElegirModo)
    if modo == '':
      break
    # elegir la direcci�n
    elegirIp(modo)
  #

# A menos que se importe este m�dulo desde otro, ir a la selecci�n de modo client/server,
# ip/puerto, y jugar
if __name__ == '__main__':
  elegirModo()
