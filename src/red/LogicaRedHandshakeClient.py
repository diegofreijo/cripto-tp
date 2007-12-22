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
  if tamStr == None or len(tamStr) < 4:
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
  # se recibieron las cartas como strings de 128 bits c/u, convertirlas a long
  p2_k_cartas, tmp = desempaquetar_Lista_Generica(msg, u128_to_long)
  logger.debug(pf + 'recibido p2_k_cartas == ' + repr(p2_k_cartas))
  if tmp != '':
    logger.warn(pf + 'hay datos sobrantes al final del mensaje recibido. Se ignoran esos datos.')


  # 3) B genera un p primo grande y genera e1b, d1b, e2b, d2b.
  # Envia a A el p y las cartas (ya encriptadas con k) ahora encriptando
  # con e1b usando RSA
  # formato: tamaño en bytes + lista(p, cartas encrip)

  # - generar el primo grande p
  while True:
    #primo = Azar.Primo(CANT_BITS_RSA)
    primo = 138840242304691757590023665847446776817598442866265113948085287165398284915819274685055955941003493073746599347005050384080452466398775813599382092517423548091124621361229576163611353039506204507457079134949940379860948903986001100674364455764235458126250127210569882368429663718956895185189386532208487637179
    if primo >= PRIMO_MINIMO: break
  logger.debug(pf + 'primo = ' + repr(primo))
  # - generar e1b, d1b
  #e1b, d1b = Rsa.generarEyD(primo, 2) # 2 porque N = p entonces fi(N) = (p-1)*(2-1) = (p-1)
  e1b = 25261129233546366239000711258765890878154280731632357063850830772921569144120163159891847665475984550223585490471831861707028884954588142104689396180765239749584971174398742697371256201427146212084793574724656554872815877201051081516330429228929501060276190638579326346940551015518000874430228023794076619237
  d1b = 55469733050751556334887129895050081961458054304101178843311861100448787538821316851214183384509616274264381564700424425116771261044472078026359622971420625782369264447076816529175832499647945955197658267901667396561213380622294751600696944942896583186534272366286455577522452613555761593283387791225540799429
  logger.debug(pf + 'e1b = ' + repr(e1b))
  logger.debug(pf + 'd1b = ' + repr(d1b))
  # - generar e2b, d2b (distintos a los anteriores)
  while True:
    #e2b, d2b = Rsa.generarEyD(primo, 2)
    e2b = 77228495887273096394999494922045365713843816690381277274999463142039579118667119677873729117261834284978584451609904311341496458202352726720496674165660231086939480044838177077697372649548905639806687936837163333571753827706811652513036818609532883029261006374009297124944344482022096957254333616947698779339
    d2b = 95663379056590315904958259825834214901237003770599243544865165365208432669683997300142786161500211393549178381765643941129509422466069713188826218843822811512538281155704057027426538594807456920233809771753714104220104416437553691968044000337886418775070864441063105697251708650336883364209545450177248989131
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
  # debug
  p3_dbg = map(lambda n: Rsa.Desencriptar(n, d1b, primo), p3_e1b_k_cartas)
  if p3_dbg != p3_k_cartas:
      print 'ERROR, son distintos!'
      quit()
  #/debug
  # armar la lista a empaquetar para enviar a A
  t = [primo] + p3_e1b_k_cartas
  #debug
  t.append(d1b)
  #/debug
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
  # (los primeros 4 bytes indican el tamanio en bytes del resto del contenido)
  logger.debug(pf + 'Red.Recibir(4)')
  tamStr = Red.recibir(4) # tamanio en bytes del resto del mensaje
  if tamStr == None or len(tamStr) < 4:
    logger.error(pf + 'paso 4, mensaje recibido truncado')
    raise 'paso 4, mensaje recibido truncado'
  tam = u32_to_long(tamStr)
  if tam <= 0:
    logger.error(pf + 'paso 4, Longitud del mensaje recibido incorrecta')
    raise 'Longitud del mensaje recibido incorrecta'
  logger.debug(pf + 'Red.Recibir('+ str(tam) + ')')
  msg = Red.recibir(tam)
  if len(msg) < tam:
    logger.error(pf + 'ERROR FATAL: mensaje de longitud menor a la esperada')
    raise 'ERROR FATAL: mensaje de longitud menor a la esperada'
  msg = tamStr + msg
  logger.debug(pf + 'recibido mensaje: ' + repr(msg))
  # se recibieron las cartas como tiras de bytes, convertirlas a long
  p4_listaDe43, tmp = desempaquetar_Lista_Generica(msg, infint_to_long)
  logger.debug(pf + 'p4_listaDe43 == ' + repr(p4_listaDe43))
  if tmp != '':
    logger.warn(pf + 'hay datos sobrantes al final del mensaje recibido. Se ignoran esos datos.')
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


  # 5) B desencripta las cartas que le envío A, obteniendo k(Bi) para su mano y
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
  #    Por último, A envia k a B
  pass
  nroPaso = 6
  logger.info(pf + '--- PASO 6')
  # (los primeros 4 bytes indican el tamanio en bytes del resto del contenido)
  logger.debug(pf + 'Red.Recibir(4)')
  tamStr = Red.recibir(4) # tamanio en bytes del resto del mensaje
  if tamStr == None or len(tamStr) < 4:
    logger.error(pf + 'paso 6, mensaje recibido truncado')
    raise 'Mensaje recibido truncado'
  tam = u32_to_long(tamStr)
  if tam <= 0:
    logger.error(pf + 'paso 6, Longitud del mensaje recibido incorrecta')
    raise 'Longitud del mensaje recibido incorrecta'
  logger.debug(pf + 'Red.Recibir('+ str(tam) + ')')
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


  # 7) B recibe k, la utiliza para ver que el mazo es válido y para ver las cartas
  # que le tocaron.
  #  Luego genera una clave RSA clásica (e3b, d3b, n) y envia la parte publica (e3b, n)
  # a A. Tambien envia el mensaje "SOY MANO" encriptado con d3b
  #  Formato: lista(infint(e3b), infint(n), str(d3b("SOY MANO")))

  # Con K desencriptar las cartas recibidas en el paso 5
  p7_misCartas = map(lambda t: (Matematica.bytes2long(Aes.AesDesencriptar(Matematica.long2bytes(t[0], 16), keyAes)), t[1]), p5_k_cartasParaMi)
  logger.debug('p7_misCartas = ' + repr(p7_misCartas))
  # chequear que las cartas estén en el mazo original
  cartas = CartasDesdeArchivo.cartas()
  for bi, e2akBi in p7_misCartas:
    logger.debug('Bi, e2akBi = ' + repr(bi) + ', ' + repr(e2akBi))
    if bi not in cartas:
      logger.error(pf + 'ERROR FATAL: las cartas recibidas del servidor no estan en el mazo original')
      logger.error(pf + 'Carta desconocida: ' + repr(bi))
      raise 'ERROR FATAL: las cartas recibidas del servidor no estan en el mazo original'
    else:
      carta = CartasDesdeArchivo.carta(bi)
      logger.info('Me toco la carta ' + str(carta) + ' - ' + repr(carta))


  return
