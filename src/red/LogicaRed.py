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
# Datos para jugar:
# - Mis cartas: diccionario con las 3 cartas que nos tocaron. Las claves son las cartas y los valores
# asociados son los valores encriptados e2b(k(Ai)) que interpretará la contraparte.
misCartas = None
# - Clave pública RSA de B: (p8_e3b, p8_n3b) para poder verificar los mensajes enviados por B
rsaContrincante = None # tupla (e, n)
# - Clave privada RSA propia: (e3a, d3a, n3a) para encriptar mensajes enviados a B
rsaPropio = None # tupla (e, d, n)


def servirJuego(direccion, puerto):
  """
  Espera una conexion de un cliente en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  global misCartas, rsaContrincante, rsaPropio
  pf = prefijo + '[servirJuego()] '

  logger.debug(pf + 'servirJuego(' + str(direccion) + ', ' + str(puerto) + ')')
  global modo
  modo = 'server'

  # 1) B le pide conexion a A
  logger.info(pf + '--- PASO 1')
  logger.debug(pf + 'Red.EsperarConexion(direccion, puerto)')
  Red.esperarConexion(direccion, puerto)
  # Conexion iniciada
  logger.debug(pf + 'conexion con el cliente iniciada. Iniciando handshake')

  # pasos 2) al 9)
  LogicaRedHandshakeServer.handshakeServer()

  # Handshake completado - preparar para el intermcambio de jugadas
  misCartas = LogicaRedHandshakeServer.misCartas
  rsaContrincante = LogicaRedHandshakeServer.rsaContrincante
  rsaPropio = LogicaRedHandshakeServer.rsaPropio
  
  return True


def conectarAJuego(direccion, puerto):
  """
  Se conecta a un servidor de Truco Mental en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  pf = prefijo + '[conectarAJuego()] '
  logger.debug(pf + 'conectarAJuego(' + str(direccion) + ', ' + str(puerto) + ')')
  global modo
  modo = 'client'

  # 1) B le pide conexion a A
  logger.info(pf + '--- PASO 1')
  logger.debug(pf + 'Red.AbrirConexion(direccion, puerto)')
  Red.abrirConexion(direccion, puerto)
  # Conexion iniciada
  logger.debug(pf + 'conexion con el servidor iniciada. Iniciando handshake')

  # pasos 2) al 9)
  LogicaRedHandshakeClient.handshakeClient()

  # Handshake completado - preparar para el intermcambio de jugadas
  misCartas = LogicaRedHandshakeClient.misCartas
  rsaContrincante = LogicaRedHandshakeClient.rsaContrincante
  rsaPropio = LogicaRedHandshakeClient.rsaPropio # n,e,d

  return True


def cerrarConexion():
  """
  Cierra la conexion con la contraparte y cancela el juego si no habia terminado.
  """
  pf = prefijo + '[cerrarConexion()] '
  logger.debug(pf + 'cerrarConexion()')
  pass
  Red.cerrarConexion()
  raise 'No implementado'


def enviarJugada(jugada):
  """
  Envia una jugada (lista de cartas o cantos) a la contraparte
  """
  pf = prefijo + '[enviarJugada()] '
  logger.debug(pf + 'enviarJugada(' + str(jugada) + ')')
  encrip = Rsa.EncriptarTexto(jugada, rsaPropio[2], rsaPropio[0])
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
	

	
