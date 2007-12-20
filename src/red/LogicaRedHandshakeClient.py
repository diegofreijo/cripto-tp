# -*- coding: utf-8 -*-
#
# LogicaRedHandshakeClient.py
#
# Hand-shake del protocolo, del lado del cliente
# Se asume que hay una conexion abierta (gestionada por el modulo Red)
#
# 20071220 Matias Albanesi Caceres
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


nroPaso = None
keyAes = None
primo = None


def handshakeClient():
  """
  Tomando una conexion abierta (en el modulo Red) realiza el handshake
  del lado del cliente.
  """
  pf = prefijo + '[handshakeClient()] '
  global nroPaso, keyAes, primo

  # 1) B le pide conexion a A
  # Ya realizado
  pass
  nroPaso = 1
  logger.info(pf + '--- PASO 1 (omitido)')

  # 2) A genera k para AES y encripta las 40 cartas con k, envia esto a B
  pass
  nroPaso = 2
  logger.info(pf + '--- PASO 2')
  #
  # recibir
  # formato: lista de valores long ocupando 128 bits cada uno
  # (los primeros 4 bytes indican el tamanio en bytes del resto del contenido)
  logger.debug(pf + 'Red.Recibir(4)')
  tamStr = Red.recibir(4) # tamanio en bytes del resto del mensaje
  if len(tamStr) < 4:
    logger.error(pf + 'paso 2, mensaje recibido truncado')
    raise 'paso 2, mensaje recibido truncado'
  tam = u32_to_long(tamStr)
  if tam <= 0:
    logger.error(pf + 'paso 2, Longitud del mensaje recibido incorrecta')
    raise 'Longitud del mensaje recibido incorrecta'
  logger.debug(pf + 'Red.Recibir('+ str(tam) + ')')
  msg = Red.recibir(tam)
  if len(msg) < tam:
    logger.error(pf + 'ERROR FATAL: mensaje de longitud menor a la esperada')
    raise 'ERROR FATAL: mensaje de longitud menor a la esperada'
  msg = tamStr + msg
  logger.debug(pf + 'recibido mensaje: ' + repr(msg))
  p2_k_cartas = desempaquetar_Lista_Generica(msg, u128_to_long)
  logger.debug(pf + 'las cartas encriptadas con K son: ' + repr(p2_k_cartas))


  # 3) B genera un p primo grande y genera e1b, d1b, e2b, d2b.
  # Envia a A el p y las cartas (ya encriptadas con k) ahora encriptando
  # con e1b usando RSA
  # formato: tamanio en bytes + lista(p, lista(cartas encrip))
  # - generar el primo grande p
  while True:
    primo = Azar.Primo(CANT_BITS_RSA)
    if primo >= PRIMO_MINIMO: break
  # - generar e1b, d1b
  e1b, d1b = Rsa.generarEyD(primo, 2) # 2 porque N = p entonces fi(N) = (p-1)*(2-1) = (p-1)
  # - generar e2b, d2b (distintos a los anteriores)
  while True:
    e1a, d1a = Rsa.generarEyD(primo, 2)
    if e2a != e1a and d2a != d1a:
      break
  # encriptar con e1b todo el mazo encriptado que se recibió
  # mezclar el mazo enviado por A (opcional)
  p3_k_cartas = Azar.mezclar(p2_k_cartas)
  # encriptar las cartas con e1b
  p3_e1b_k_cartas = map(lambda n: rsa.EncriptarTexto(n, e1b, primo), p3_k_cartas)



  return




  pass
  nroPaso = 3
  logger.info(pf + '--- PASO 3')
  logger.debug(pf + 'Red.Recibir(4)')
  tamStr = Red.recibir(4) # tamanio en bytes del resto del mensaje
  if len(tamStr) < 4:
    logger.error(pf + 'paso 3, mensaje recibido truncado')
    raise 'paso 3, mensaje recibido truncado'
  tam = u32_to_long(tamStr)
  if tam <= 0:
    logger.error(pf + 'paso 3, Longitud del mensaje recibido incorrecta')
    raise 'Longitud del mensaje recibido incorrecta'
  logger.debug(pf + 'Red.Recibir('+ str(tam) + ')')
  msg = Red.recibir(tam)
  if len(msg) < tam:
    logger.error(pf + 'ERROR FATAL: mensaje de longitud menor a la esperada')
    raise 'ERROR FATAL: mensaje de longitud menor a la esperada'
  t = desempaquetar_Lista_Generica(msg, lambda x: x) # no desempaquetar los elementos
  # La lista debe tener 2 elementos
  # - el primer elem. es p, un primo grande
  # - el segundo elem. es una lista de cartas
  if len(t) != 2:
    logger.error(pf + 'ERROR FATAL: se esperaban exactamente 2 elementos')
    raise 'ERROR FATAL: se esperaban exactamente 2 elementos'
  primo = infint_to_long(t[0])
  if primo < PRIMO_MINIMO:
    logger.error(pf + 'ERROR FATAL: el primo recibido es demasiado chico')
    raise 'ERROR FATAL: el primo recibido es demasiado chico'
  if not Azar.MillerRabin(primo): # if not Matematica.esPrimo(primo):
    logger.error(pf + 'ERROR FATAL: el primo recibido no es un primo!')
    raise 'ERROR FATAL: el primo recibido no es un primo!'
  # obtener la lista de cartas
  p3_e1b_k_cartas = desempaquetar_Lista_Generica(t[1], infint_to_long)
  if len(p3_e1b_k_cartas) != len(p2_k_cartas):
    logger.error(pf + 'ERROR FATAL: cantidad de cartas recibidas (' + str(len(p3_e1b_k_cartas)) + ' no coincide con la cantidad esperada (' + str(len(p2_k_cartas)) + ')')
    raise 'ERROR FATAL: cantidad de cartas recibidas (' + str(len(p3_e1b_k_cartas)) + ' no coincide con la cantidad esperada (' + str(len(p2_k_cartas)) + ')'
  # TODO
  # chequear que no haya cartas repetidas

  # 4) A usa P para generarse sus propias claves e1a, d1a tq e1a*d1a = 1 (mod p-1)
  #    idem con e2a, d2a
  #    elegir 3 cartas de las enviadas por B y firmarlas con e2a
  #    enviar cada carta como una tupla (e1b(k(CARTAi)), e2a(e1b(k(CARTAi))))
  #    Enviar el resto de las cartas encriptadas con e1a
  e1a, d1a = generarEyD(p, 2) # 2 porque N = p entonces fi(N) = (p-1)*(2-1)
  while True:
    e1a, d1a = generarEyD(p, 2)
    if e2a != e1a and d2a != d1a:
      break
  # elegir cartas para B
  # mezclar el mazo enviado por B y tomar las primeras 3 cartas
  p4_cartasParaB = Azar.extraerDe(p3_e1b_k_cartas, 3)
  # firmarlas con e2a y tuplificar
  p4_cartasParaB_e2a = map(lambda b: (b, rsa.Encriptar(b, e2a, primo)), p4_cartasParaB)
  # tomar el resto de las cartas
  p4_restoCartas = filter(lambda n: (n not in p4_cartasParaB), p3_e1b_k_cartas)
  # mezclarlas (innecesario)
  p4_restoCartas = Azar.mezclar(p4_restoCartas)
  # encriptarlas con e1a
  p4_restoCartas_e1a = map(lambda n: rsa.Encriptar(n, e1a, primo), p4_restoCartas)
  # enviar como una lista de 43 elementos
  lista = [].append(p4_cartasParaB_e2a[0][0])
  lista.append(p4_cartasParaB_e2a[0][1])
  lista.append(p4_cartasParaB_e2a[1][0])
  lista.append(p4_cartasParaB_e2a[1][1])
  lista.append(p4_cartasParaB_e2a[2][0])
  lista.append(p4_cartasParaB_e2a[2][1])
  p4_listaAEnviar = lista + p4_restoCartas_e1a
  # enviar
  # formato: tamaÃ±o en bytes + lista de valores long ocupando una cantidad ilimitada de bits cada uno
  msg = empaquetar_Lista_Generica(p4_listaAEnviar, long_to_infint)
  msg = long_to_u32(len(msg)) + msg
  logger.debug(pf + 'Red.Enviar(cartas de B encriptadas con e2a y el resto con e1a)')
  Red.enviar(msg)

  # 5) B desencripta las cartas que le envio A, obteniendo k(Bi) para su mano y
  #    e1a(k(Ri)) para el resto
  #    Entonces elige 3 cartas Ai del resto y las desencripta con d1b, de manera
  #    que obtiene e1a(k(Ai)). Envia estas cartas asi y tambien encriptadas con
  #    e2b
  # formato: lista(e1a(k(Ai)), e2b(e1a(k(Ai)), ...)
  pass
  nroPaso = 5
  logger.info(pf + '--- PASO 5')
  logger.debug(pf + 'Red.Recibir(4)')
  tamStr = Red.recibir(4) # tamanio en bytes del resto del mensaje
  tam = u32_to_long(tam)
  if tam <= 0:
    logger.error(pf + 'paso 5, Longitud del mensaje recibido incorrecta')
    raise 'Longitud del mensaje recibido incorrecta'
  logger.debug(pf + 'Red.Recibir('+ str(tam) + ')')
  msg = Red.recibir(tam)
  if len(msg) < tam:
    logger.error(pf + 'ERROR FATAL: mensaje de longitud menor a la esperada')
    raise 'ERROR FATAL: mensaje de longitud menor a la esperada'

  # 6) A recibe las cartas y aplica la desencripcion de e1a con d1a.
  #    Luego utiliza K y desencripta las cartas que le tocaron, de manera que se
  #    tienen las cartas Ai elegidas por B
  # obtener las cartas propias
  nroPaso = 6
  logger.info(pf + '--- PASO 6')
  p6_misCartas_encrip = desempaquetar_Lista_Generica(msg, infint_to_long)
  if len(p6_misCartas_encrip) != 6:
    logger.error(pf + 'ERROR FATAL: cantidad de cartas recibidas (' + str(len(p6_misCartas_encrip)) + ' no coincide con la cantidad esperada (6)')
    raise 'ERROR FATAL: cantidad de cartas recibidas (' + str(len(p6_misCartas_encrip)) + ' no coincide con la cantidad esperada (6)'
  # desencriptar las cartas con d1a
  p6_misCartas_d1a = map(lambda n: Rsa.Desencriptar(n, d1a, primo), p6_misCartas_encrip)
  # ahora tengo k(A1), e2b(k(A1)), k(A2), e2b(k(A2)), idem 3er carta
  # Obtener una lista de 3 tuplas asociando k(Ai) con e2b(k(Ai))
  p6_misCartas_lista = []
  p6_misCartas_lista.append( (p6_misCartas_d1a[0], p6_misCartas_d1a[1]) )
  p6_misCartas_lista.append( (p6_misCartas_d1a[2], p6_misCartas_d1a[5]) )
  p6_misCartas_lista.append( (p6_misCartas_d1a[4], p6_misCartas_d1a[6]) )
  # Desencriptar k(Ai) con k para obtener Ai
  p6_misCartas = map(lambda kAi, e2bkAi: (Aes.AesDesencriptar(keyAes, kAi), e2bkAi), p6_misCartas_lista)
  # chequear que las cartas estÃ©n en el mazo original
  for ai, e2bkAi in p6_misCartas:
    if ai not in cartas:
      logger.error(pf + 'ERROR FATAL: las cartas recibidas del cliente no estan en el mazo original')
      raise 'ERROR FATAL: las cartas recibidas del cliente no estan en el mazo original'

  # Por Ãºltimo, enviar k a B
  logger.info(pf + '--- PASO 6 (envio)')
  msg = long_to_u128(keyAes)
  msg = long_to_u32(len(msg)) + msg
  logger.debug(pf + 'Red.Enviar(k)')
  Red.enviar(msg)

  # 7) B recibe k, la utiliza para ver que el mazo es vÃ¡lido y para ver las cartas
  # que le tocaron.
  #  Luego genera una clave RSA clasica (e3b, d3b, n) y envia la parte publica (e3b, n)
  # a A. Tambien envia el mensaje "SOY MANO" encriptado con d3b
  #  Formato: lista(infint(e3b), infint(n), str(d3b("SOY MANO")))
  pass
  nroPaso = 7
  logger.info(pf + '--- PASO 7')

  # 8) A desencripta con (e3b, n) el mensaje encriptado, chequeandolo.
  #    Luego A genera una clave RSA clasica (e3a, d3a, n) y envia la parte publica
  #    (e3a, n), mas el mensaje "SOS MANO" encriptado con d3a
  nroPaso = 8
  logger.info(pf + '--- PASO 8')
  #
  logger.debug(pf + 'Red.Recibir(4)')
  tamStr = Red.recibir(4) # tamanio en bytes del resto del mensaje
  tam = u32_to_long(tam)
  if tam <= 0:
    logger.error(pf + 'paso 8, Longitud del mensaje recibido incorrecta')
    raise 'Longitud del mensaje recibido incorrecta'
  logger.debug(pf + 'Red.Recibir('+ str(tam) + ')')
  msg = Red.recibir(tam)
  if len(msg) < tam:
    logger.error(pf + 'ERROR FATAL: mensaje de longitud menor a la esperada')
    raise 'ERROR FATAL: mensaje de longitud menor a la esperada'
  t = desempaquetar_Lista_Generica(msg, lambda x: x) # no desempaquetar los elementos
  # La lista debe tener 3 elementos
  # - el primer elem. es e3b, un long grande
  # - el segundo elem. es n, un long grande
  # - el tercer elem. es un string encriptado con d3b
  if len(t) != 3:
    logger.error(pf + 'ERROR FATAL: se esperaban exactamente 3 elementos')
    raise 'ERROR FATAL: se esperaban exactamente 3 elementos'
  p8_e3b = infint_to_long(t[0])
  p8_nb = infint_to_long(t[1])
  p8_mensaje_encrip = t[2]
  p8_mensaje = Rsa.DesencriptarTexto(p8_mensaje_encrip, p8_e3b, p8_nb)
  if p8_mensaje != MENSAJE_SOY_MANO:
    logger.error(pf + 'ERROR FATAL: mensaje de preinicio de juego incorrecto (se esperaba ' + MENSAJE_SOY_MANO + ')')
    raise 'ERROR FATAL: mensaje de preinicio de juego incorrecto (se esperaba ' + MENSAJE_SOY_MANO + ')'

  logger.info(pf + '--- PASO 8 (envio)')
  while True:
   p8_na, e3a, d3a = Rsa.GenerarClaves(CANT_BITS_RSA)
   # chequear que las claves no coincidan con las de B
   if p8_na != p8_nb and e3a != p8_e3b and d3a != p8_e3b: break
  logger.debug(pf + 'clave RSA generada: (e3a, d3a, n3a) = (' + str(e3a) + ', ' + str(d3a) + ', ' + str(p8_na) + ')')
  # generar elementos del mensaje a enviar
  t = [long_to_infint(e3a), long_to_infint(p8_na), Rsa.EncriptarTexto(MENSAJE_SOS_MANO, d3a, p8_na)]
  # empaquetar en una lista
  msg = empaquetar_Lista_Generica(t, lambda x: x) # no empaquetar los elementos, ya son string
  msg = long_to_u32(len(msg)) + msg
  logger.debug(pf + 'Red.Enviar([e3a, n3a, d3a(SOS_MANO)])')
  Red.enviar(msg)

  # 9) Al recibir B el mensaje de A, chequea que el mensaje encriptado sea
  # la confirmacion de que es mano, el protocolo de handshake esta terminado.
  pass
  nroPaso = 9
  logger.info(pf + '--- PASO 9')

  # Datos para jugar:
  # - cartas para jugar con B: debe enviarse e2b(k(Ai)) cuando se quiera jugar la carta Ai
  #   (p6_misCartas_lista)
  # - la clave (p8_e3b, p8_nb) para poder verificar los mensajes enviados por B
  #
  # De la misma manera, B necesita estos datos para jugar con nosotros:
  # - cartas para jugar con A: son los valores e2A(k(Bi)) cuando B quiera jugar Bi
  #   enviar un cÃ³digo, que debe estar como primer elemento de alguna tupla en p4_cartasParaB_e2a
  # - la clave (e3a, p8_na) para poder verificar los mensajes enviados por A

  raise 'No implementado'

