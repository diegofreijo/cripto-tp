from Crypto.Hash import SHA

cartas = open("cartas.txt", 'r')
hasheadas = ""

for carta in cartas:
	sha = SHA.new()
	sha.update(carta[:-1])
	hasheadas = hasheadas + carta[:-1] + ": " + str(int(sha.hexdigest(),16)) + "\n"
	
archivo_hasheadas = open("hasheadas.txt", 'w')
archivo_hasheadas.write(hasheadas)