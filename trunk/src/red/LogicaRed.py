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
# Proximo numero de secuencia  para las jugadas
secuencia = None


def repartir(modo):
  ## Ejecuta el handshake segun el modo ('S' o 'C')
  
  global misCartas, rsaContrincante, rsaPropio, d2, primo, keyAes, secuencia

  if modo == 'S':
  
    # Inicio el handshake
    LogicaRedHandshakeServer.handshakeServer()

    # Handshake completado - preparar para el intermcambio de jugadas
    misCartas =         LogicaRedHandshakeServer.misCartas
    rsaContrincante =   LogicaRedHandshakeServer.rsaContrincante
    rsaPropio =         LogicaRedHandshakeServer.rsaPropio
    d2 =                LogicaRedHandshakeServer.d2a
    primo =             LogicaRedHandshakeServer.primo
    keyAes =            LogicaRedHandshakeServer.keyAes
    secuencia =         LogicaRedHandshakeServer.secuencia + 1
  
  else:
  
    # Inicio el handshake
    LogicaRedHandshakeClient.handshakeClient()

    # Handshake completado - preparar para el intermcambio de jugadas
    misCartas =         LogicaRedHandshakeClient.misCartas
    rsaContrincante =   LogicaRedHandshakeClient.rsaContrincante
    rsaPropio =         LogicaRedHandshakeClient.rsaPropio
    d2 =                LogicaRedHandshakeClient.d2b
    primo =             LogicaRedHandshakeClient.primo
    keyAes =            LogicaRedHandshakeClient.keyAes
    secuencia =         LogicaRedHandshakeClient.secuencia + 1
    
  return True


def servirJuego(direccion, puerto):
  """
  Espera una conexion de un cliente en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  pf = prefijo + '[servirJuego()] '
  logger.debug(pf + 'servirJuego(' + str(direccion) + ', ' + str(puerto) + ')')
  modo = 'server'

  # Espero conexion
  logger.info('Modo server, esperando conexion...', False)
  logger.debug(pf + 'Red.EsperarConexion(' + str(direccion) + ', ' + str(puerto)+ ')')
  Red.esperarConexion(direccion, puerto)
  # Conexion iniciada
  logger.info('conexion entrante!')
  logger.debug(pf + 'conexion con el cliente iniciada. Iniciando handshake')
  
  return True


def conectarAJuego(direccion, puerto):
  """
  Se conecta a un servidor de Truco Mental en la direccion y puerto especificados.
  Una vez iniciada la conexion, se encarga de realizar el handshake necesario
  para jugar al Truco de manera segura
  """
  pf = prefijo + '[conectarAJuego()] '
  logger.debug(pf + 'conectarAJuego(' + str(direccion) + ', ' + str(puerto) + ')')
  modo = 'client'

  # 1) B le pide conexion a A
  logger.info('Modo client, pidiendo conexion...', False)
  logger.debug(pf + 'Red.AbrirConexion(' + str(direccion) + ', ' + str(puerto)+ ')')
  Red.abrirConexion(direccion, puerto)
  # Conexion iniciada
  logger.info('peticion aceptada!')
  logger.debug(pf + 'conexion con el servidor iniciada. Iniciando handshake')

  return True


def cerrarConexion():
  # Cierra la conexion con la contraparte y cancela el juego si no habia terminado
  pf = prefijo + '[cerrarConexion()] '
  logger.debug(pf + 'cerrarConexion()')
  Red.cerrarConexion()


def enviarJugada(jugada): 
  global misCartas, secuencia, rsaPropio

  ##  Envia una jugada (lista de cartas o cantos) a la contraparte
  pf = prefijo + '[enviarJugada()] '
  logger.debug(pf + 'enviarJugada()')  
  
  # Veo que tipo de jugada es y genero el paquete correspondiente
  paquete = None
  if isinstance(jugada, Carta):
    logger.debug(pf + 'estoy enviando una carta')
    carta_firmada = misCartas[jugada]
    paquete = JugadaPaquete(secuencia, COMANDO_JUEGO_CARTA, carta_firmada, None)
  elif isinstance(jugada, str) and jugada == "AL_MAZO":
    logger.debug(pf + 'estoy enviando que me voy al mazo')
    paquete = JugadaPaquete(secuencia, COMANDO_ME_VOY_AL_MAZO, None, None)
  elif isinstance(jugada, _cantoEnvidoTantos):
    logger.debug(pf + 'estoy enviando un canto de tantos de envido')
    paquete = JugadaPaquete(secuencia, COMANDO_CANTO_TANTO, None, jugada.tantos)
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
    else:
      msg = 'ERROR: Me llego un canto envido que no entiendo: ' + str(jugada)
      logger.debug(pf + msg)
      raise(msg)
    # Ahora que lo tengo, genero el paquete
    paquete = JugadaPaquete(secuencia, comando, None, None)
  elif isinstance(jugada, _cantoTruco):
    logger.debug(pf + 'estoy enviando un canto de truco')
    # Veo que tipo de canto de truco es
    comando = None
    if jugada == QUIEROTRUCO:
      comando = COMANDO_QUIERO_TRUCO
    elif jugada == NOQUIEROTRUCO:
      comando = COMANDO_NO_QUIERO_TRUCO
    elif jugada == TRUCO:
      comando = COMANDO_TRUCO
    elif jugada == RETRUCO:
      comando = COMANDO_RETRUCO
    elif jugada == VALE4:
      comando = COMANDO_VALE_CUATRO
    else:
      msg = 'ERROR: Me llego un canto truco que no entiendo: ' + str(jugada)
      logger.debug(pf + msg)
      raise(msg)
    # Ahora que lo tengo, genero el paquete
    paquete = JugadaPaquete(secuencia, comando, None, None)
  else:
    msg = 'ERROR: Me llego para enviar una jugada que no entiendo: ' + str(jugada)
    logger.debug(pf + msg)
    raise(msg)
   
  # Firmo y envio el paquete generado 
  Red.enviar(paquete.empaquetar(rsaPropio[1], rsaPropio[2]))
  logger.debug(pf + 'Envie el paquete numero ' + str(secuencia))
  
  # Incremento el numero de secuencia
  secuencia = secuencia + 1

  return True


def recibirJugada():
  global d2, primo, keyAes, secuencia, rsaContrincante

  ## Espera que la contraparte envie una jugada (lista de cartas o cantos)
  pf = prefijo + '[recibirJugada()] '
  logger.debug(pf + 'recibirJugada()')
  
  # Recibo la longitud del paquete firmado, y el paquete firmado
  longitud = Red.recibir(CANT_CHARS_LONGITUDES)
  longitud = struct.unpack('L', longitud)[0]
  paquete = Red.recibir(longitud)
  
  # Desencripto el paquete
  paquete = Rsa.DesencriptarTexto(paquete, rsaContrincante[0], rsaContrincante[1])
  
  # Inicializo el puntero de lectura en el comienzo
  p = 0
  
  # Verifico el numero de seccuencia del paquete
  secuencia_paquete = infint_to_long(paquete[p : p + CANT_CHARS_SECUENCIA].zfill(CANT_CHARS_SECUENCIA))
  p = p + CANT_CHARS_SECUENCIA
  if secuencia_paquete != secuencia:
    msg = 'ERROR: Me llego el numero de secuencia ' + str(secuencia_paquete) + ' cuando me debio haber llegado ' + str(secuencia)
    logger.debug(msg)
    cerrarConexion()
    raise(msg)
  else:
    logger.debug(pf + 'Recibiendo paquete numero ' + str(secuencia) + '...')
    # Incremento el numero de secuenciamiento
    secuencia = secuencia + 1

  # Recibo el comando de la jugada
  comando = paquete[p : p + CANT_CHARS_COMANDO]
  p = p + CANT_CHARS_COMANDO
  
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
    longitud = struct.unpack('L', paquete[p : p + CANT_CHARS_LONGITUDES])[0]
    p = p + CANT_CHARS_LONGITUDES
    # Levanto la firma de la carta y la desencripto con d2
    carta = infint_to_long(paquete[p : p + longitud])
    p = p + longitud
    carta = u128_to_long(Aes.AesDesencriptar(long_to_u128(Rsa.Desencriptar(carta, d2, primo)), keyAes))
    carta = CartasDesdeArchivo.carta(carta)
    jugada = carta
  elif comando == COMANDO_CANTO_TANTO:
    # Levanto los tantos cantados
    jugada = DevolverObjetoTantos(int(paquete[p : p + CANT_CHARS_TANTO]))
    p = p + CANT_CHARS_TANTO
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
  
  
  logger.debug(pf + 'Secuencia recibida: ' + str(secuencia-1))
  #logger.debug(pf + 'Comando recibido: ' + str(jugada))
  logger.debug(pf + 'Jugada recibida: ' + str(jugada))
  #logger.debug(pf + 'Tantos recibidos: ' + str(jugada))
  
  return jugada


def mostrarMano(cartas):
    # Le envio al contrincante mi mano para que pueda verificar mi envido
    
    # Meto el comando
    paquete = COMANDO_TE_MUESTRO_MI_MANO
    
    # Agrego las 3 cartas con sus longitudes
    carta_str = long_to_infint(cartas[0])
    paquete = paquete + struct.pack('L', len(carta_str)) + carta_str
    
    carta_str = long_to_infint(cartas[1])
    paquete = paquete + struct.pack('L', len(carta_str)) + carta_str
    
    carta_str = long_to_infint(cartas[2])
    paquete = paquete + struct.pack('L', len(carta_str)) + carta_str
    
    # Firmo el paquete y le agrego la longitud total
    paquete = Rsa.EncriptarTexto(paquete, rsaPropio[1], rsaPropio[2])
    longitud = struct.pack('L', len(paquete)).zfill(CANT_CHARS_LONGITUDES)
    paquete = longitud + paquete
    
    # Y lo envio
    Red.enviar(paquete)
    
    
def verMano():
  # Recibo la mano del otro para poder verificar su envido
  
  # Recibo la longitud del paquete firmado, y el paquete firmado
  longitud = Red.recibir(CANT_CHARS_LONGITUDES)
  longitud = struct.unpack('L', longitud)[0]
  paquete = Red.recibir(longitud)
  
  # Desencripto el paquete
  paquete = Rsa.DesencriptarTexto(paquete, rsaContrincante[0], rsaContrincante[1])
    
  # Inicializo el puntero de lectura en el comienzo
  p = 0
  
  # Verifico el comando, no sea cosa que me quiso mandar otra cosa
  comando = paquete[p : p + CANT_CHARS_COMANDO]
  p = p + CANT_CHARS_COMANDO
  if comando != COMANDO_TE_MUESTRO_MI_MANO:
    raise('ERROR: esperaba la mano del contrincante pero me mando este comando: ' + str(comando))
  
  # Recibo las cartas
  cartas = []
  for i in range(3):
    # Recibo la longitud de la carta
    longitud = struct.unpack('L', paquete[p : p + CANT_CHARS_LONGITUDES])[0]
    p = p + CANT_CHARS_LONGITUDES
    # Levanto la firma de la carta y la desencripto con d2
    carta = infint_to_long(paquete[p : p + longitud])
    p = p + longitud
    carta = u128_to_long(Aes.AesDesencriptar(long_to_u128(Rsa.Desencriptar(carta, d2, primo)), keyAes))
    carta = CartasDesdeArchivo.carta(carta)
    cartas.append(carta)
    
  return cartas

 