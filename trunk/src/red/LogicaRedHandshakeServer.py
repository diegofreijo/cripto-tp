# -*- coding: cp1252 -*-
#
# LogicaRedHandshakeServer.py
#
# Hand-shake del protocolo, del lado del server
# Se asume que hay una conexion abierta (gestionada por el modulo Red)
#
# 20071218 Matías Albanesi Cáceres
#
#
import Red
import Aes
import Rsa
import Registro
import CartasDesdeArchivo
import Azar
from LogicaRedStruct import *
from LogicaRedParam import *



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


# Datos para jugar:
# - Mis cartas: diccionario con las 3 cartas que nos tocaron. Las claves son las cartas y los valores
# asociados son los valores encriptados e2b(k(Ai)) que interpretará la contraparte.
misCartas = None
# 
# - Clave pública RSA de B: (p8_e3b, p8_n3b) para poder verificar los mensajes enviados por B
rsaContrincante = None # tupla (e, n)
#
# - Clave privada RSA propia: (e3a, d3a, n3a) para encriptar mensajes enviados a B
rsaPropio = None # tupla (e, d, n)
#
# - Clave simétrica K: keyAes
keyAes = None
# - Clave para ver la carta jugada por el contrincante
d2a = None
primo = None


def handshakeServer():
  """
  Tomando una conexion abierta (en el modulo Red) realiza el handshake
  del lado del servidor.
  """
  pf = prefijo + '[handshakeServer()] '
  global misCartas, rsaContrincante, rsaPropio, keyAes, d2a, primo

  # 1) B le pide conexion a A
  # Ya realizado
  pass
  nroPaso = 1
  logger.info(pf + '--- PASO 1 (omitido)')


  # 2) A genera k para AES y encripta las 40 cartas con k, envía esto a B
  nroPaso = 2
  logger.info(pf + '--- PASO 2')
  # obtener una clave aleatoria de 128 bits para AES
  keyAesLong = Azar.Bits(128)
  logger.debug(pf + 'keyAesLong = ' + repr(keyAesLong))
  keyAes = long_to_u128(keyAesLong)
  logger.debug(pf + 'keyAes = ' + repr(keyAes))
  # encriptar las cartas
  cartas = CartasDesdeArchivo.cartas()
  logger.debug(pf + 'cartas = ' + repr(cartas))
  cartas_str = map(lambda x: long_to_u128(x), cartas)
  logger.debug(pf + 'cartas_str = ' + repr(cartas_str))
  p2_k_cartas_str = map(lambda x: Aes.AesEncriptar(x, keyAes), cartas_str)
  logger.debug(pf + 'p2_k_cartas_str = ' + repr(p2_k_cartas_str))
  p2_k_cartas = map(infint_to_long, p2_k_cartas_str)
  logger.debug(pf + 'p2_k_cartas = ' + repr(p2_k_cartas))

  # enviar
  # formato: tamaño en bytes + códigos de las cartas, encriptados con AES, como strings de bytes
  msg = empaquetar_Lista_Generica(p2_k_cartas_str) # sin conversion de elementos de la lista
  logger.debug(pf + 'Red.Enviar(p2_k_cartas_str)')
  Red.enviar(msg)


  # 3) B genera un p primo grande y genera e1b, d1b, e2b, d2b.
  # Envía a A el p y las cartas (ya encriptadas con k) ahora encriptando
  # con e1b usando RSA
  # formato: tamaño en bytes + lista(p, cartas encrip)
  pass
  nroPaso = 3
  logger.info(pf + '--- PASO 3')
  t = recibirListaGenerica(Red, logger, pf, 'paso 3, ', 'recibido t == ', infint_to_long) # desempaquetar los strings como longs

  # La lista debe tener 41 elementos
  # - el primer elem. es p, un primo grande
  # - el resto de los elementos son las cartas k(Ci) encriptadas con e1b
  if len(t) != 1 + len(p2_k_cartas_str):
    logger.error(pf + 'ERROR FATAL: se esperaban exactamente ' + str(1 + len(p2_k_cartas_str)) + ' elementos')
    raise 'ERROR FATAL: se esperaban exactamente ' + str(1 + len(p2_k_cartas_str)) + ' elementos'
  primo = t[0]
  if primo < PRIMO_MINIMO:
    logger.error(pf + 'ERROR FATAL: el primo recibido es demasiado chico')
    raise 'ERROR FATAL: el primo recibido es demasiado chico'
  if not Azar.MillerRabin(primo): # if not Matematica.esPrimo(primo):
    logger.error(pf + 'ERROR FATAL: el primo recibido no es un primo!')
    raise 'ERROR FATAL: el primo recibido no es un primo!'
  # obtener la lista de cartas
  p3_e1b_k_cartas = t[1:]
  logger.debug(pf + 'recibido p3_e1b_k_cartas == ' + repr(p3_e1b_k_cartas))
  if len(p3_e1b_k_cartas) != len(p2_k_cartas_str):
    logger.error(pf + 'ERROR FATAL: cantidad de cartas recibidas (' + str(len(p3_e1b_k_cartas)) + ' no coincide con la cantidad esperada (' + str(len(p2_k_cartas_str)) + ')')
    raise 'ERROR FATAL: cantidad de cartas recibidas (' + str(len(p3_e1b_k_cartas)) + ' no coincide con la cantidad esperada (' + str(len(p2_k_cartas_str)) + ')'
  # TODO: chequear que no haya cartas repetidas


  # 4) A usa P para generarse sus propias claves e1a, d1a tq e1a*d1a = 1 (mod p-1)
  #    idem con e2a, d2a
  #    elegir 3 cartas de las enviadas por B y firmarlas con e2a
  #    enviar cada carta como una tupla (e1b(k(CARTAi)), e2a(e1b(k(CARTAi))))
  #    Enviar el resto de las cartas encriptadas con e1a
  e1a, d1a = Rsa.generarEyD(primo, 2) # 2 porque N = p entonces fi(N) = (p-1)*(2-1)
  while True:
    e2a, d2a = Rsa.generarEyD(primo, 2)
    if e2a != e1a and d2a != d1a:
      break
  # elegir cartas para B
  # tomar 3 cartas al azar
  p4_cartasParaB = Azar.extraerDe(p3_e1b_k_cartas, 3)
  # firmarlas con e2a y tuplificar
  p4_cartasParaB_e2a = map(lambda b: (b, Rsa.Encriptar(b, e2a, primo)), p4_cartasParaB)
  # tomar el resto de las cartas
  p4_restoCartas = filter(lambda n: (n not in p4_cartasParaB), p3_e1b_k_cartas)
  # mezclarlas (innecesario)
  p4_restoCartas = Azar.mezclar(p4_restoCartas)
  # encriptarlas con e1a
  p4_restoCartas_e1a = map(lambda r: Rsa.Encriptar(r, e1a, primo), p4_restoCartas)
  # enviar como una lista de 43 elementos
  lista = []
  lista.append(p4_cartasParaB_e2a[0][0])
  lista.append(p4_cartasParaB_e2a[0][1])
  lista.append(p4_cartasParaB_e2a[1][0])
  lista.append(p4_cartasParaB_e2a[1][1])
  lista.append(p4_cartasParaB_e2a[2][0])
  lista.append(p4_cartasParaB_e2a[2][1])
  p4_listaAEnviar = lista + p4_restoCartas_e1a
  # enviar
  # formato: tamaño en bytes + lista de códigos de cartas (convertidos de long a tiras de bytes)
  msg = empaquetar_Lista_Generica(p4_listaAEnviar, long_to_infint)
  logger.debug(pf + 'Red.Enviar(cartas de B encriptadas con e2a y el resto con e1a)')
  Red.enviar(msg)


  # 5) B desencripta las cartas que le envío A, obteniendo k(Bi) para su mano y
  #    e1a(k(Ri)) para el resto
  #    Entonces elige 3 cartas Ai del resto y las desencripta con d1b, de manera
  #    que obtiene e1a(k(Ai)). Envía estas cartas así y también encriptadas con
  #    e2b
  # formato: lista(e1a(k(Ai)), e2b(e1a(k(Ai)), ...)
  pass
  nroPaso = 5
  logger.info(pf + '--- PASO 5')


  # 6) A recibe las cartas y aplica la desencripcion de e1a con d1a.
  #    Luego utiliza K y desencripta las cartas que le tocaron, de manera que se
  #    tienen las cartas Ai elegidas por B
  # obtener las cartas propias
  nroPaso = 6
  logger.info(pf + '--- PASO 6')
  p6_misCartas_encrip = recibirListaGenerica(Red, logger, pf, 'paso 3, ', 'recibido p6_misCartas_encrip == ', infint_to_long) # desempaquetar los strings como longs

  if len(p6_misCartas_encrip) != 6:
    logger.error(pf + 'ERROR FATAL: cantidad de cartas recibidas (' + str(len(p6_misCartas_encrip)) + ' no coincide con la cantidad esperada (6)')
    raise 'ERROR FATAL: cantidad de cartas recibidas (' + str(len(p6_misCartas_encrip)) + ' no coincide con la cantidad esperada (6)'
  # desencriptar las cartas con d1a
  p6_misCartas_d1a = map(lambda n: Rsa.Desencriptar(n, d1a, primo), p6_misCartas_encrip)
  logger.debug(pf + 'p6_misCartas_d1a = ' + repr(p6_misCartas_d1a))
  # ahora tengo k(A1), e2b(k(A1)), k(A2), e2b(k(A2)), idem 3er carta
  # Obtener una lista de 3 tuplas asociando k(Ai) con e2b(k(Ai))
  p6_misCartas_lista = []
  p6_misCartas_lista.append( (p6_misCartas_d1a[0], p6_misCartas_d1a[1]) )
  p6_misCartas_lista.append( (p6_misCartas_d1a[2], p6_misCartas_d1a[3]) )
  p6_misCartas_lista.append( (p6_misCartas_d1a[4], p6_misCartas_d1a[5]) )
  logger.debug(pf + 'p6_misCartas_lista = ' + repr(p6_misCartas_lista))
  # Desencriptar k(Ai) con k para obtener Ai
  # Recordar que hay que convertir a una cadena de bytes (de 16 bytes)
  p6_misCartas = map(lambda t: (Matematica.bytes2long(Aes.AesDesencriptar(Matematica.long2bytes(t[0], 16), keyAes)), t[1]), p6_misCartas_lista)
  logger.debug(pf + 'p6_misCartas = ' + repr(p6_misCartas))
  # chequear que las cartas estén en el mazo original
  misCartas = {}
  logger.debug(pf + 'chequear que las cartas estén en el mazo original')
  for ai, e2bkAi in p6_misCartas:
    logger.debug(pf + 'Ai, e2bkAi = ' + repr(ai) + ', ' + repr(e2bkAi))
    if ai not in cartas:
      logger.error(pf + 'ERROR FATAL: las cartas recibidas del cliente no estan en el mazo original')
      logger.error(pf + 'Carta desconocida: ' + repr(ai))
      raise 'ERROR FATAL: las cartas recibidas del cliente no estan en el mazo original'
    else:
      carta = CartasDesdeArchivo.carta(ai)
      misCartas[carta] = e2bkAi
      logger.info(pf + 'Me toco la carta ' + str(carta) + ' - ' + repr(carta))

  # Por último, enviar k a B
  logger.info(pf + '--- PASO 6 (envio)')
  msg = keyAes # ya es str
  msg = long_to_u32(len(msg)) + msg
  logger.debug(pf + 'Red.Enviar(k)')
  Red.enviar(msg)

  # 7) B recibe k, la utiliza para ver que el mazo es válido y para ver las cartas
  # que le tocaron.
  #  Luego genera una clave RSA clásica (e3b, d3b, n) y envia la parte publica (e3b, n)
  # a A. Tambien envia el mensaje "SOY MANO" encriptado con d3b
  #  Formato: lista(infint(e3b), infint(n), str(d3b("SOY MANO")))
  pass
  nroPaso = 7
  logger.info(pf + '--- PASO 7 (turno de B)')


  # 8) A desencripta con (e3b, n3b) el mensaje encriptado, chequeandolo.
  #    Luego A genera una clave RSA clásica (e3a, d3a, n3a) y envia la parte publica
  #    (e3a, n3a), más el mensaje "SOS MANO" encriptado con d3a
  nroPaso = 8
  logger.info(pf + '--- PASO 8 (recepcion)')
  t = recibirListaGenerica(Red, logger, pf, 'paso 8, ', 'recibido t == ') # no convertir los elementos

  # La lista debe tener 3 elementos
  # - el primer elem. es e3b, un long grande
  # - el segundo elem. es n3b, un long grande
  # - el tercer elem. es un string encriptado con d3b
  if len(t) != 3:
    logger.error(pf + 'ERROR FATAL: se esperaban exactamente 3 elementos')
    raise 'ERROR FATAL: se esperaban exactamente 3 elementos'
  p8_e3b = infint_to_long(t[0])
  logger.debug(pf + 'p8_e3b == ' + repr(p8_e3b))
  p8_n3b = infint_to_long(t[1])
  logger.debug(pf + 'p8_n3b == ' + repr(p8_n3b))
  p8_mensaje_encrip = t[2]
  logger.debug(pf + 'p8_mensaje_encrip == ' + repr(p8_mensaje_encrip))
  p8_mensaje = Rsa.DesencriptarTexto(p8_mensaje_encrip, p8_e3b, p8_n3b)
  logger.debug(pf + 'p8_mensaje == ' + str(p8_mensaje))
  if p8_mensaje != MENSAJE_SOY_MANO:
    mensaje_error = pf + 'ERROR FATAL: mensaje de preinicio de juego incorrecto (se esperaba ' + MENSAJE_SOY_MANO + ')'
    logger.error(mensaje_error)
    raise mensaje_error

  logger.info(pf + '--- PASO 8 (envio)')
  while True:
		n3a, e3a, d3a = Rsa.GenerarClaves(CANT_BITS_PRIMOS)
		# chequear que las claves no coincidan con las de B
		if n3a != p8_n3b and e3a != p8_e3b and d3a != p8_e3b: break
  logger.debug(pf + 'clave RSA generada: (e3a, d3a, n3a) = (' + str(e3a) + ', ' + str(d3a) + ', ' + str(n3a) + ')')
  # generar elementos del mensaje a enviar
  p8_listaParaEnviar = [long_to_infint(e3a), long_to_infint(n3a), Rsa.EncriptarTexto(MENSAJE_SOS_MANO, d3a, n3a)]
  logger.debug(pf + 'p8_listaParaEnviar = ' + repr(p8_listaParaEnviar))
  # empaquetar en una lista
  msg = empaquetar_Lista_Generica(p8_listaParaEnviar) # no convertir los elementos, ya son string
  logger.debug(pf + 'Red.Enviar([e3a, n3a, d3a(SOS_MANO)])')
  Red.enviar(msg)


  # 9) Al recibir B el mensaje de A, chequea que el mensaje encriptado sea
  # la confirmacion de que es mano, el protocolo de handshake esta terminado.
  pass
  nroPaso = 9
  logger.info(pf + '--- PASO 9 (turno de B)')

  logger.info(pf + '--- HANDSHAKE EXITOSO. ES EL TURNO DE LA CONTRAPARTE.')

  # Datos para jugar:
  #
  # - Mis cartas: diccionario con las 3 cartas que nos tocaron. Las claves son las cartas y los valores
  # asociados son los valores encriptados e2b(k(Ai)) que interpretará la contraparte.
  # Ya asignado.
  # 
  # - Clave pública RSA de B: (p8_e3b, p8_n3b) para poder verificar los mensajes enviados por B
  rsaContrincante = (p8_e3b, p8_n3b)
  #
  # - Clave privada RSA propia: (e3a, d3a, n3a) para encriptar mensajes enviados a B
  rsaPropio = (e3a, d3a, n3a)
  #
  # - Clave simétrica K: keyAes
  #   Ya asignado.

  return True
