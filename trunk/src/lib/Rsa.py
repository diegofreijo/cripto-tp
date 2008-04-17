# -*- coding: cp1252 -*-
import Azar
import Matematica
from math import log


## Genera un n con primos de longitud @bits_primos y e, d para RSA
def GenerarClaves(bits_primos):
  p = Azar.Primo(bits_primos)
  while True:
    q = Azar.Primo(bits_primos)
    # Acá habría que agregar algún criterio
    # para que q no sea muy parecido a p
    if q != p: break
  #
  n = p*q

  ## Calculo e
  #e = Azar.EnteroEntre(2, fi-1)
  #while Matematica.Mcd(e, fi) != 1:
  #	e = Azar.EnteroEntre(2, fi-1)

  ## Calculo d
  #d = Matematica.Inverso(e, fi)
  #while d < 0:
  #	d = d + fi

  # Obtengo e y d
  e, d = generarEyD(p, q)

  # Devuelvo todo lo generado
  return [n, e, d]


## Genera e y d tales que e * d = 1 mod (fi(n = p*q)) para RSA
def generarEyD(p, q):
  fi = (p-1)*(q-1)

  # Calculo e
  while True:
    e = Azar.EnteroEntre(2, fi-1)
    mcd, alfa, beta = Matematica.McdExtendido(e, fi)
    if mcd == 1: break

  # Calculo d
  d = alfa
  while d < 0:
    d = d + fi

  return (e, d)


## Encriptacion y desencriptacion de numeros chicos (menores a n)
def Encriptar(plain, e, n):
	return Matematica.PotenciaModular(plain, e, n)

def Desencriptar(cypher, d, n):
	return Matematica.PotenciaModular(cypher, d, n)



## Encriptacion y desencriptacion de numeros grandes (mayores a n)
def EncriptarNumero(plain, e, n):
	raise "No implementado"

def DesencriptarNumero(cypher, d, n):
	raise "No implementado"


	
## Encriptacion y desencriptacion de texto
def EncriptarTexto(plain, e, n):
  ## Calculo cuantos bits ocupa el n y cuanto los bloques (es n - 1 para asegurarse que el bloque no es >= a n y se resta otro mas para poder agregar un bit en 1 adicional y asegurar que el bloque es un numero grande)
  tam_n = int(log(n, 2)) + 1
  tam_bloque = tam_n - 1 - 1
  
  ## Segmenta @texto en bloques de @tam_bloque bits:
  ##		el ultimo bloque es padeado con 00...01 tal que todo el ultimo bloque ocupa tam_bloque.
  ##		Si no hace falta padeo, el ultimo bloque es solo de padeo y al ante ultimo le agrega un 1 adelante
  # Lista de bloques
  bloques_plain = []
  # Bloque actual
  bloque = 0
  # Cuantos bits faltan agregar para completar el bloque
  restantes = tam_bloque
  for letra in plain:
  	# Veo si puedo agregar toda la letra o un pedazo
  	if restantes >= 8:
  		bloque |= (ord(letra) << (tam_bloque - restantes))
  		restantes -= 8
  	else:
  		# Armo una mascara para dividir la letra entre la parte que va al bloque actual y la que va al siguiente
  		mascara =  255 >> (8 - restantes)
  		primer_pedazo = ord(letra) & mascara
  		mascara = ~mascara
  		segundo_pedazo = (ord(letra) & mascara) >> restantes
  		
  		# Completo el bloque actual
  		bloque |= (primer_pedazo << (tam_bloque - restantes))
  		bloques_plain.append(bloque)
  		
  		# Comienzo el proximo bloque
  		bloque = segundo_pedazo
  		restantes = tam_bloque - (8 - restantes)
  
  # Si me quedaron bits para llenar el ultimo bloque, padeo. Si no, agrego un bloque nuevo solo de padeo
  tam_ultimo_bloque = tam_bloque - restantes
  if restantes == 0:
  	bloques_plain.append(bloque)
  	bloques_plain.append(1)
  else:
  	# Por separado, padeo el ultimo bloque
  	if restantes == 1:
  		# Si faltaba un bit, pongo un 1 en el lugar restante y agrego en otro bloque el padeo de todos 0s
  		bloque |= 1 << (tam_bloque - 1)
  		bloques_plain.append(bloque)
  		bloques_plain.append(0)
  	else:
  		# Armo una mascara para agregar el padding
  		mascara = 1 << tam_ultimo_bloque
  		bloque |= mascara
  		bloques_plain.append(bloque)
  
  
  
  ## Agrego al comienzo de cada bloque un bit en 1 para asegurarme que tengo un numero grande
  mascara = (1 << tam_bloque)
  for i in xrange(len(bloques_plain)):
  	bloques_plain[i] |= mascara
  
  
  # Encripto cada bloque por separado
  cypher = 0
  for i in xrange(len(bloques_plain)):
  	bloque_cypher = Encriptar(bloques_plain[i], e, n)
  	cypher |= bloque_cypher << (i * tam_n)
    
  # Convierto a bytes
  scypher = Matematica.long2bytes(cypher, (len(bloques_plain) * tam_n + 7) // 8) # '//' es division entera, no un comentario
  
  return scypher


def DesencriptarTexto(scypher, d, n):
  # Convierto scypher a un valor long
  cypher = Matematica.bytes2long(scypher)

  ## Separo de a bloques
  tam_n = int(log(n, 2)) + 1
  tam_cypher = int(log(cypher, 2)) + 1
  cant_bloques = (tam_cypher // tam_n) + 1
  bloques_cypher = []
  mascara = (1 << tam_n) - 1
  for i in xrange(cant_bloques):
  	bloque = cypher & mascara
  	bloque = bloque >> (i * tam_n)
  	bloques_cypher.append(bloque)
  	mascara = mascara << tam_n
  
  ## Desencripto cada bloque por separado y junto todo el texto plano
  plain = 0
  tam_bloque = tam_n - 1 - 1
  # Mascara que me saca el 1 adicional a la izquierda de todo del bloque
  mascara = (1 << tam_bloque) - 1
  for i in xrange(len(bloques_cypher)):
  	plain_actual = Desencriptar(bloques_cypher[i], d, n)
  	plain_sin_uno_adicional = plain_actual & mascara
  	plain |= (plain_sin_uno_adicional) << (i * tam_bloque)
  
  
  ## Busco el padeo y lo elimino (o sea, busco la secuencia 000...01 al comienzo del plain)
  tam_plain = int(log(plain,2))
  mascara = (1 << tam_plain) - 1
  plain &= mascara
  
  
  ## Convierto los bytes a letras
  plain_str = ""
  cant_letras = tam_plain / 8
  mascara = 255
  for i in xrange(cant_letras):
  	letra = (plain & (mascara << (i * 8))) >> (i * 8)
  	plain_str += chr(letra)
  
  return plain_str
	
	
	
	
