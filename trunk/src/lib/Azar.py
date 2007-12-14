import random

def EnteroEntre(a, b):
	random.seed()
	return random.randint(a,b)
	
def Bits(cantidad):
	random.seed()
	return random.getrandbits(cantidad)

def Primo(bits):
	raise "No implementado"