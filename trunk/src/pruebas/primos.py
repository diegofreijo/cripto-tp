import sys
sys.path.append("..\\lib")
import Azar
import time

bits = 128
cant = 10
print "Comenzando pruebas de " + str(cant) + " primos de " + str(bits) + " bits"
for i in xrange(10):
	tiempo = time.clock()
	print str(i) + ": " + str(Azar.Primo(bits)) + "		->	" + str(time.clock() - tiempo) + " segundos"

bits = 128
cant = 10
print "Comenzando pruebas de " + str(cant) + " primos fuertes de " + str(bits) + " bits"
for i in xrange(10):
	tiempo = time.clock()
	print str(i) + ": " + str(Azar.PrimoFuerte(bits,10,10)) + "		->	" + str(time.clock() - tiempo) + " segundos"
