# -*- coding: cp1252 -*-
import Red
import Aes
import Rsa
import Registro
import CartasDesdeArchivo
import struct


#def ComenzarPartida(ip):
#	raise "No implementado"

#def DejarPartida():
#	raise "No implementado"


## PARA EL LOG DEL MODULO
logger = Registro.newRegistro()
logger.setConsola(False)
logger.setArchivo(False)
DEBUGLOG=lambda x: logger.debug(x)

def ActivarRegistro(nuevoLogger):
	global logger, DEBUGLOG
	if logger != None:
                DEBUGLOG("[LogicaRed.py] Fin del registro")
                logger.setArchivo(None)
        logger = nuevoLogger
	if logger == None:
		DEBUGLOG=lambda x: 0
	else:
		DEBUGLOG=lambda x: logger.debug(x)
	DEBUGLOG("[LogicaRed.py] Comienzo del registro")
## FIN LOG DEL MODULO


def _tolong(nro):
  """
  Empaqueta el nro como un entero largo unsigned de 32 bits
  """
  return struct.pack('L', nro)

def _fromlong(txt32bits):
  """
  Desempaqueta un texto de 32 bits que es un unsigned long a un numero
  """
  return struct.unpack('L', txt32bits)[0]

nroPaso = None
modo = None
keyAes = None

def ServirJuego(direccion, puerto):
  """
  Espera una conexion de un cliente en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  logger.debug('[LogicaRed.py] ServirJuego(' + str(direccion) + ', ' + str(puerto) + ')')
  global nroPaso, modo, keyAes
  modo = 'server'
  nroPaso = 1
  pass
  # 1) B le pide conexion a A
  logger.info('[LogicaRed.py][ServirJuego()] --- PASO 1')
  logger.debug('[LogicaRed.py][ServirJuego()] Red.EsperarConexion(direccion, puerto)')
  Red.EsperarConexion(direccion, puerto)
  # Conexion iniciada
  logger.debug('[LogicaRed.py][ServirJuego()] conexion con el cliente iniciada')
  # 2) A genera k para AES y encripta las 40 cartas con k, envía esto a B
  nroPaso = 2
  logger.info('[LogicaRed.py][ServirJuego()] --- PASO 2')
  # obtener una clave aleatoria de 128 bits para AES
  keyAes = Azar.Bits(128)
  logger.debug('[LogicaRed.py][ServirJuego()] generado K = ' + str(keyAes))
  # encriptar las cartas
  cartas = CartasDesdeArchivo.cartas()
  logger.debug('[LogicaRed.py][ServirJuego()] las cartas son: ' + str(cartas))
  k_cartas = map(lambda x: Aes.AesEncriptar(x, keyAes), cartas)
  logger.debug('[LogicaRed.py][ServirJuego()] las cartas encriptadas con K son: ' + str(k_cartas))
  # enviar
  # formato: long total bytes + string, donde string es repr(k_cartas)
  t = repr(k_cartas)
  t = _tolong(len(t)) + t
  logger.debug('[LogicaRed.py][ServirJuego()] Red.Enviar(cartas encriptadas con K)')
  Red.Enviar(t)
  # 3) B genera un p primo grande y genera e1b, d1b, e2b, d2b.
  # Envía a A el p y las cartas (ya encriptadas con k) ahora encriptando
  # con e1b usando RSA
  nroPaso = 3
  logger.info('[LogicaRed.py][ServirJuego()] --- PASO 3')
  logger.debug('[LogicaRed.py][ServirJuego()] Red.Recibir(4)')
  tam = Red.Recibir(4)
  tam = _fromlong(tam)
  logger.debug('[LogicaRed.py][ServirJuego()] Red.Recibir('+ str(tam) + ')')
  msg = Red.Recibir(tam)
  if len(msg) < 4:
    logger.error('[LogicaRed.py][ServirJuego()] ERROR FATAL: mensaje muy corto')
    raise 'ERROR FATAL: mensaje muy corto'
  cantCartas = _tolong(msg[:4])
  if cantCartas != len(cartas):
    logger.error('[LogicaRed.py][ServirJuego()] ERROR FATAL: cantidad de cartas incorrecta')
  
  raise 'No implementado'


def ConectarAJuego(direccion, puerto):
  """
  Se conecta a un servidor de Truco Mental en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  logger.debug('[LogicaRed.py] ConectarAJuego(' + str(direccion) + ', ' + str(puerto) + ')')
  pass
  raise 'No implementado'


def CerrarConexion():
  """
  Cierra la conexion con la contraparte y cancela el juego si no habia terminado.
  """
  logger.debug('[LogicaRed.py] CerrarConexion()')
  pass
  raise 'No implementado'


def EnviarJugada(jugadas):
  """
  Envia una jugada (lista cartas o cantos) a enviar a la contraparte
  """
  logger.debug('[LogicaRed.py] EnviarJugada(' + str(jugadas) + ')')
  pass
  raise 'No implementado'


def RecibirJugada():
  """
  Espera que la contraparte envie una jugada (lista de cartas o cantos)
  """
  logger.debug('[LogicaRed.py] RecibirJugada()')
  pass
  raise 'No implementado'
	

	
