import random

def EnterosEntre(a, b):
	random.seed()
	return random.randint(a,b)
	
def Bits(cantidad):
	random.seed()
	return random.getrandbits(cantidad)

def Primos(bits):
	raise "No implementado"