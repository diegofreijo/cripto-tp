# -*- coding: cp1252 -*-
#
# LogicaRedHandshakeServer.py
#
# Hand-shake del protocolo, del lado del server
# Se asume que hay una conexion abierta (gestionada por el modulo Red)
#
# 20071218 Mat�as Albanesi C�ceres
#
#
import Red
import Aes
import Rsa
import Registro
import CartasDesdeArchivo
from LogicaRedStruct import *
from LogicaRedParam import *

PRIMO_MINIMO = 1L<<33 # minimo valor permitido para el primo P recibido

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


def handshakeServer():
  """
  Tomando una conexion abierta (en el modulo Red) realiza el handshake
  del lado del servidor.
  """
  pf = prefijo + '[handshakeServer()] '
  global nroPaso, keyAes, primo

  # 1) B le pide conexion a A
  # Ya realizado
  pass
  nroPaso = 1
  logger.info(pf + '--- PASO 1 (omitido)')
  #logger.debug(pf + 'Red.EsperarConexion(direccion, puerto)')
  #Red.EsperarConexion(direccion, puerto)
  # Conexion iniciada
  #logger.debug(pf + 'conexion con el cliente iniciada')

  # 2) A genera k para AES y encripta las 40 cartas con k, env�a esto a B
  nroPaso = 2
  logger.info(pf + '--- PASO 2')
  # obtener una clave aleatoria de 128 bits para AES
  keyAes = Azar.Bits(128)
  logger.debug(pf + 'generado K = ' + str(keyAes))
  # encriptar las cartas
  cartas = CartasDesdeArchivo.cartas()
  logger.debug(pf + 'las cartas son: ' + repr(cartas))
  p2_k_cartas = map(lambda x: Aes.AesEncriptar(x, keyAes), cartas)
  logger.debug(pf + 'las cartas encriptadas con K son: ' + repr(p2_k_cartas))
  # enviar
  # formato: tama�o en bytes + lista de valores long ocupando 128 bits cada uno
  msg = _empaquetarListaGenerica(p2_k_cartas, _longtou128)
  msg = _longtou32(len(msg)) + msg
  logger.debug(pf + 'Red.Enviar(cartas encriptadas con K)')
  Red.Enviar(msg)

  # 3) B genera un p primo grande y genera e1b, d1b, e2b, d2b.
  # Env�a a A el p y las cartas (ya encriptadas con k) ahora encriptando
  # con e1b usando RSA
  # formato: tama�o en bytes + lista(p, lista(cartas encrip))
  pass
  nroPaso = 3
  logger.info(pf + '--- PASO 3')
  logger.debug(pf + 'Red.Recibir(4)')
  tamStr = Red.Recibir(4) # tama�o en bytes del resto del mensaje
  tam = _u32tolong(tam)
  if tam <= 0:
    logger.error(pf + 'paso 3, Longitud del mensaje recibido incorrecta')
    raise 'Longitud del mensaje recibido incorrecta'
  logger.debug(pf + 'Red.Recibir('+ str(tam) + ')')
  msg = Red.Recibir(tam)
  if len(msg) < tam:
    logger.error(pf + 'ERROR FATAL: mensaje de longitud menor a la esperada')
    raise 'ERROR FATAL: mensaje de longitud menor a la esperada'
  t = _desempaquetarListaGenerica(msg, lambda x: x) # no desempaquetar los elementos
  # La lista debe tener 2 elementos
  # - el primer elem. es p, un primo grande
  # - el segundo elem. es una lista de cartas
  if len(t) != 2:
    logger.error(pf + 'ERROR FATAL: se esperaban exactamente 2 elementos')
    raise 'ERROR FATAL: se esperaban exactamente 2 elementos'
  primo = _infinttolong(t[0])
  if primo < PRIMO_MINIMO:
    logger.error(pf + 'ERROR FATAL: el primo recibido es demasiado chico')
    raise 'ERROR FATAL: el primo recibido es demasiado chico'
  if not Azar.MillerRabin(primo): # if not Matematica.esPrimo(primo):
    logger.error(pf + 'ERROR FATAL: el primo recibido no es un primo!')
    raise 'ERROR FATAL: el primo recibido no es un primo!'
  # obtener la lista de cartas
  p3_e1b_k_cartas = _desempaquetarListaGenerica(t[1], _infinttolong)
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
  raise 'No implementado'

