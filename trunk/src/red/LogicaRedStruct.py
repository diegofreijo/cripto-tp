# -*- coding: cp1252 -*-
import struct
import Matematica

def _longtou32(nro):
  """
  Empaqueta el nro como un entero largo unsigned de 32 bits
  """
  return struct.pack('L', nro)

def _u32tolong(txt32bits):
  """
  Desempaqueta un texto de 32 bits que es un unsigned long a un numero
  """
  return struct.unpack('L', txt32bits)[0]

def _longtou128(nro):
  """
  Empaqueta el nro como un entero largo unsigned de 128 bits
  """
  p0 = nro & (~(1L<<32))
  p1 = (nro>>32) & (~(1L<<32))
  p2 = (nro>>64) & (~(1L<<32))
  p3 = (nro>>96) & (~(1L<<32))
  return struct.pack('LLLL', (p0,p1,p2,p3))

def _u128tolong(txt128bits):
  """
  Desempaqueta un texto de 128 bits que son 4 unsigned long's de 32 bits
  a un numero long de 128 bits
  """
  t = struct.unpack('LLLL', txt128bits)
  u0 = t[0]
  u1 = t[1]
  u2 = t[2]
  u3 = t[3]
  rv = ((((u3<<32) | u2)<<32) | u1)<<32 | u0
  return rv

def _longtoinfint(nro):
  """
  Empaqueta el nro como un entero de longitud ilimitada (string)
  """
  #return repr(long(nro))
  return Matematica.long2bytesIlim(nro)

def _infinttolong(txt):
  """
  Desempaqueta un texto como un entero long
  """
  #return long(txt)
  return Matematica.bytes2long(txt)

def _empaquetarListaGenerica(lista, func):
  """
  Codifica en texto una lista de valores, usando el codificador func
  para cada elemento de la lista
  """
  # formato:
  # 4 bytes ... longitud total en bytes de lo que sigue
  # 4 bytes ... tamanio de la lista
  # resto   ... cada elemento, en orden, como string empaquetado con la funcion
  #             func, prefijado con el tamanio (4 bytes)
  rv = _longtou32(len(lista))
  for o in lista:
    t = func(o)
    rv = rv + _longtou32(len(t)) + t
  rv = _longtou32(len(rv)) + rv
  return rv

def _desempaquetarListaGenerica(texto, func):
  """
  Decodifica un texto en una lista de objetos, usando para reconstruir
  cada elemento la funcion func.
  Devuelve un par (lista, restante) donde el 1er elem es la lista de objetos
  reconstruida y el segundo elemento es el texto sobrante
  """
  lista = []
  longBytesStr = texto[0:4]
  if len(longBytesStr) < 4:
    raise '_desempaquetarListaGenerica(): longitud en bytes no presente'
  longBytes = _u32tolong(longBytesStr)
  if longBytes < 4:
    raise '_desempaquetarListaGenerica(): longitud en bytes demasiado corta'
  longLista = _longtou32(texto[4:8])
  msg = texto[8:(4+longBytes)]
  while len(lista) < longLista:
    # Tomar un elemento mas
    if len(msg) < 4:
      raise '_desempaquetarListaGenerica(): longitud en bytes de elemento demasiado corta'
    longBytesElem = _u32tolong(msg[0:4])
    if 4 + longBytesElem > len(msg):
      raise '_desempaquetarListaGenerica(): longitud en bytes de elemento excede bytes restantes'
    bytesElem = msg[4:(4+longBytesElem)]
    msg = msg[(4+longBytesElem):]
    elem = func(bytesElem)
    lista.append(elem)
  #
  # La cantidad de texto restante debería ser cero - si no es cero, hay
  # informacion basura
  if len(msg) > 0:
    raise '_desempaquetarListaGenerica(): datos sobrantes luego del final de la lista'

  # Se reconstruyo correctamente la lista. Devolver lista y datos restantes
  restante = texto[(4+longBytes):]
  return (lista, restante)
