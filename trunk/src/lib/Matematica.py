def _EuclidesExtendido(a,b):
	if b == 0:
		return [a,1,0]
	else:
		ee = EuclidesExtendido(b, a % b)
		return [ee[0], ee[2], ee[1] - (int)(a / b) * ee[2]]


## Devuelve el maximo comun divisor entre a y b
def Mcd(a,b):
	return _EuclidesExtendido(a, b)[0]


## Devuelve el inverso multiplicativo de e en Zn (se supone que MCD(e,n) == 1)
def Inverso(e,n):
	return _EuclidesExtendido(e, fi)[1]
	

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
	while b > 0:
		if b & 1 > 0:
		  a = (a * a2p) % n
		b = b >> 1
		a2p = (a2p * a2p) % n
	return a
