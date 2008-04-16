# -*- coding: cp1252 -*-
import Red
import Aes
import Rsa
import Registro
import CartasDesdeArchivo
import struct
from LogicaRedParam import *
from LogicaRedStruct import *
import LogicaRedHandshakeServer
import LogicaRedHandshakeClient
from JugadaPaquete import *
from Carta import *
from CantoEnvido import *
from CantoEnvido import _cantoEnvidoTantos
from CantoEnvido import _cantoEnvido
from CantoTruco import *
from CantoTruco import _cantoTruco
#from CantoTruco import *

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
# - Claves para ver la carta jugada por el contrincante
d2 = None
primo = None
keyAes = None

def servirJuego(direccion, puerto):
  """
  Espera una conexion de un cliente en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  global misCartas, rsaContrincante, rsaPropio
  pf = prefijo + '[servirJuego()] '

  logger.debug(pf + 'servirJuego(' + str(direccion) + ', ' + str(puerto) + ')')
  global modo, misCartas, rsaContrincante, rsaPropio, d2, primo, keyAes
  modo = 'server'

  # Espero conexion
  logger.info('Modo server, esperando conexion...', False)
  logger.debug(pf + 'Red.EsperarConexion(' + str(direccion) + ', ' + str(puerto)+ ')')
  Red.esperarConexion(direccion, puerto)
  # Conexion iniciada
  logger.info('conexion entrante!')
  logger.debug(pf + 'conexion con el cliente iniciada. Iniciando handshake')

  # Inicio el handshake
  LogicaRedHandshakeServer.handshakeServer()

  # Handshake completado - preparar para el intermcambio de jugadas
  misCartas =         LogicaRedHandshakeServer.misCartas
  rsaContrincante =   LogicaRedHandshakeServer.rsaContrincante
  rsaPropio =         LogicaRedHandshakeServer.rsaPropio
  d2 =                LogicaRedHandshakeServer.d2a
  primo =             LogicaRedHandshakeServer.primo
  keyAes =            LogicaRedHandshakeServer.keyAes
    
  return True


def conectarAJuego(direccion, puerto):
  """
  Se conecta a un servidor de Truco Mental en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  pf = prefijo + '[conectarAJuego()] '
  logger.debug(pf + 'conectarAJuego(' + str(direccion) + ', ' + str(puerto) + ')')
  global modo, misCartas, rsaContrincante, rsaPropio, d2, primo, keyAes
  modo = 'client'

  # 1) B le pide conexion a A
  logger.info('Modo client, pidiendo conexion...', False)
  logger.debug(pf + 'Red.AbrirConexion(' + str(direccion) + ', ' + str(puerto)+ ')')
  Red.abrirConexion(direccion, puerto)
  # Conexion iniciada
  logger.info('peticion aceptada!')
  logger.debug(pf + 'conexion con el servidor iniciada. Iniciando handshake')

  # pasos 2) al 9)
  LogicaRedHandshakeClient.handshakeClient()

  # Handshake completado - preparar para el intermcambio de jugadas
  misCartas =         LogicaRedHandshakeClient.misCartas
  rsaContrincante =   LogicaRedHandshakeClient.rsaContrincante
  rsaPropio =         LogicaRedHandshakeClient.rsaPropio # n,e,d
  d2 =                LogicaRedHandshakeClient.d2b
  primo =             LogicaRedHandshakeClient.primo
  keyAes =            LogicaRedHandshakeClient.keyAes
  
  return True


def cerrarConexion():
  # Cierra la conexion con la contraparte y cancela el juego si no habia terminado
  pf = prefijo + '[cerrarConexion()] '
  logger.debug(pf + 'cerrarConexion()')
  pass
  Red.cerrarConexion()
  raise 'No implementado'


def enviarJugada(jugada): 
  global misCartas, QUIEROENVIDO
  
  ##  Envia una jugada (lista de cartas o cantos) a la contraparte
  pf = prefijo + '[enviarJugada()] '
  logger.debug(pf + 'enviarJugada()')  
  
  #plain = infint_to_long(jugada) # convierto el texto que me pasaron en un long
  #plain = Rsa.EncriptarTexto(plain, rsaPropio[2], rsaPropio[0])
  
  # Veo que tipo de jugada es y genero el paquete correspondiente
  paquete = None
  if isinstance(jugada, Carta):
    logger.debug(pf + 'estoy enviando una carta')
    carta_firmada = misCartas[jugada]
    paquete = JugadaPaquete(COMANDO_JUEGO_CARTA, carta_firmada, None)
  elif isinstance(jugada, str) and jugada == "AL_MAZO":
    logger.debug(pf + 'estoy enviando que me voy al mazo')
    paquete = JugadaPaquete(COMANDO_ME_VOY_AL_MAZO, None, None)
  elif isinstance(jugada, _cantoEnvidoTantos):
    logger.debug(pf + 'estoy enviando un canto de tantos de envido')
    paquete = JugadaPaquete(COMANDO_CANTO_TANTO, None, jugada.tantos)
  elif isinstance(jugada, _cantoEnvido):
    logger.debug(pf + 'estoy enviando un canto de envido')
    # Veo que tipo de canto de envido es
    comando = None
    if jugada == QUIEROENVIDO:
      comando = COMANDO_QUIERO_ENVIDO
    elif jugada == NOQUIEROENVIDO:
      comando = COMANDO_NO_QUIERO_ENVIDO
    elif jugada == ENVIDO:
      comando = COMANDO_ENVIDO
    elif jugada == ENVIDOENVIDO:
      comando = COMANDO_ENVIDO_ENVIDO
    elif jugada == REALENVIDO:
      comando = COMANDO_REAL_ENVIDO
    elif jugada == FALTAENVIDO:
      comando = COMANDO_FALTA_ENVIDO
    # Ahora que lo tengo, genero el paquete
    paquete = JugadaPaquete(comando, None, None)
  elif isinstance(jugada, _cantoTruco):
    logger.debug(pf + 'estoy enviando un canto de truco')
    # Veo que tipo de canto de truco es
    comando = None
    if jugada == NOQUIEROTRUCO:
      comando = COMANDO_NO_QUIERO_TRUCO
    elif jugada == TRUCO:
      comando = COMANDO_TRUCO
    elif jugada == RETRUCO:
      comando = COMANDO_RETRUCO
    elif jugada == VALE4:
      comando = COMANDO_VALE_CUATRO
    # Ahora que lo tengo, genero el paquete
    paquete = JugadaPaquete(comando, None, None)
  else:
    msg = 'ERROR: Me llego para enviar una jugada que no entiendo: ' + str(jugada)
    logger.debug(pf + msg)
    raise(msg)
   
   
  # Envio el paquete generado  
  Red.enviar(paquete.empaquetar())

  return True


def recibirJugada():
  global d2, primo, keyAes

  ## Espera que la contraparte envie una jugada (lista de cartas o cantos)
  pf = prefijo + '[recibirJugada()] '
  logger.debug(pf + 'recibirJugada()')

  # Recibo el comando de la jugada
  comando = Red.recibir(CANT_CHARS_COMANDO)
  
  # Veo como sigo recibiendo en funcion del comando de la jugada
  jugada = None
  if comando == COMANDO_QUIERO_ENVIDO:
    jugada = QUIEROENVIDO
  elif comando == COMANDO_NO_QUIERO_ENVIDO:
    jugada = NOQUIEROENVIDO
  elif comando == COMANDO_ENVIDO:
    jugada = ENVIDO
  elif comando == COMANDO_ENVIDO_ENVIDO:
    jugada = ENVIDOENVIDO
  elif comando == COMANDO_REAL_ENVIDO:
    jugada = REALENVIDO
  elif comando == COMANDO_FALTA_ENVIDO:
    jugada = FALTAENVIDO
  elif comando == COMANDO_QUIERO_TRUCO:
    jugada = QUIEROTRUCO
  elif comando == COMANDO_NO_QUIERO_TRUCO:
    jugada = NOQUIEROTRUCO
  elif comando == COMANDO_TRUCO:
    jugada = TRUCO
  elif comando == COMANDO_RETRUCO:
    jugada = RETRUCO
  elif comando == COMANDO_VALE_CUATRO:
    jugada = VALE4
  elif comando == COMANDO_JUEGO_CARTA:
    # Recibo la longitud de la carta
    longitud = struct.unpack('L', Red.recibir(CANT_CHARS_LONGITUDES).zfill(CANT_CHARS_LONGITUDES))[0]
    # Levanto la firma de la carta y la desencripto con d2
    carta = infint_to_long(Red.recibir(longitud))
    carta = u128_to_long(Aes.AesDesencriptar(long_to_u128(Rsa.Desencriptar(carta, d2, primo)), keyAes))
    carta = CartasDesdeArchivo.carta(carta)
    jugada = carta
  elif comando == COMANDO_CANTO_TANTO:
    # Levanto los tantos cantados
    jugada = DevolverObjetoTantos(int(Red.recibir(CANT_CHARS_TANTO)))
  elif comando == COMANDO_SON_BUENAS:
    jugada = NOTENGOTANTOS
  elif comando == COMANDO_ME_VOY_AL_MAZO:
    jugada = 'AL_MAZO'
  else:
    msg = 'ERROR: Recibi una jugada desconocida:' + str(comando)
    logger.debug(pf + msg)
    raise (msg)

  #msg = Rsa.DesencriptarTexto(msg, rsaContrincate[1], rsaContrincante[0])
  #plain = long_to_infinit(msg) # convierto el long en el text
  #plain = carta
  
  logger.debug(pf + 'jugada recibida: ' + str(jugada))
  
  return jugada

	
