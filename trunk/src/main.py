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
  # Preparar el log según el modo
  if modo == 'S':
    logger.setArchivo("server.log")
  else:
    logger.setArchivo("client.log")
  logger.setNivelArchivo(Registro.DEBUG)
  logger.setNivelConsola(Registro.INFO)
  logger.debug('Inicio del registro de comenzarJuego()')
  # Preparar el log en los módulos Red y LogicaRed
  Red.activarRegistro(logger)
  LogicaRed.activarRegistro(logger)
  # Preparar el log en el módulo LogicaRedHandshakeServer/Client
  if modo == 'S':
    LogicaRedHandshakeServer.activarRegistro(logger)
  else:
    LogicaRedHandshakeClient.activarRegistro(logger)
  logger.info('Iniciando comunicacion')
  
  ## Inicio del Handshake segun el modo
  if modo == 'S':
    LogicaRed.servirJuego(direcc, puerto)
    jugador = ManoTruco.ManoTruco(LogicaRedHandshakeServer.misCartas.keys(), True)
    print "Mi mano: "
    for carta in LogicaRedHandshakeServer.misCartas.keys(): print '  ' + str(carta)
    logger.info('Conectado, soy mano')
  else:
    LogicaRed.conectarAJuego(direcc, puerto)
    jugador = ManoTruco.ManoTruco(LogicaRedHandshakeClient.misCartas.keys(), False)
    print "Mi mano: "
    for carta in LogicaRedHandshakeClient.misCartas.keys(): print '  ' + str(carta)
    logger.info('Conectado, soy pie')
	  
  ## Bucle principal
  while jugador.terminado() != None:
    # Armo las validaciones para ver a quien le toca
    me_toca_envido = not jugador.envidoCerrado() and jugador.turnoDeJuegoEnvido()
    me_toca_truco = not jugador.trucoCerrado() and jugador.turnoDeJuegoTruco()
    # Veo si tengo que jugar yo o mi contrincante
    if jugador.turnoDeJuego() or me_toca_envido or me_toca_truco:
      # Me toca
      jugadas = jugador.jugadasPosibles()
      MostrarJugadas(jugadas)
      opcionJugada = -1
      while opcionJugada not in range(0, len(jugadas)):
        opcionJugada = raw_input("Elija opcion a jugar: ")
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

  # Fin de la partida
  print '\n- Fin de la partida -\n'
  
  # Muestro puntos ganados
  mensajes, puntos = jugador.ptosGanados()
  print mensajes
  print 'Puntos ganados: ' + str(puntos)

  # Finalizo la conexion
  LogicaRed.cerrarConexion()
  
  
def MostrarJugadas(jugadas):
  i = 0
  print
  while i < len(jugadas):
    print "\t" + str(i+1) + " - " + str(jugadas[i])
    i = i + 1
  print
  return


def _valElegirIp(texto):
  """
  Chequear si el texto es una dirección IP válida
  """
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
    msg = 'Modo Server. Elegir la dirección ip donde se escucharán conexiones (dejar en blanco para cualquier interfase): '
    direcc = "127.0.0.1"#obt_texto(msg, _valElegirIpBlanco)
  else:
    msg = 'Modo Client. Elegir la dirección ip a donde hay que conectar (requerido): '
    direcc = "127.0.0.1"#obt_texto(msg, _valElegirIp)
  #
  if modo == 'S':
    msg = 'Modo Server. Elegir el puerto donde se escucharán conexiones (requerido): '
  else:
    msg = 'Modo Client. Elegir el puerto a donde conectarse (requerido): '
  puerto = 11111#obt_texto(msg, _valElegirIpPuerto)
  puerto = int(puerto)
  #
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
    # elegir la dirección
    elegirIp(modo)
  #

# A menos que se importe este módulo desde otro, ir a la selección de modo client/server,
# ip/puerto, y jugar
if __name__ == '__main__':
  elegirModo()
