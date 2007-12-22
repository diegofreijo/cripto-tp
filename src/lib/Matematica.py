# -*- coding: cp1252 -*-
import struct
from Crypto.Util import number

def _EuclidesExtendido(a,b):
	if b == 0:
		return [a,1,0]
	else:
		ee = _EuclidesExtendido(b, a % b)
		return [ee[0], ee[2], ee[1] - (int)(a / b) * ee[2]]

def _mcd_ext(a, b):
  """
  Devolver una 3-upla (d, alfa, beta) con d=MCD(a,b) y alfa, beta
  de manera que d = alfa*a + beta*b (MAC 20071001)
  """
  if a > b:
    t = _mcd_ext(b, a)
    return (t[0], t[2], t[1])
  # Ahora tengo a <= b
  if a == 0:
    return (b, 0, 1)

  # valores de inicializacion
  alfam2 = 0
  alfam1 = 1
  betam2 = 1
  betam1 = 0
  r = 1
  while r > 0:
    # a==alfam1*a0 + betam1*b0
    # b==alfam2*a0 + betam2*b0
    c = b/a
    r = b%a
    # si r==0, el MCD es a
    alfa = alfam2 - c*alfam1
    beta = betam2 - c*betam1
    alfam2 = alfam1
    alfam1 = alfa
    betam2 = betam1
    betam1 = beta
    b = a
    a = r
  # al terminar, el MCD queda en b==alfam2*a0+betam2*b0
  return (b, alfam2, betam2)


## Devuelve el maximo comun divisor entre a y b
def Mcd(a,b):
  #return _EuclidesExtendido(a,b)[0]
  return _mcd_ext(a, b)[0]


## Devuelve el inverso multiplicativo de e en Zn (se supone que MCD(e,n) == 1)
def Inverso(e,n):
  #return _EuclidesExtendido(e,n)[1]
  return _mcd_ext(e, n)[1]


## Devuelve una 3-upla (d, alfa, beta) con d==Mcd(a, b) y
## d==alfa*a + beta*b
def McdExtendido(a, b):
  """
  Devuelve una 3-upla (d, alfa, beta) con d==Mcd(a, b) y d==alfa*a + beta*b
  """
  return _mcd_ext(a, b)


## Devuelve un string con la representacion binaria de n
def int2bin(n):
	if n < 0:  raise ValueError, "n: " + str(n)
	if n == 0: return "0"
	ret = ""
	while n > 0:
		ret = str(n % 2) + ret
		n = n >> 1
	return ret
	

## Devuelve (a**b) % n
def PotenciaModular(a, b, n):
	a2p = a % n
	a = 1
	while b != 0:
		if (b & 1) != 0:
		  a = (a * a2p) % n
		b = b >> 1
		a2p = (a2p * a2p) % n
	return a


def long2bytes(n, tamBytes):
	"""
	Convertir el entero largo positivo n en una cadena de bytes de tamaño fijo tamBytes
	El valor de retorno tiene siempre tamaño tamBytes incluso si n es demasiado grande
	para representarse con ese tamaño (en este caso contiene sólo los bytes menos significativos)
	"""
	s = ''
	n = long(n)
	while n > 0 and len(s) < tamBytes:
	  s = struct.pack('>I', n & 0xffffffffL) + s
	  n = n >> 32
	# Recortar la cadena resultante
	if len(s) > tamBytes:
		s = s[:tamBytes]
	# Extender si es más chica con ceros en la parte superior
	if len(s) < tamBytes:
		s = (tamBytes - len(s)) * '\000' + s
	return s


def long2bytesIlim(n):
	"""
	Convertir el entero largo positivo n en una cadena de bytes de tamaño ilimitado
	"""
	return number.long_to_bytes(n)


def bytes2long(s):
	"""
	Convertir una cadena de bytes en el entero largo positivo que representan sus bits.
	"""
	return number.bytes_to_long(s)


