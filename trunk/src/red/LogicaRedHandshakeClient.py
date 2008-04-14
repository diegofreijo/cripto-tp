# -*- coding: cp1252 -*-
#
# LogicaRedHandshakeClient.py
#
# Hand-shake del protocolo, del lado del cliente
# Se asume que hay una conexion abierta (gestionada por el modulo Red)
#
# 20071220 Matias Albanesi Cáceres
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
# asociados son los valores encriptados e2a(k(Bi)) que interpretará la contraparte.
misCartas = None
# 
# - Clave pública RSA de A: (p9_e3a, p9_n3a) para poder verificar los mensajes enviados por A
rsaContrincante = None # tupla (e, n)
#
# - Clave privada RSA propia: (e3b, d3b, n3b) para encriptar mensajes enviados a A
rsaPropio = None # tupla (e, d, n)
#
# - Clave simétrica K: keyAes
keyAes = None
# - Clave para ver la carta jugada por el contrincante
d2b = None
primo = None

def handshakeClient():
  """
  Tomando una conexion abierta (en el modulo Red) realiza el handshake
  del lado del cliente.
  """
  pf = prefijo + '[handshakeClient()] '
  global misCartas, rsaContrincante, rsaPropio, keyAes, d2b, primo

  # 1) B le pide conexion a A
  # Ya realizado
  pass
  nroPaso = 1
  logger.info(pf + '--- PASO 1 (omitido)')


  # 2) A genera k para AES y encripta las 40 cartas con k, envía esto a B
  pass
  nroPaso = 2
  logger.info(pf + '--- PASO 2')
  #
  # recibir
  # formato: lista de valores long ocupando 128 bits cada uno
  # (los primeros 4 bytes indican el tamanio en bytes del resto del contenido)
  p2_k_cartas = recibirListaGenerica(Red, logger, pf, 'paso 2, ', 'recibido p2_k_cartas == ', u128_to_long)

  # 3) B genera un p primo grande y genera e1b, d1b, e2b, d2b.
  # Envia a A el p y las cartas (ya encriptadas con k) ahora encriptando
  # con e1b usando RSA
  # formato: tamaño en bytes + lista(p, cartas encrip)

  # - generar el primo grande p
  while True:
    primo = Azar.Primo(CANT_BITS_PRIMOS)
    if primo >= PRIMO_MINIMO: break
  logger.debug(pf + 'primo = ' + repr(primo))
  # - generar e1b, d1b
  e1b, d1b = Rsa.generarEyD(primo, 2) # 2 porque N = p entonces fi(N) = (p-1)*(2-1) = (p-1)
  logger.debug(pf + 'e1b = ' + repr(e1b))
  logger.debug(pf + 'd1b = ' + repr(d1b))
  # - generar e2b, d2b (distintos a los anteriores)
  while True:
    e2b, d2b = Rsa.generarEyD(primo, 2)
    if e2b != e1b and d2b != d1b:
      break
  logger.debug(pf + 'e2b = ' + repr(e2b))
  logger.debug(pf + 'd2b = ' + repr(d2b))
  # encriptar con e1b todo el mazo encriptado que se recibió
  # mezclar el mazo enviado por A (opcional)
  #p3_k_cartas = Azar.mezclar(p2_k_cartas)
  p3_k_cartas = p2_k_cartas
  # encriptar las cartas con e1b
  p3_e1b_k_cartas = map(lambda n: Rsa.Encriptar(n, e1b, primo), p3_k_cartas)
  logger.debug(pf + 'p3_e1b_k_cartas = ' + repr(p3_e1b_k_cartas))
  # armar la lista a empaquetar para enviar a A
  t = [primo] + p3_e1b_k_cartas
  msg = empaquetar_Lista_Generica(t, long_to_infint) # enviar convirtiendo los longs a cadenas de bytes
  logger.debug(pf + 'Red.Enviar(primo, p3_e1b_k_cartas)')
  Red.enviar(msg)


  # 4) A usa P para generarse sus propias claves e1a, d1a tq e1a*d1a = 1 (mod p-1)
  #    idem con e2a, d2a
  #    elegir 3 cartas de las enviadas por B y firmarlas con e2a
  #    enviar cada carta como una tupla (e1b(k(CARTAi)), e2a(e1b(k(CARTAi))))
  #    Enviar el resto de las cartas encriptadas con e1a
  # formato: tamaño en bytes + lista de códigos de cartas (convertidos de long a tiras de bytes)
  pass
  nroPaso = 4
  logger.info(pf + '--- PASO 4')
  # se recibieron las cartas como tiras de bytes, convertirlas a long
  p4_listaDe43 = recibirListaGenerica(Red, logger, pf, 'paso 4, ', 'recibido p4_listaDe43 == ', infint_to_long)
  # La lista debe tener 43 elementos
  # - los primeros 6 elementos son las 3 cartas que el servidor selecciona para nosotros, con y
  #   sin encriptación con e2a
  # - el resto de los elementos son las 37 cartas restantes del mazo encriptadas con e1a
  t = p4_listaDe43
  if len(t) != 3 + len(p2_k_cartas):
    logger.error(pf + 'ERROR FATAL: se esperaban exactamente ' + str(3 + len(p2_k_cartas)) + ' elementos')
    raise 'ERROR FATAL: se esperaban exactamente ' + str(3 + len(p2_k_cartas)) + ' elementos'
  # los segundos elementos de cada tupla están encriptados con e2a, y son lo que hay
  # que enviar para hacer una jugada
  p4_e1b_k_cartasParaMi = [ (t[0], t[1]), (t[2], t[3]), (t[4], t[5]) ]
  logger.debug(pf + 'p4_e1b_k_cartasParaMi == ' + repr(p4_e1b_k_cartasParaMi))
  p4_e1a_e1b_k_restoMazo = t[6:]
  logger.debug(pf + 'p4_e1a_e1b_k_restoMazo == ' + repr(p4_e1a_e1b_k_restoMazo))


  # 5) B desencripta las cartas que le envió A, obteniendo k(Bi) para su mano y
  #    e1a(k(Ri)) para el resto
  #    Entonces elige 3 cartas Ai del resto y las desencripta con d1b, de manera
  #    que obtiene e1a(k(Ai)). Envía estas cartas así y también encriptadas con
  #    e2b
  # formato: lista(e1a(k(Ai)), e2b(e1a(k(Ai)), ...)
  nroPaso = 5
  logger.info(pf + '--- PASO 5')
  p5_k_cartasParaMi = map( lambda t: (Rsa.Desencriptar(t[0], d1b, primo), Rsa.Desencriptar(t[1], d1b, primo)), p4_e1b_k_cartasParaMi ) # desencripto
  logger.debug(pf + 'p5_k_cartasParaMi = ' + repr(p5_k_cartasParaMi))
  # elegir cartas para A
  # tomar 3 cartas al azar
  p5_e1a_e1b_k_cartasParaA = Azar.extraerDe(p4_e1a_e1b_k_restoMazo, 3)
  logger.debug(pf + 'p5_e1a_e1b_k_cartasParaA = ' + repr(p5_e1a_e1b_k_cartasParaA))
  # tomar el resto de las cartas
  p5_restoCartas = filter(lambda n: (n not in p5_e1a_e1b_k_cartasParaA), p4_e1a_e1b_k_restoMazo)
  logger.debug(pf + 'p5_restoCartas = ' + repr(p5_restoCartas))
  # desencriptar con d1b las cartas para A
  p5_e1a_k_cartasParaA = map( lambda t: Rsa.Desencriptar(t, d1b, primo), p5_e1a_e1b_k_cartasParaA )
  logger.debug(pf + 'p5_e1a_k_cartasParaA = ' + repr(p5_e1a_k_cartasParaA))
  # encriptar estas cartas con e2b y mandar las dos formas (e1a_k y e2b_e1a_k) a A
  p5_e2b_e1a_k_cartasParaA = map( lambda t: Rsa.Encriptar(t, e2b, primo), p5_e1a_k_cartasParaA)
  logger.debug(pf + 'p5_e2b_e1a_k_cartasParaA = ' + repr(p5_e2b_e1a_k_cartasParaA))
  # armar una lista de 6 cartas intercalando una carta no encriptada con e2b y la misma carta,
  # encriptada con e2b
  p5_listaAEnviar = []
  p5_listaAEnviar.append(p5_e1a_k_cartasParaA[0])
  p5_listaAEnviar.append(p5_e2b_e1a_k_cartasParaA[0])
  p5_listaAEnviar.append(p5_e1a_k_cartasParaA[1])
  p5_listaAEnviar.append(p5_e2b_e1a_k_cartasParaA[1])
  p5_listaAEnviar.append(p5_e1a_k_cartasParaA[2])
  p5_listaAEnviar.append(p5_e2b_e1a_k_cartasParaA[2])
  logger.debug(pf + 'p5_listaAEnviar = ' + repr(p5_listaAEnviar))
  # enviar
  # formato: lista de cartas, convirtiendo los longs a tiras de bytes
  msg = empaquetar_Lista_Generica(p5_listaAEnviar, long_to_infint)
  logger.debug(pf + 'Red.Enviar(cartas de A encriptadas con e1a_k y con e2b_e1a_k)')
  Red.enviar(msg)


  # 6) A recibe las cartas y aplica la desencripcion de e1a con d1a.
  #    Luego utiliza K y desencripta las cartas que le tocaron, de manera que se
  #    tienen las cartas Ai elegidas por B
  #    Por último, A envía k a B
  pass
  nroPaso = 6
  logger.info(pf + '--- PASO 6 (turno de A)')

  # 7) B recibe k, la utiliza para ver que el mazo es válido y para ver las cartas
  # que le tocaron.
  #  Luego genera una clave RSA clásica (e3b, d3b, n3b) y envia la parte publica (e3b, n3b)
  # a A. Tambien envia el mensaje "SOY MANO" encriptado con d3b
  #  Formato: lista(infint(e3b), infint(n), str(d3b("SOY MANO")))
  nroPaso = 7
  logger.info(pf + '--- PASO 7 (recepcion)')
  # (los primeros 4 bytes indican el tamanio en bytes del resto del contenido)
  logger.debug(pf + 'Red.recibir(4)')
  tamStr = Red.recibir(4) # tamanio en bytes del resto del mensaje
  if tamStr == None or len(tamStr) < 4:
    logger.error(pf + 'paso 6, mensaje recibido truncado')
    raise 'Mensaje recibido truncado'
  tam = u32_to_long(tamStr)
  if tam <= 0:
    logger.error(pf + 'paso 6, Longitud del mensaje recibido incorrecta')
    raise 'Longitud del mensaje recibido incorrecta'
  logger.debug(pf + 'Red.recibir('+ str(tam) + ')')
  msg = Red.recibir(tam)
  if len(msg) < tam:
    logger.error(pf + 'ERROR FATAL: mensaje de longitud menor a la esperada')
    raise 'ERROR FATAL: mensaje de longitud menor a la esperada'
  keyAes = msg
  msg = tamStr + msg
  logger.debug(pf + 'recibido mensaje: ' + repr(msg))
  # obtener el valor de K
  logger.debug(pf + 'keyAes == ' + repr(keyAes))
  keyAesLong = infint_to_long(keyAes)
  logger.debug(pf + 'keyAesLong == ' + repr(keyAesLong))
  # TODO: chequear que K sea de 128 bits

  # Con K desencriptar las cartas recibidas en el paso 5
  p7_misCartas = map(lambda t: (Matematica.bytes2long(Aes.AesDesencriptar(Matematica.long2bytes(t[0], 16), keyAes)), t[1]), p5_k_cartasParaMi)
  logger.debug(pf + 'p7_misCartas = ' + repr(p7_misCartas))
  # chequear que las cartas están en el mazo original
  misCartas = {}
  cartas = CartasDesdeArchivo.cartas()
  for bi, e2akBi in p7_misCartas:
    logger.debug(pf + 'Bi, e2akBi = ' + repr(bi) + ', ' + repr(e2akBi))
    if bi not in cartas:
      logger.error(pf + 'ERROR FATAL: las cartas recibidas del servidor no estan en el mazo original')
      logger.error(pf + 'Carta desconocida: ' + repr(bi))
      raise 'ERROR FATAL: las cartas recibidas del servidor no estan en el mazo original'
    else:
      carta = CartasDesdeArchivo.carta(bi)
      misCartas[carta] = e2akBi
      logger.info(pf + 'Me toco la carta ' + str(carta) + ' - ' + repr(carta))

  # generar una clave RSA (e3b, d3b, n)
  n3b, e3b, d3b = Rsa.GenerarClaves(CANT_BITS_PRIMOS)
  logger.debug(pf + 'clave RSA generada: (e3b, d3b, n3b) = (' + str(e3b) + ', ' + str(d3b) + ', ' + str(n3b) + ')')
  # generar elementos del mensaje a enviar
  p7_listaParaEnviar = [long_to_infint(e3b), long_to_infint(n3b), Rsa.EncriptarTexto(MENSAJE_SOY_MANO, d3b, n3b)]
  logger.debug(pf + 'p7_listaParaEnviar = ' + repr(p7_listaParaEnviar))
  # empaquetar en una lista
  msg = empaquetar_Lista_Generica(p7_listaParaEnviar) # no convertir los elementos, ya son string
  logger.debug(pf + 'Red.Enviar([e3b, n3b, d3b(SOY_MANO)])')
  Red.enviar(msg)


  # 8) A desencripta con (e3b, n3b) el mensaje encriptado, chequeandolo.
  #    Luego A genera una clave RSA clásica (e3a, d3a, n3a) y envia la parte publica
  #    (e3a, n3a), más el mensaje "SOS MANO" encriptado con d3a
  pass
  nroPaso = 8
  logger.info(pf + '--- PASO 8 (turno de A)')


  # 9) Al recibir B el mensaje de A, chequea que el mensaje encriptado sea
  # la confirmacion de que es mano, el protocolo de handshake esta terminado.
  nroPaso = 9
  logger.info(pf + '--- PASO 9 (recepcion)')
  # recibir los elementos como una lista de strings
  t = recibirListaGenerica(Red, logger, pf, 'paso 9, ', 'recibido t == ')
  # La lista debe tener 3 elementos
  # - el primer elem. es e3a, un long grande
  # - el segundo elem. es n3a, un long grande
  # - el tercer elem. es un string encriptado con d3a
  if len(t) != 3:
    logger.error(pf + 'ERROR FATAL: se esperaban exactamente 3 elementos')
    raise 'ERROR FATAL: se esperaban exactamente 3 elementos'
  p9_e3a = infint_to_long(t[0])
  logger.debug(pf + 'p9_e3a = ' + repr(p9_e3a))
  p9_n3a = infint_to_long(t[1])
  logger.debug(pf + 'p9_n3a = ' + repr(p9_n3a))
  p9_mensaje_encrip = t[2]
  logger.debug(pf + 'p9_mensaje_encrip = ' + repr(p9_mensaje_encrip))
  p9_mensaje = Rsa.DesencriptarTexto(p9_mensaje_encrip, p9_e3a, p9_n3a)
  logger.debug(pf + 'p9_mensaje = ' + repr(p9_mensaje))
  if p9_mensaje != MENSAJE_SOS_MANO:
    mensaje_error = pf + 'ERROR FATAL: mensaje de preinicio de juego incorrecto (se esperaba ' + MENSAJE_SOY_MANO + ')'
    logger.error(mensaje_error)
    raise mensaje_error
    
  logger.info(pf + '--- HANDSHAKE EXITOSO. ES MI TURNO.')

  # Datos para jugar:
  # - Mis cartas: diccionario con las 3 cartas que nos tocaron. Las claves son las cartas y los valores
  # asociados son los valores encriptados e2a(k(Bi)) que interpretará la contraparte.
  # Ya asignado.
  # 
  # - Clave pública RSA de A: (p9_e3a, p9_n3a) para poder verificar los mensajes enviados por A
  rsaContrincante = (p9_e3a, p9_n3a) # tupla (e, n)
  #
  # - Clave privada RSA propia: (e3b, d3b, n3b) para encriptar mensajes enviados a A
  rsaPropio = (e3b, d3b, n3b) # tupla (e, d, n)
  #
  # - Clave simétrica K: keyAes
  # Ya asignado.

  return True
