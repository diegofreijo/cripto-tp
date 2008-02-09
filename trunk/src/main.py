# -*- coding: cp1252 -*-
execfile("..\\setpath.py")
import Registro
import Palo
import Carta
#import Canto
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
CartasDesdeArchivo.inicializar("red\\hasheadas.txt")


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
  #
  logger.info('Iniciando comunicacion')
  if modo == 'S':
    logger.info('Modo server - esperando conexion')
    LogicaRed.servirJuego(direcc, puerto)
    Jugador=ManoTruco.ManoTruco(LogicaRedHandshakeServer.misCartas.keys(),True)
  else:
    logger.info('Modo client - realizando conexion')
    LogicaRed.conectarAJuego(direcc, puerto)
    Jugador=ManoTruco.ManoTruco(LogicaRedHandshakeClient.misCartas.keys(),False)
  logger.info('Conectado')
  while not Jugador.terminado()!=None:
    if Jugador.esMiTurno==True:
      jugadas = Jugador.jugadasPosibles()
      mostrarLista(jugadas)
      print "Elija el numero de la opcion a jugar: (empezando en 0)"
      opcionInt = int(raw_input("> "))
      opcionJugada = jugadas[opcionInt]
      print "Usted eligio jugar  ",
      print str( opcionJugada )
    else:
      print "Tengo que recibir la jugada del otro!"
  
  return

def mostrarLista(jugadas):
  i=0
  while i<len(jugadas):
    print "\t" + str(i) + "- " + str(jugadas[i])
    i=i+1
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
  #

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
    direcc = obt_texto(msg, _valElegirIpBlanco)
  else:
    msg = 'Modo Client. Elegir la direcci�n ip a donde hay que conectar (requerido): '
    direcc = obt_texto(msg, _valElegirIp)
  #
  if modo == 'S':
    msg = 'Modo Server. Elegir el puerto donde se escuchar�n conexiones (requerido): '
  else:
    msg = 'Modo Client. Elegir el puerto a donde conectarse (requerido): '
  puerto = obt_texto(msg, _valElegirIpPuerto)
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
