# -*- coding: cp1252 -*-
import Red
import Aes
import Rsa
import Registro
import CartasDesdeArchivo
import struct
from LogicaRedStruct import *
import LogicaRedHandshakeServer
import LogicaRedHandshakeClient


#def ComenzarPartida(ip):
#	raise "No implementado"

#def DejarPartida():
#	raise "No implementado"


## PARA EL LOG DEL MODULO
prefijo = '[' + __name__ + '] ' # nombre del modulo
logger = Registro.newRegistro()
logger.setConsola(False)
logger.setArchivo(False)
DEBUGLOG=lambda x: logger.debug(x)

def activarRegistro(nuevoLogger):
	global logger, DEBUGLOG
	if logger != None:
                DEBUGLOG(prefijo + "Fin del registro")
                logger.setArchivo(None)
        logger = nuevoLogger
	if logger == None:
		DEBUGLOG=lambda x: 0
	else:
		DEBUGLOG=lambda x: logger.debug(x)
	DEBUGLOG(prefijo + "Comienzo del registro")
## FIN LOG DEL MODULO


modo = None

def servirJuego(direccion, puerto):
  """
  Espera una conexion de un cliente en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  pf = prefijo + '[servirJuego()] '

  logger.debug(pf + 'servirJuego(' + str(direccion) + ', ' + str(puerto) + ')')
  global modo
  modo = 'server'

  # 1) B le pide conexion a A
  nroPaso = 1
  logger.info(pf + '--- PASO 1')
  logger.debug(pf + 'Red.EsperarConexion(direccion, puerto)')
  Red.esperarConexion(direccion, puerto)
  # Conexion iniciada
  logger.debug(pf + 'conexion con el cliente iniciada. Iniciando handshake')

  # pasos 2) al 9)
  LogicaRedHandshakeServer.handshakeServer()

  # Handshake completado - ahora entrar al pre-inicio del juego
  pass

  # Pre-inicio completado - preparar para el intermcambio de jugadas
  pass
  
  raise 'No implementado'


def conectarAJuego(direccion, puerto):
  """
  Se conecta a un servidor de Truco Mental en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  pf = prefijo + '[conectarAJuego()] '
  logger.debug(pf + 'conectarAJuego(' + str(direccion) + ', ' + str(puerto) + ')')

  # 1) B le pide conexion a A
  nroPaso = 1
  logger.info(pf + '--- PASO 1')
  logger.debug(pf + 'Red.AbrirConexion(direccion, puerto)')
  Red.abrirConexion(direccion, puerto)
  # Conexion iniciada
  logger.debug(pf + 'conexion con el servidor iniciada. Iniciando handshake')

  # pasos 2) al 9)
  LogicaRedHandshakeClient.handshakeClient()

  # Handshake completado - ahora entrar al pre-inicio del juego
  pass

  # Pre-inicio completado - preparar para el intermcambio de jugadas
  pass

  raise 'No implementado'


def cerrarConexion():
  """
  Cierra la conexion con la contraparte y cancela el juego si no habia terminado.
  """
  pf = prefijo + '[cerrarConexion()] '
  logger.debug(pf + 'cerrarConexion()')
  pass
  raise 'No implementado'


def enviarJugada(jugadas):
  """
  Envia una jugada (lista cartas o cantos) a enviar a la contraparte
  """
  pf = prefijo + '[enviarJugada()] '
  logger.debug(pf + 'rnviarJugada(' + str(jugadas) + ')')
  pass
  raise 'No implementado'


def recibirJugada():
  """
  Espera que la contraparte envie una jugada (lista de cartas o cantos)
  """
  pf = prefijo + '[recibirJugada()] '
  logger.debug(pf + 'recibirJugada()')
  pass
  raise 'No implementado'
	

	
