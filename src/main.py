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
  # Preparar el log seg�n el modo
  if modo == 'S':
    logger.setArchivo("server.log")
  else:
    logger.setArchivo("client.log")
  logger.setNivelArchivo(Registro.DEBUG)
  logger.setNivelConsola(Registro.INFO)
  logger.info('Inicio del registro de comenzarJuego()')
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
    logger.info('Modo server - esperando conexion')
    LogicaRed.servirJuego(direcc, puerto)
    jugador = ManoTruco.ManoTruco(LogicaRedHandshakeServer.misCartas.keys(),True)
    print "Modo: " + str(modo) + "  cartas: " + str(LogicaRedHandshakeServer.misCartas.keys())
  else:
    logger.info('Modo client - realizando conexion')
    LogicaRed.conectarAJuego(direcc, puerto)
    jugador=ManoTruco.ManoTruco(LogicaRedHandshakeClient.misCartas.keys(),False)
    print "Modo: " + str(modo) + "  cartas: " + str(LogicaRedHandshakeClient.misCartas.keys())
  logger.info('Conectado')
	
  
  ## Bucle principal. Juega o espera una jugada.
  # Si no soy mano, espero a que el otro juege para comenzar el bucle
  if not jugador.SoyMano():
    print "Esperando a que el otro juegue..."
    jugadaContrincante = LogicaRed.recibirJugada()
    jugador.recibirJugada(jugadaContrincante)
    print "El contrincante jugo: " + str(jugadaContrincante)
    
  ## Bucle principal
  while jugador.terminado() != None:
    jugadas = jugador.jugadasPosibles()
    MostrarJugadas(jugadas)
    opcionJugada = int(raw_input("Elija opcion a jugar: ")) - 1

    print "Enviando jugada..."
    jugador.jugar(jugadas[opcionJugada])
    LogicaRed.enviarJugada(jugadas[opcionJugada])

    print "Esperando a que el otro juegue..."
    jugadaContrincante = LogicaRed.recibirJugada()
    jugador.recibirJugada(jugadaContrincante)
    print "El contrincante jugo: " + str(jugadaContrincante)

  # Muestro puntos ganados
  jugador.ptosGanados()


def MostrarJugada(opcionJugada):
  if isinstance(opcionJugada, str) and opcionJugada == "AL_MAZO":
    return opcionJugada
  elif isinstance(opcionJugada, _cantoEnvidoTantos):
    return opcionJugada.codigo + str(opcionJugada.valor)
  elif isinstance(opcionJugada, _cantoEnvido):
    return opcionJugada.codigo
  elif isinstance(opcionJugada, _cantoTruco):
    return opcionJugada.codigo
  elif isinstance(opcionJugada, Carta):
    return str(opcionJugada.numero) + ' ' + upper(str(opcionJugada.palo))
  return None
  
  
def MostrarJugadas(jugadas):
  i = 0
  while i < len(jugadas):
    print "\t" + str(i+1) + " - " + MostrarJugada(jugadas[i])
    i = i + 1
  return


def _valElegirIp(texto):
  """
  Chequear si el texto es una direcci�n IP v�lida
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
    msg = 'Modo Server. Elegir la direcci�n ip donde se escuchar�n conexiones (dejar en blanco para cualquier interfase): '
    direcc = "127.0.0.1"#obt_texto(msg, _valElegirIpBlanco)
  else:
    msg = 'Modo Client. Elegir la direcci�n ip a donde hay que conectar (requerido): '
    direcc = "127.0.0.1"#obt_texto(msg, _valElegirIp)
  #
  if modo == 'S':
    msg = 'Modo Server. Elegir el puerto donde se escuchar�n conexiones (requerido): '
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
    # elegir la direcci�n
    elegirIp(modo)
  #

# A menos que se importe este m�dulo desde otro, ir a la selecci�n de modo client/server,
# ip/puerto, y jugar
if __name__ == '__main__':
  elegirModo()
