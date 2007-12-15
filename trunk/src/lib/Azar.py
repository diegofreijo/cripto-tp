import random
import Matematica

def EnteroEntre(a, b):
	random.seed()
	return random.randint(a,b)


def Bits(cantidad):
	random.seed()
	return random.getrandbits(cantidad)


## Test de primalidad Miller-Rabin sobre n, para una probabilidad de declarar primo a un n compuesto de 4**{-k}
_primeros_primos = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]
def MillerRabin(n, k = 10):
    n = abs(n)
    if (n & 1) == 0: return (n == 2)
    for t in _primeros_primos:
        if (n % t) == 0: return (n == t)
    d = n - 1
    s = 0
    # obtener n-1 = 2**s * d
    while (d & 1) == 0:
        d = (d >> 1)
        s = s + 1
    # proceder k veces:
    i = 0
    while i < k:
        i = i + 1
        # obtener un numero aleatorio a entre 1 y n-1
        a = EnteroEntre(2, n-1)
        # obtener a^d mod n
        a2d = Matematica.PotenciaModular(a, d, n)
        if a2d == 1:
            # n es un probablemente un primo. Intentar con otros a's
            continue
        # para cada r entre 0 y s-1, testear a**((2**r)*d)
        r = 0
        while r < s:
            # a^((2^r)*d) debe ser != n-1 para todos los r's
            if a2d == n-1:
                # n es un probablemente un primo. Intentar con otros a's
                #print 'a^((2^r)*d) == n-1 - con n-1=', n-1
                break
            r = r + 1
            if r < s: a2d = (a2d * a2d) % n
        # si r < s algun a^((2^r)*d) era == -1 mod n, o sea n era un probable primo
        if r == s: return False # es compuesto (seguro)
    return True # es un probable primo

	
	
def Primo(bits):
	while 1:
		n = Bits(bits)
		if MillerRabin(n,10): break
	return n
	
