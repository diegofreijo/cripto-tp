# -*- coding: cp1252 -*-
import struct
import Matematica

def long_to_u32(nro):
  """
  Empaqueta el nro como un entero largo unsigned de 32 bits
  """
  return struct.pack('I', nro)

def u32_to_long(txt32bits):
  """
  Desempaqueta un texto de 32 bits que es un unsigned long a un numero
  """
  return struct.unpack('I', txt32bits)[0]

def long_to_u128(nro):
  """
  Empaqueta el nro como un entero largo unsigned de 128 bits
  """
  p0 = nro & (~(1L<<32))
  p1 = (nro>>32) & (~(1L<<32))
  p2 = (nro>>64) & (~(1L<<32))
  p3 = (nro>>96) & (~(1L<<32))
  return struct.pack('IIII', p0, p1, p2, p3)

def u128_to_long(txt128bits):
  """
  Desempaqueta un texto de 128 bits que son 4 unsigned long's de 32 bits
  a un numero long de 128 bits
  """
  t = struct.unpack('IIII', txt128bits)
  u0 = t[0]
  u1 = t[1]
  u2 = t[2]
  u3 = t[3]
  rv = ((((u3<<32) | u2)<<32) | u1)<<32 | u0
  return rv

def long_to_infint(nro):
  """
  Empaqueta el nro como un entero de longitud ilimitada (string)
  """
  #return repr(long(nro))
  return Matematica.long2bytesIlim(nro)

def infint_to_long(txt):
  """
  Desempaqueta un texto como un entero long
  """
  #return long(txt)
  return Matematica.bytes2long(txt)

def empaquetar_Lista_Generica(lista, func):
  """
  Codifica en texto una lista de valores, usando el codificador func
  para cada elemento de la lista
  """
  # formato:
  # 4 bytes ... longitud total en bytes de lo que sigue
  # 4 bytes ... tamanio de la lista
  # resto   ... cada elemento, en orden, como string empaquetado con la funcion
  #             func, prefijado con el tamanio (4 bytes)
  rv = long_to_u32(len(lista))
  for o in lista:
    t = func(o)
    rv = rv + long_to_u32(len(t)) + t
  rv = long_to_u32(len(rv)) + rv
  return rv

def desempaquetar_Lista_Generica(texto, func):
  """
  Decodifica un texto en una lista de objetos, usando para reconstruir
  cada elemento la funcion func.
  Devuelve un par (lista, restante) donde el 1er elem es la lista de objetos
  reconstruida y el segundo elemento es el texto sobrante
  """
  lista = []
  longBytesStr = texto[0:4]
  if len(longBytesStr) < 4:
    raise ValueError('desempaquetar_Lista_Generica(): longitud en bytes no presente')
  longBytes = u32_to_long(longBytesStr)
  if longBytes < 8:
    raise ValueError('desempaquetar_Lista_Generica(): longitud en bytes demasiado corta')
  longLista = u32_to_long(texto[4:8])
  msg = texto[8:(4+longBytes)]
  while len(lista) < longLista:
    print len(lista), longLista
    # Tomar un elemento mas
    if len(msg) < 4:
      print lista
      print len(msg)
      raise 'desempaquetar_Lista_Generica(): longitud en bytes de elemento demasiado corta'
    longBytesElem = u32_to_long(msg[0:4])
    if 4 + longBytesElem > len(msg):
      raise 'desempaquetar_Lista_Generica(): longitud en bytes de elemento excede bytes restantes'
    bytesElem = msg[4:(4+longBytesElem)]
    msg = msg[(4+longBytesElem):]
    elem = func(bytesElem)
    lista.append(elem)
  #
  # La cantidad de texto restante debería ser cero - si no es cero, hay
  # informacion basura
  if len(msg) > 0:
    raise 'desempaquetar_Lista_Generica(): datos sobrantes luego del final de la lista'

  # Se reconstruyo correctamente la lista. Devolver lista y datos restantes
  restante = texto[(4+longBytes):]
  return (lista, restante)
